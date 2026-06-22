# NovaQure Team Execution Guide

## Project Objective

Build a complete implementation of NovaQure:

```text
Protein
↓
Generation
↓
Evaluation
↓
AQKC
↓
NQRE
↓
Ranking
↓
AMDE
↓
Optimization
↓
Dashboard
```

Every team member owns a module and delivers independently while adhering to shared contracts.

---

# Global Rules

## Before Writing Any Code

Read:

```text
docs/project/PRD.md
docs/project/architecture.md
docs/project/roadmap.md
docs/project/ai-instructions.md
docs/project/api-spec.md
docs/project/module-contracts.md
```

No code should be written before understanding these documents.

---

## Git Workflow

### Initial Setup

```bash
git clone <repo-url>

git checkout develop

git pull
```

---

### Create Your Branch

Generation Lead:

```bash
git checkout -b feature/generation
```

Evaluation Lead:

```bash
git checkout -b feature/evaluation
```

Optimization Lead:

```bash
git checkout -b feature/optimization
```

Platform Lead:

```bash
git checkout -b feature/platform
```

---

### Daily Workflow

```bash
git add .

git commit -m "feat: implemented module"

git push origin <branch-name>
```

Create Pull Request → develop

Never push directly to:

```text
main
develop
```

---

# Shared Contracts

All modules communicate using contracts.

Location:

```text
backend/contracts/
```

Required:

```text
molecule.py
evaluation.py
reliability.py
ranking.py
agent.py
```

Nobody changes contracts without team discussion.

---

# Team Member 1

# Generation Lead

## Ownership

```text
backend/generation/
backend/sampling/
datasets/
```

---

## Objective

Generate chemically valid molecules.

---

## Deliverables

### Week 1

Dataset pipeline.

Create:

```text
dataset_loader.py
smiles_validator.py
selfies_converter.py
```

Output:

```json
{
  "molecule_id":"1",
  "smiles":"CCO",
  "selfies":"[C][C][O]"
}
```

---

### Week 2

JTVAE integration.

Create:

```text
jtvae_service.py
generation_service.py
```

Output:

```json
[
  {
    "molecule_id":"1",
    "smiles":"..."
  }
]
```

---

### Week 3

QCBM-inspired sampling.

Create:

```text
qcbm_sampler.py
latent_sampler.py
```

---

## Verification

Must generate:

```text
100 molecules
```

with:

```text
>90% validity
```

using RDKit validation.

---

## Master Prompt

Use the Generation Lead prompt provided in project documentation.

---

# Team Member 2

# Evaluation Lead

## Ownership

```text
backend/evaluation/
backend/aqkc/
backend/nqre/
```

---

## Objective

Evaluate molecules and compute reliability.

---

## Deliverables

### Week 1

RDKit metrics.

Implement:

```text
qed_service.py
lipinski_service.py
sa_service.py
```

---

### Week 2

Chemprop integration.

Implement:

```text
affinity_service.py
```

---

### Week 3

AQKC.

Implement:

```text
aqkc_service.py
```

Output:

```json
{
  "corrected_energy": -1.2,
  "noise_score": 0.14
}
```

---

### Week 4

NQRE.

Implement:

```text
nqre_service.py
```

Output:

```json
{
  "reliability_score": 0.91,
  "confidence_score": 0.88
}
```

---

## Verification

Every molecule must contain:

```text
QED
SA
Affinity
Reliability
Confidence
```

---

## Master Prompt

Use the Evaluation Lead prompt provided in project documentation.

---

# Team Member 3

# Optimization Lead

## Ownership

```text
backend/ranking/
backend/amde/
backend/orchestrator/
```

---

## Objective

Create explainable optimization loop.

---

## Deliverables

### Week 1

Ranking engine.

Create:

```text
ranking_service.py
```

Input:

```json
{
  "qed":0.8,
  "sa":0.7,
  "affinity":-8.1,
  "reliability":0.9
}
```

Output:

```json
{
  "rank":1,
  "score":92.4
}
```

---

### Week 2

AMDE.

Create:

```text
amde_service.py
```

Output:

```json
{
  "decision":"refine",
  "reason":"low affinity",
  "confidence":0.82
}
```

---

### Week 3

Optimization orchestrator.

Create:

```text
optimization_pipeline.py
```

---

## Verification

Run:

```text
5 optimization cycles
```

and show improvement trend.

---

## Master Prompt

Use the Optimization Lead prompt provided in project documentation.

---

# Team Member 4

# Platform Lead

## Ownership

```text
backend/api/
backend/database/
backend/auth/
frontend/
```

---

## Objective

Create APIs, storage, dashboard, and deployment.

---

## Deliverables

### Week 1

Database.

Create:

```text
users
projects
experiments
molecules
evaluations
rankings
agent_logs
```

---

### Week 2

FastAPI.

Create:

```text
health
projects
experiments
generation
evaluation
ranking
```

endpoints.

---

### Week 3

Frontend.

Create:

```text
Project Dashboard
Experiment Dashboard
Molecule Viewer
Ranking Dashboard
```

---

### Week 4

Authentication and deployment.

---

## Verification

Complete pipeline visible in browser.

---

## Master Prompt

Use the Platform Lead prompt provided in project documentation.

---

# Integration Schedule

## End of Week 1

Expected:

```text
Protein
↓
Molecule Generation
↓
Database Storage
```

---

## End of Week 2

Expected:

```text
Generation
↓
Evaluation
↓
AQKC
```

---

## End of Week 3

Expected:

```text
Generation
↓
Evaluation
↓
AQKC
↓
NQRE
↓
Ranking
```

---

## End of Week 4

Expected:

```text
Generation
↓
Evaluation
↓
AQKC
↓
NQRE
↓
Ranking
↓
AMDE
```

---

## End of Week 5

Expected:

```text
Complete Dashboard
```

---

# Definition of Done

A module is complete only if it includes:

* Source code
* Unit tests
* README
* Input schema
* Output schema
* Integration instructions
* Verification example

No module is considered finished with code alone.
