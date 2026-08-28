from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from functools import lru_cache
from rdkit import Chem

logger = logging.getLogger(__name__)


class IUPACService:
    """
    Hybrid Real-Time IUPAC Name Resolver Service.

    Resolves SMILES strings into official IUPAC chemical names using PubChem PUG REST API
    with instantaneous LRU caching and RDKit offline fallback.
    """

    @staticmethod
    @lru_cache(maxsize=2048)
    def resolve(smiles: str) -> str:
        """
        Resolve a SMILES string to its official IUPAC chemical name.
        """
        if not smiles or not isinstance(smiles, str):
            return "Unknown Candidate"

        # Step 1: Attempt PubChem PUG REST API lookup
        try:
            encoded_smiles = urllib.parse.quote(smiles, safe="")
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encoded_smiles}/property/IUPACName/JSON"
            
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "NovaQure-Biotech-Platform/1.0"}
            )
            
            with urllib.request.urlopen(req, timeout=0.5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    props = data.get("PropertyTable", {}).get("Properties", [])
                    if props and "IUPACName" in props[0]:
                        name = props[0]["IUPACName"]
                        logger.info("Resolved official PubChem IUPAC name for SMILES %s: %s", smiles, name)
                        return name
        except Exception:
            # Silent fallback when PubChem API is unreachable or SMILES is a novel mutation
            pass

        # Step 2: RDKit Offline Fallback Descriptor Generator
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                # Analyze core ring systems
                ring_info = mol.GetRingInfo()
                num_rings = ring_info.NumRings()
                num_atoms = mol.GetNumAtoms()
                
                # Detect key pharmaceutical heterocycles
                smarts_quinazoline = Chem.MolFromSmarts("c1cnc2ccccc2n1")
                smarts_pyridine = Chem.MolFromSmarts("c1ccncc1")
                smarts_aniline = Chem.MolFromSmarts("c1ccccc1N")
                smarts_indole = Chem.MolFromSmarts("c1ccc2[nH]ccc2c1")
                smarts_pyrimidine = Chem.MolFromSmarts("c1cncnc1")
                
                if smarts_quinazoline and mol.HasSubstructMatch(smarts_quinazoline):
                    return f"4-Anilinoquinazoline Analog ({num_atoms} Atoms)"
                elif smarts_aniline and mol.HasSubstructMatch(smarts_aniline):
                    return f"Substituted Anilino-Heterocycle ({num_atoms} Atoms)"
                elif smarts_indole and mol.HasSubstructMatch(smarts_indole):
                    return f"Indolyl Bioactive Lead ({num_atoms} Atoms)"
                elif smarts_pyrimidine and mol.HasSubstructMatch(smarts_pyrimidine):
                    return f"Pyrimidine Core Scaffold ({num_atoms} Atoms)"
                elif smarts_pyridine and mol.HasSubstructMatch(smarts_pyridine):
                    return f"Pyridinyl Substituted Scaffold ({num_atoms} Atoms)"
                elif num_rings >= 2:
                    return f"Polycyclic Targeted Lead ({num_atoms} Atoms)"
                else:
                    return f"Substituted Heterocycle ({num_atoms} Atoms)"
        except Exception:
            pass

        return "Novel Targeted Bioactive Lead"
