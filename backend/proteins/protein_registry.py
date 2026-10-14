"""
NovaQure Protein Target Registry Catalog

Centralized static metadata for key therapeutic target proteins across
Oncology and Neurodegenerative drug discovery domains.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TargetProteinInfo:
    id: str
    name: str
    gene_symbol: str
    uniprot_id: str
    chembl_id: str
    pdb_id: str
    disease_domain: str
    indication: str
    active_site_residues: List[str]
    default_threshold_pic50: float
    description: str


TARGET_REGISTRY: Dict[str, TargetProteinInfo] = {
    "EGFR": TargetProteinInfo(
        id="EGFR",
        name="Epidermal Growth Factor Receptor",
        gene_symbol="EGFR",
        uniprot_id="P00533",
        chembl_id="CHEMBL203",
        pdb_id="1M17",
        disease_domain="Oncology",
        indication="Non-Small Cell Lung Cancer (NSCLC) & Glioblastoma",
        active_site_residues=["Met793", "Thr790", "Lys745", "Leu844"],
        default_threshold_pic50=7.0,
        description="Receptor tyrosine kinase driving cell proliferation. Primary target for EGFR kinase inhibitors (Erlotinib, Gefitinib, Osimertinib)."
    ),
    "KRAS": TargetProteinInfo(
        id="KRAS",
        name="GTPase KRas (G12D / G12C)",
        gene_symbol="KRAS",
        uniprot_id="P01116",
        chembl_id="CHEMBL2189121",
        pdb_id="6OIM",
        disease_domain="Oncology",
        indication="Pancreatic, Colorectal, and NSCLC Cancers",
        active_site_residues=["Cys12", "Asp12", "Lys16", "Tyr96"],
        default_threshold_pic50=6.5,
        description="Small GTPase oncogene driver. Key target for covalent allele-specific inhibitors (Sotorasib, Adagrasib)."
    ),
    "BACE1": TargetProteinInfo(
        id="BACE1",
        name="Beta-Site APP Cleaving Enzyme 1",
        gene_symbol="BACE1",
        uniprot_id="P56817",
        chembl_id="CHEMBL4822",
        pdb_id="1FKN",
        disease_domain="Neurodegeneration",
        indication="Alzheimer's Disease & Amyloid Plaque Pathology",
        active_site_residues=["Asp32", "Asp228", "Thr72", "Arg128"],
        default_threshold_pic50=6.8,
        description="Transmembrane aspartyl protease initiating amyloid-beta production. Key therapeutic target for Alzheimer's neurodegeneration."
    ),
    "HER2": TargetProteinInfo(
        id="HER2",
        name="Human Epidermal Growth Factor Receptor 2",
        gene_symbol="ERBB2",
        uniprot_id="P04626",
        chembl_id="CHEMBL1824",
        pdb_id="3RCD",
        disease_domain="Oncology",
        indication="HER2+ Breast Cancer & Gastric Adenocarcinoma",
        active_site_residues=["Thr798", "Met801", "Lys753", "Leu852"],
        default_threshold_pic50=7.0,
        description="ERBB family kinase receptor. Primary off-target counter-screening partner to evaluate EGFR kinase selectivity index."
    ),
    "BRAF": TargetProteinInfo(
        id="BRAF",
        name="Serine/Threonine-Protein Kinase B-Raf (V600E)",
        gene_symbol="BRAF",
        uniprot_id="P15056",
        chembl_id="CHEMBL5145",
        pdb_id="4EHE",
        disease_domain="Oncology",
        indication="Melanoma, Colorectal, and Thyroid Cancers",
        active_site_residues=["Val600", "Glu600", "Lys483", "Asp594"],
        default_threshold_pic50=7.2,
        description="Serine/threonine kinase driving the MAPK signaling pathway. Key target for selective BRAF inhibitors (Vemurafenib, Dabrafenib)."
    ),
}


def get_target_info(target_id: str) -> Optional[TargetProteinInfo]:
    return TARGET_REGISTRY.get(target_id.upper())


def list_targets() -> List[TargetProteinInfo]:
    return list(TARGET_REGISTRY.values())
