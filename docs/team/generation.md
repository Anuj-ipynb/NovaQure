# NovaQure Generation Lead

## Mission

Build the molecular generation subsystem capable of producing valid drug-like molecules from target proteins.

---

## You Own

```text
backend/generation/
backend/sampling/
datasets/
```

You do NOT modify:

```text
evaluation/
aqkc/
nqre/
ranking/
amde/
frontend/
```

---

## Branch

```bash
git checkout -b feature/generation
```

---

## Phase 1

Implement:

```text
dataset_loader.py
smiles_validator.py
selfies_converter.py
```

Output Contract:

```json
{
  "molecule_id": "uuid",
  "smiles": "CCO",
  "selfies": "[C][C][O]"
}
```

---

## Phase 2

Implement:

```text
jtvae_service.py
generation_service.py
```

Output:

```python
List[Molecule]
```

---

## Phase 3

Implement:

```text
qcbm_sampler.py
latent_sampler.py
```

---

## Deliverables

```text
Generated Molecules
SELFIES Conversion
Latent Embeddings
JTVAE Integration
QCBM Sampling
```

---

## Verification

Generate:

```text
100 molecules
```

Requirements:

```text
RDKit Validity > 90%
```

---

## Integration Output

File:

```text
outputs/artifacts/generated_molecules.json
```

---

## Git Workflow

```bash
git add .
git commit -m "feat: generation module"
git push
```

Create PR → develop

---

## Definition of Done

* Tests pass
* README exists
* Integration example exists
* Output follows contract
* No hardcoded paths
 

---
## MASTER PROMPT FOR IMPLEMENTATION
You are the Lead Molecular Generation Engineer for NovaQure.

Context:

NovaQure is a Hybrid AI–Quantum Drug Discovery Framework.

Your ownership includes:

* Molecular Generation Engine
* Dataset Processing
* SELFIES Pipeline
* Latent Space Construction
* JTVAE Integration
* QCBM-inspired Sampling

Current Architecture:

Protein → Generation → Sampling → Evaluation → AQKC → NQRE → Ranking → AMDE

Requirements:

1. Use Python 3.12.
2. Follow FastAPI modular architecture.
3. Use RDKit and SELFIES.
4. Do not create monolithic scripts.
5. Follow Repository → Service → DTO patterns.
6. Every module must be independently testable.

Tasks:

Step 1:
Create dataset ingestion pipeline.

Deliver:

* dataset_loader.py
* smiles_validator.py
* selfies_converter.py

Step 2:
Create preprocessing pipeline.

Deliver:

* canonicalize_smiles()
* remove_duplicates()
* generate_selfies()

Step 3:
Create latent-space abstraction.

Deliver:

* latent_vector.py
* latent_sampler.py

Step 4:
Implement JTVAE integration layer.

Deliver:

* jtvae_service.py
* generation_service.py

Step 5:
Implement QCBM-inspired sampler.

Deliver:

* qcbm_sampler.py

Output Requirements:

* Generate complete production-ready code.
* Include imports.
* Include typing.
* Include tests.
* Include directory structure.
* Include setup instructions.
* Include integration instructions with evaluation module.

Never provide pseudocode.
Always provide executable code.

---