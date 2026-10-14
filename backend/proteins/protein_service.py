"""
NovaQure Protein Service

Provides service-layer access to target protein catalog metadata and trained model status.
"""

from __future__ import annotations
import logging
from typing import Dict, List, Any
from backend.configs.chembl_config import MODEL_ROOT
from backend.proteins.protein_registry import TARGET_REGISTRY, TargetProteinInfo

logger = logging.getLogger(__name__)


class ProteinService:

    def __init__(self) -> None:
        self.model_dir = MODEL_ROOT / "chemprop"

    def is_model_ready(self, target_id: str) -> bool:
        target_key = target_id.lower()
        model_file = self.model_dir / f"{target_key}_model.pt"
        if model_file.exists():
            return True
        if target_key == "egfr":
            fallback = self.model_dir / "best.pt"
            return fallback.exists()
        return False

    def get_all_targets(self) -> List[Dict[str, Any]]:
        targets = []
        for key, info in TARGET_REGISTRY.items():
            ready = self.is_model_ready(key)
            targets.append({
                "id": info.id,
                "name": info.name,
                "gene_symbol": info.gene_symbol,
                "uniprot_id": info.uniprot_id,
                "chembl_id": info.chembl_id,
                "pdb_id": info.pdb_id,
                "disease_domain": info.disease_domain,
                "indication": info.indication,
                "active_site_residues": info.active_site_residues,
                "default_threshold_pic50": info.default_threshold_pic50,
                "description": info.description,
                "model_ready": ready,
            })
        return targets

    def get_target(self, target_id: str) -> Dict[str, Any] | None:
        key = target_id.upper()
        info = TARGET_REGISTRY.get(key)
        if not info:
            return None
        return {
            "id": info.id,
            "name": info.name,
            "gene_symbol": info.gene_symbol,
            "uniprot_id": info.uniprot_id,
            "chembl_id": info.chembl_id,
            "pdb_id": info.pdb_id,
            "disease_domain": info.disease_domain,
            "indication": info.indication,
            "active_site_residues": info.active_site_residues,
            "default_threshold_pic50": info.default_threshold_pic50,
            "description": info.description,
            "model_ready": self.is_model_ready(key),
        }
