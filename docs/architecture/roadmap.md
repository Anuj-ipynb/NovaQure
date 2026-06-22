# roadmap.md

# NovaQure Implementation Roadmap

## Project Objective

Build a modular AI–Quantum Drug Discovery Platform capable of:

1. Generating molecules.
2. Evaluating molecular quality.
3. Estimating reliability.
4. Iteratively refining candidates.
5. Producing explainable rankings.
6. Supporting future publication and patent filing.

---

# PHASE 0 — Repository & Development Foundation

## Goal

Establish a reproducible development environment and project structure.

---

## Pre-Requisites

None.

---

## Task Checklist

### Repository Setup

* [ ] Create GitHub repository.
* [ ] Configure branch strategy.
* [ ] Create `.gitignore`.
* [ ] Create `README.md`.
* [ ] Create `LICENSE`.

### Project Structure

* [ ] Create backend directory.
* [ ] Create frontend directory.
* [ ] Create datasets directory.
* [ ] Create outputs directory.
* [ ] Create docs directory.
* [ ] Create reports directory.
* [ ] Create experiments directory.

### Python Environment

* [ ] Create virtual environment.
* [ ] Configure requirements.txt.
* [ ] Install FastAPI.
* [ ] Install PyTorch.
* [ ] Install RDKit.
* [ ] Install PennyLane.
* [ ] Install Chemprop.

### Developer Tooling

* [ ] Configure Ruff.
* [ ] Configure Black.
* [ ] Configure Pytest.
* [ ] Configure Pre-Commit Hooks.

---

## Verification

Pass:

```bash
pytest
ruff check .
black --check .
```

Repository builds successfully on a clean machine.

---

# PHASE 1 — Data Layer Foundation

## Goal

Create persistent storage for projects, experiments, molecules, and evaluations.

---

## Pre-Requisites

Phase 0 completed.

---

## Task Checklist

### Database Setup

* [ ] Configure SQLite.
* [ ] Configure SQLAlchemy.
* [ ] Configure Alembic.

### Tables

* [ ] users
* [ ] projects
* [ ] experiments
* [ ] molecules
* [ ] evaluations
* [ ] agent_logs

### Repositories

* [ ] UserRepository
* [ ] ProjectRepository
* [ ] ExperimentRepository
* [ ] MoleculeRepository
* [ ] EvaluationRepository

### Migrations

* [ ] Create initial migration.
* [ ] Apply migration.
* [ ] Verify schema.

---

## Verification

Execute:

```bash
alembic upgrade head
```

Create:

```text
User
Project
Experiment
Molecule
Evaluation
```

using ORM.

All CRUD tests pass.

---

# PHASE 2 — Protein Processing Engine

## Goal

Implement target protein management.

---

## Pre-Requisites

Phase 1 completed.

---

## Task Checklist

### Models

* [ ] Protein schema.
* [ ] Protein metadata schema.

### Services

* [ ] ProteinService.
* [ ] ProteinValidationService.

### Targets

* [ ] KRAS.
* [ ] EGFR.
* [ ] APP.

### APIs

* [ ] GET proteins.
* [ ] GET protein details.

---

## Verification

Request:

```http
GET /proteins
```

Returns:

```json
[
  "KRAS",
  "EGFR",
  "APP"
]
```

All tests pass.

---

# PHASE 3 — Molecular Generation Engine (JTVAE)

## Goal

Generate valid molecular candidates.

---

## Pre-Requisites

Phase 2 completed.

---

## Task Checklist

### Data

* [ ] Download ZINC subset.
* [ ] Preprocess molecules.
* [ ] Generate SELFIES.

### JTVAE

* [ ] Encoder.
* [ ] Decoder.
* [ ] Latent sampler.

### Outputs

* [ ] SMILES generation.
* [ ] SELFIES generation.
* [ ] Latent embeddings.

### Persistence

* [ ] Store generated molecules.

---

## Verification

Generate:

```text
100 molecules
```

Validate:

```text
RDKit Validity > 90%
```

Store in database.

---

# PHASE 4 — Quantum-Inspired Sampling Layer

## Goal

Implement QCBM-inspired latent sampling.

---

## Pre-Requisites

Phase 3 completed.

---

## Task Checklist

### Sampling

* [ ] Latent vector extraction.
* [ ] QCBM simulation.
* [ ] Candidate selection.

### Metrics

* [ ] Diversity score.
* [ ] Novelty score.

### Storage

* [ ] Save sampled embeddings.

---

## Verification

Compare:

```text
Random Sampling
vs
QCBM Sampling
```

Verify diversity improvement.

---

# PHASE 5 — Molecular Property Evaluation

## Goal

Evaluate molecular quality.

---

## Pre-Requisites

Phase 4 completed.

---

## Task Checklist

### RDKit

* [ ] QED.
* [ ] SA Score.
* [ ] Lipinski.

### Chemprop

* [ ] Affinity predictor.

### Evaluation Service

* [ ] Evaluation pipeline.

### Persistence

* [ ] Save evaluations.

---

## Verification

Evaluate:

```text
100 molecules
```

Output:

```json
{
  "qed": 0.74,
  "sa": 0.68,
  "lipinski": true,
  "affinity": -8.1
}
```

for every molecule.

---

# PHASE 6 — NQRE (Patent Component #1)

## Goal

Implement reliability-aware molecular evaluation.

---

## Pre-Requisites

Phase 5 completed.

---

## Task Checklist

### Inputs

* [ ] Energy.
* [ ] Variance.
* [ ] Noise.
* [ ] Convergence.

### Scoring

* [ ] Reliability algorithm.
* [ ] Confidence algorithm.

### Logging

* [ ] Reliability trace.

### Persistence

* [ ] Save reliability scores.

---

## Verification

Every evaluated molecule contains:

```json
{
  "reliability_score": 0.89,
  "confidence_score": 0.91
}
```

No null values.

---

# PHASE 7 — Explainable Ranking Engine

## Goal

Rank molecules transparently.

---

## Pre-Requisites

Phase 6 completed.

---

## Task Checklist

### Ranking Formula

* [ ] QED weight.
* [ ] SA weight.
* [ ] Affinity weight.
* [ ] Reliability weight.

### Explanations

* [ ] Ranking reason.
* [ ] Ranking breakdown.

### Storage

* [ ] Ranking table.

---

## Verification

Generate:

```text
Top 20 molecules
```

Each includes:

```text
Rank
Score
Reason
Confidence
```

---

# PHASE 8 — AMDE (Patent Component #2)

## Goal

Implement autonomous optimization.

---

## Pre-Requisites

Phase 7 completed.

---

## Task Checklist

### ReAct Agent

* [ ] Observation.
* [ ] Reasoning.
* [ ] Decision.
* [ ] Action.

### Decision Types

* [ ] Refine.
* [ ] Regenerate.
* [ ] Terminate.

### Memory

* [ ] Optimization history.

### Logging

* [ ] Agent traces.

---

## Verification

Agent produces:

```json
{
  "decision": "refine",
  "reason": "...",
  "confidence": 0.84
}
```

for weak candidates.

---

# PHASE 9 — Closed-Loop Optimization

## Goal

Connect generation and refinement.

---

## Pre-Requisites

Phase 8 completed.

---

## Task Checklist

### Workflow

* [ ] Generate.
* [ ] Evaluate.
* [ ] Analyze.
* [ ] Refine.
* [ ] Regenerate.

### Iterations

* [ ] Configurable iterations.
* [ ] Stop criteria.

### Persistence

* [ ] Track optimization history.

---

## Verification

Run:

```text
5 optimization cycles
```

Observe improvement trend in:

```text
Affinity
QED
Reliability
```

---

# PHASE 10 — FastAPI Backend

## Goal

Expose platform functionality through APIs.

---

## Pre-Requisites

Phase 9 completed.

---

## Task Checklist

### Endpoints

* [ ] Projects.
* [ ] Experiments.
* [ ] Molecules.
* [ ] Rankings.

### Validation

* [ ] Pydantic models.

### Documentation

* [ ] OpenAPI.

---

## Verification

Swagger UI fully operational.

All endpoints tested.

---

# PHASE 11 — Authentication & Authorization

## Goal

Secure platform access.

---

## Pre-Requisites

Phase 10 completed.

---

## Task Checklist

* [ ] JWT verification.
* [ ] User management.
* [ ] Ownership validation.
* [ ] Role management.

---

## Verification

Unauthorized access returns:

```http
401
```

Forbidden access returns:

```http
403
```

---

# PHASE 12 — React Dashboard

## Goal

Build research visualization layer.

---

## Pre-Requisites

Phase 11 completed.

---

## Task Checklist

### UI

* [ ] Login.
* [ ] Projects.
* [ ] Experiments.

### Visualizations

* [ ] Molecule Viewer.
* [ ] Ranking Dashboard.
* [ ] Reliability Dashboard.
* [ ] Agent Trace Viewer.

---

## Verification

Complete workflow executable from browser.

---

# PHASE 13 — Queue System & Workers

## Goal

Move heavy computation off API threads.

---

## Pre-Requisites

Phase 12 completed.

---

## Task Checklist

* [ ] Redis.
* [ ] Celery.
* [ ] Generation Worker.
* [ ] Evaluation Worker.
* [ ] Quantum Worker.

---

## Verification

API remains responsive during long jobs.

---

# PHASE 14 — Experiment Tracking

## Goal

Enable reproducible research.

---

## Pre-Requisites

Phase 13 completed.

---

## Task Checklist

* [ ] Run IDs.
* [ ] Config snapshots.
* [ ] Dataset versions.
* [ ] Git commit tracking.

---

## Verification

Any experiment can be reproduced from stored metadata.

---

# PHASE 15 — Publication & Patent Readiness

## Goal

Prepare evidence for publication and patent filing.

---

## Pre-Requisites

All previous phases completed.

---

## Task Checklist

### Benchmarking

* [ ] Baseline comparison.
* [ ] Ablation study.
* [ ] Reliability analysis.

### Documentation

* [ ] Architecture diagrams.
* [ ] Experimental results.
* [ ] Patent draft artifacts.

### Deliverables

* [ ] Research paper.
* [ ] Patent specification.
* [ ] Demo video.

---

## Verification

System demonstrates:

1. Molecule generation.
2. Reliability scoring.
3. Agentic optimization.
4. Closed-loop improvement.
5. Explainable ranking.

Patentable contributions are reproducible and experimentally validated.
