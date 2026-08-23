# -*- coding: utf-8 -*-
"""Variational Junction‑Tree Molecular Encoder (VJTVAE).

This module implements a lightweight variational encoder that:
  1. Parses a SMILES string (decoded from SELFIES).
  2. Constructs a molecular graph using RDKit.
  3. Performs a few rounds of message‑passing using plain PyTorch (no torch‑geometric).
  4. Aggregates node embeddings to obtain a graph representation.
  5. Projects the graph representation to a mean (μ) and log‑variance (logσ) vector.
  6. Samples a latent vector ``z`` via the re‑parameterisation trick.

During training we also predict a small set of phys‑chemical descriptors
(e.g. MolWt, LogP, H‑bond donors/acceptors, rotatable bonds).  The loss
combines a mean‑squared‑error term for these regression targets and a KL
divergence term that regularises the latent distribution toward a standard
Gaussian.

The class conforms to the ``BaseEncoder`` interface used by
:class:`backend.generation.encoder_service.EncoderService`.
"""

from __future__ import annotations

import logging
import math
import os
from typing import List

logger = logging.getLogger(__name__)

import torch
import torch.nn as nn
import torch.nn.functional as F
from rdkit import Chem
from rdkit.Chem import Descriptors

from backend.generation.base_encoder import BaseEncoder
from backend.generation.selfies_converter import selfies_to_smiles

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _atom_features(atom: Chem.rdchem.Atom) -> List[float]:
    """Return a simple feature vector for a single atom.

    Features used:
        - One‑hot atom type (C, N, O, F, S, Cl, Br, I, others)
        - Atom degree (0‑4)
        - Formal charge
        - Aromatic flag (0/1)
    The vector length is fixed (11)."""
    atom_type = atom.GetSymbol()
    types = ["C", "N", "O", "F", "S", "Cl", "Br", "I"]
    type_one_hot = [1.0 if atom_type == t else 0.0 for t in types]
    # Pad to length 8
    if len(type_one_hot) < 8:
        type_one_hot += [0.0] * (8 - len(type_one_hot))
    degree = [float(atom.GetDegree()) / 4.0]  # normalised
    charge = [float(atom.GetFormalCharge()) / 3.0]  # typical range –3..+3
    aromatic = [1.0 if atom.GetIsAromatic() else 0.0]
    return type_one_hot + degree + charge + aromatic


def _mol_to_graph(mol: Chem.Mol) -> tuple[torch.Tensor, torch.Tensor]:
    """Convert an RDKit Mol into node/edge tensors.

    Returns
    -------
    node_feats : torch.Tensor of shape (N, F)
        Feature vectors for each atom.
    edge_index : torch.LongTensor of shape (2, E)
        Edge list in COO format (source, target).  Undirected edges are
        represented twice (i → j and j → i) for simplicity.
    """
    N = mol.GetNumAtoms()
    node_feats = []
    for atom in mol.GetAtoms():
        node_feats.append(_atom_features(atom))
    node_feats = torch.tensor(node_feats, dtype=torch.float32)

    edge_src = []
    edge_dst = []
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        edge_src.extend([i, j])
        edge_dst.extend([j, i])
    if len(edge_src) == 0:
        # isolated atom – create a self‑loop to avoid empty edge list
        edge_src = list(range(N))
        edge_dst = list(range(N))
    edge_index = torch.tensor([edge_src, edge_dst], dtype=torch.long)
    return node_feats, edge_index


def _compute_descriptors(mol: Chem.Mol) -> torch.Tensor:
    """Return a small descriptor vector used as a proxy regression target.

    The vector consists of:
        - MolWt (scaled by 100)
        - LogP
        - NumHDonors
        - NumHAcceptors
        - NumRotatableBonds
    All values are cast to ``float32``.
    """
    wt = Descriptors.MolWt(mol) / 100.0
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    rot = Descriptors.NumRotatableBonds(mol)
    return torch.tensor([wt, logp, hbd, hba, rot], dtype=torch.float32)

# ---------------------------------------------------------------------------
# Model definition
# ---------------------------------------------------------------------------

class VariationalJTVAE(BaseEncoder, nn.Module):
    """Variational Junction‑Tree encoder compatible with ``EncoderService``.

    Parameters
    ----------
    latent_dim : int, default 128
        Dimensionality of the latent space.
    hidden_dim : int, default 256
        Size of hidden node embeddings.
    mp_steps : int, default 2
        Number of message‑passing iterations.
    """

    def __init__(self, latent_dim: int = 128, hidden_dim: int = 256, mp_steps: int = 2, model_path: str | None = "models/vjtv.pt"):
        super().__init__()
        nn.Module.__init__(self)
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim
        self.mp_steps = mp_steps

        # Input node feature size = 11 (see _atom_features)
        self.node_encoder = nn.Linear(11, hidden_dim)
        self.message_mlp = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, hidden_dim)
        )
        # Graph read‑out (sum) → hidden_dim
        self.graph_proj = nn.Linear(hidden_dim, hidden_dim)
        # μ and logσ heads
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)
        # Descriptor regression head (optional proxy)
        self.descriptor_head = nn.Linear(latent_dim, 5)

        # Attempt to load trained checkpoint if present
        if model_path and os.path.exists(model_path):
            try:
                checkpoint = torch.load(model_path, map_location="cpu")
                state_dict = checkpoint.get("model_state_dict", checkpoint)
                self.load_state_dict(state_dict)
                self.eval()
            except Exception as e:
                logger.warning("Failed to load VJTVAE checkpoint from %s: %s", model_path, e)

    # ---------------------------------------------------------------------
    # Core encoder interface
    # ---------------------------------------------------------------------
    def encode(self, selfies_string: str) -> List[float]:
        """Encode a SELFIES string and return a latent vector (list of floats)."""
        try:
            smiles = selfies_to_smiles(selfies_string)
        except Exception as e:
            raise ValueError(f"Invalid SELFIES string: {selfies_string}") from e
        if not smiles:
            raise ValueError("Decoded SMILES string is empty")
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES representation: {smiles}")
        node_feats, edge_index = _mol_to_graph(mol)
        # Move to device (CPU – training script will handle GPU transfer)
        device = torch.device("cpu")
        node_feats = node_feats.to(device)
        edge_index = edge_index.to(device)
        # Initial node embeddings
        h = self.node_encoder(node_feats)  # (N, hidden_dim)
        # Message passing
        for _ in range(self.mp_steps):
            # Gather neighbor messages
            src, dst = edge_index
            msg = h[src]
            # Aggregate (sum) messages for each destination node
            agg = torch.zeros_like(h)
            agg = agg.index_add(0, dst, msg)
            # Update node features
            h = self.message_mlp(agg + h)
        # Graph read‑out (sum over nodes)
        g = torch.sum(h, dim=0)  # (hidden_dim,)
        g = F.relu(self.graph_proj(g))
        mu = self.fc_mu(g)
        logvar = self.fc_logvar(g)
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        z = mu + eps * std
        # Return as Python list for consistency with other encoders
        return z.detach().cpu().numpy().astype(float).tolist()

    # ---------------------------------------------------------------------
    # Auxiliary methods used during training (not part of the public API)
    # ---------------------------------------------------------------------
    def forward(self, mol: Chem.Mol) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass used by the training script.

        Returns ``(mu, logvar, descriptor_pred)``.
        """
        node_feats, edge_index = _mol_to_graph(mol)
        device = next(self.parameters()).device
        node_feats = node_feats.to(device)
        edge_index = edge_index.to(device)
        h = self.node_encoder(node_feats)
        for _ in range(self.mp_steps):
            src, dst = edge_index
            msg = h[src]
            agg = torch.zeros_like(h)
            agg = agg.index_add(0, dst, msg)
            h = self.message_mlp(agg + h)
        g = torch.sum(h, dim=0)
        g = F.relu(self.graph_proj(g))
        mu = self.fc_mu(g)
        logvar = self.fc_logvar(g)
        z = mu  # for descriptor regression we use the mean vector
        descriptor_pred = self.descriptor_head(z)
        return mu, logvar, descriptor_pred

    def compute_kl(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        """KL divergence between ``N(mu, sigma)`` and standard normal.
        Returns a scalar (mean over batch)."""
        kl = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
        return kl

    def compute_regression_loss(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Mean‑squared‑error loss for descriptor regression."""
        return F.mse_loss(pred, target)

    def _mol_to_graph(self, mol: Chem.Mol) -> tuple[torch.Tensor, torch.Tensor]:
        """Delegate graph conversion to module-level helper."""
        return _mol_to_graph(mol)

    # ``BaseEncoder`` does not define a ``train`` method; the training script
    # will instantiate this class directly and use the ``forward`` method.

# ---------------------------------------------------------------------------
# End of module
# ---------------------------------------------------------------------------
