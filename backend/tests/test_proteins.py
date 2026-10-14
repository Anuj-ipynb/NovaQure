"""
Unit tests for NovaQure Protein Target Registry & Selectivity Service
"""

import unittest
from backend.proteins.protein_registry import TARGET_REGISTRY, get_target_info, list_targets
from backend.proteins.protein_service import ProteinService
from backend.evaluation.affinity_service import AffinityService


class TestProteinService(unittest.TestCase):

    def test_target_registry_contains_approved_targets(self):
        expected_targets = {"EGFR", "KRAS", "BACE1", "HER2", "BRAF"}
        self.assertTrue(expected_targets.issubset(set(TARGET_REGISTRY.keys())))

    def test_get_target_info(self):
        egfr = get_target_info("EGFR")
        self.assertIsNotNone(egfr)
        self.assertEqual(egfr.gene_symbol, "EGFR")
        self.assertEqual(egfr.uniprot_id, "P00533")

        kras = get_target_info("KRAS")
        self.assertIsNotNone(kras)
        self.assertEqual(kras.chembl_id, "CHEMBL2189121")

    def test_protein_service_catalog(self):
        service = ProteinService()
        targets = service.get_all_targets()
        self.assertGreaterEqual(len(targets), 5)
        
        target_ids = [t["id"] for t in targets]
        self.assertIn("EGFR", target_ids)
        self.assertIn("BACE1", target_ids)

    def test_affinity_service_multi_target_fallback(self):
        affinity_service = AffinityService()
        # Test valid SMILES prediction across different target_protein keys
        aff_egfr = affinity_service.predict("CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5", target_protein="EGFR")
        self.assertIsInstance(aff_egfr, float)
        self.assertGreater(aff_egfr, 0.0)

        aff_kras = affinity_service.predict("CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5", target_protein="KRAS")
        self.assertIsInstance(aff_kras, float)
        self.assertGreater(aff_kras, 0.0)


if __name__ == "__main__":
    unittest.main()
