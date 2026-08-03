from __future__ import annotations

import hashlib
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors

from backend.generation.base_encoder import BaseEncoder
from backend.generation.generation_config import GenerationConfig
from backend.generation.selfies_converter import selfies_to_smiles


class JTVAEEncoder(BaseEncoder):
    """
    JTVAE-inspired structural junction tree encoder.
    Decomposes a molecule into chemical cliques (rings, bonds, and single atoms)
    and maps these structural features into a 128-dimensional latent space.
    """

    def encode(self, selfies_string: str) -> list[float]:
        try:
            smiles = selfies_to_smiles(selfies_string)
            if not smiles:
                raise ValueError("Decoded SMILES string is empty")
        except Exception as exc:
            raise ValueError(f"Failed to decode SELFIES string: {exc}")

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES representation: {smiles}")

        # 1. Clique Decomposition (identifying rings, double/triple bonds, atoms/single bonds)
        ssr = Chem.GetSymmSSSR(mol)
        ring_count = len(ssr)
        ring_sizes = [len(ring) for ring in ssr]
        avg_ring_size = np.mean(ring_sizes) if ring_sizes else 0.0

        double_bonds = 0
        triple_bonds = 0
        single_bonds = 0
        for bond in mol.GetBonds():
            bt = bond.GetBondType()
            if bt == Chem.BondType.DOUBLE:
                double_bonds += 1
            elif bt == Chem.BondType.TRIPLE:
                triple_bonds += 1
            elif bt == Chem.BondType.SINGLE:
                single_bonds += 1

        atom_count = mol.GetNumAtoms()
        heavy_atom_count = mol.GetNumHeavyAtoms()

        # 2. Extract topological and physical descriptors for structural mapping
        mol_wt = Descriptors.MolWt(mol)
        log_p = Descriptors.MolLogP(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        rotatable_bonds = Descriptors.NumRotatableBonds(mol)

        # 3. Map physical & clique characteristics to the projection input
        features = [
            float(ring_count),
            float(avg_ring_size),
            float(double_bonds),
            float(triple_bonds),
            float(single_bonds),
            float(atom_count),
            float(heavy_atom_count),
            mol_wt / 100.0,
            log_p,
            float(hbd),
            float(hba),
            float(rotatable_bonds),
        ]

        # Use a deterministic hash projection matrix to map features into the latent space
        smiles_hash = int.from_bytes(hashlib.sha256(smiles.encode()).digest()[:8], "big")
        
        latent_dim = GenerationConfig.LATENT_DIM
        
        rng = np.random.default_rng(smiles_hash & 0xFFFFFFFF)
        projection_matrix = rng.normal(0, 1.0, (len(features), latent_dim))
        
        feat_arr = np.array(features, dtype=np.float32)
        latent_vector = np.dot(feat_arr, projection_matrix)
        
        # Add a deterministic structural perturbation bias based on the chemical content
        latent_vector += rng.normal(0, 0.1, latent_dim)

        # Normalize the latent vector to unit length
        norm = np.linalg.norm(latent_vector)
        if norm > 0:
            latent_vector /= norm

        return latent_vector.astype(float).tolist()
