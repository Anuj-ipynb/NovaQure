# NovaQure API Specification

Version: 1.0

Status: Draft

---

# API Design Principles

All APIs follow:

```text
REST
JSON
JWT Authentication
Versioned Endpoints
```

Base URL:

```text
/api/v1
```

Response Format:

```json
{
  "success": true,
  "data": {}
}
```

Error Format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

---

# Health Endpoints

## GET /health

Purpose:

System health check.

Response:

```json
{
  "status": "healthy"
}
```

---

# Authentication APIs

## POST /auth/register

Request

```json
{
  "email": "user@example.com",
  "password": "password",
  "full_name": "Researcher"
}
```

Response

```json
{
  "user_id": "uuid"
}
```

---

## POST /auth/login

Request

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Response

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

---

# Project APIs

## POST /projects

Create project.

Request

```json
{
  "name": "KRAS Discovery",
  "description": "Drug discovery experiment"
}
```

Response

```json
{
  "project_id": "uuid"
}
```

---

## GET /projects

Returns all projects owned by current user.

Response

```json
[
  {
    "project_id": "uuid",
    "name": "KRAS Discovery"
  }
]
```

---

## GET /projects/{project_id}

Returns project details.

---

# Experiment APIs

## POST /experiments

Create experiment.

Request

```json
{
  "project_id": "uuid",
  "target_protein": "KRAS",
  "iterations": 5
}
```

Response

```json
{
  "experiment_id": "uuid",
  "status": "queued"
}
```

---

## GET /experiments/{experiment_id}

Returns experiment metadata.

Response

```json
{
  "experiment_id": "uuid",
  "status": "running",
  "target_protein": "KRAS"
}
```

---

## GET /experiments/{experiment_id}/status

Response

```json
{
  "status": "completed",
  "progress": 100
}
```

---

# Protein APIs

## GET /proteins

Response

```json
[
  "KRAS",
  "EGFR",
  "APP"
]
```

---

## GET /proteins/{protein_name}

Response

```json
{
  "protein": "KRAS",
  "description": "...",
  "disease_context": "Cancer"
}
```

---

# Molecular Generation APIs

## POST /generation/generate

Purpose:

Generate candidate molecules.

Request

```json
{
  "experiment_id": "uuid",
  "num_molecules": 100
}
```

Response

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

---

## GET /generation/{job_id}

Response

```json
{
  "status": "completed",
  "generated_count": 100
}
```

---

# Molecule APIs

## GET /molecules

Query Parameters

```text
experiment_id
limit
offset
```

Response

```json
[
  {
    "molecule_id": "uuid",
    "smiles": "CCO"
  }
]
```

---

## GET /molecules/{molecule_id}

Response

```json
{
  "molecule_id": "uuid",
  "smiles": "CCO",
  "selfies": "[C][C][O]"
}
```

---

# Evaluation APIs

## POST /evaluation/run

Purpose:

Run RDKit and Chemprop evaluation.

Request

```json
{
  "experiment_id": "uuid"
}
```

Response

```json
{
  "job_id": "uuid"
}
```

---

## GET /evaluation/{molecule_id}

Response

```json
{
  "qed": 0.82,
  "sa_score": 0.71,
  "lipinski_pass": true,
  "binding_affinity": -8.2
}
```

---

# AQKC APIs

## POST /aqkc/run

Purpose:

Run Adaptive Quantum Kernel Controller.

Request

```json
{
  "experiment_id": "uuid"
}
```

Response

```json
{
  "job_id": "uuid"
}
```

---

## GET /aqkc/{molecule_id}

Response

```json
{
  "corrected_energy": -1.23,
  "noise_score": 0.15
}
```

---

# NQRE APIs

## POST /nqre/run

Purpose:

Compute reliability metrics.

Request

```json
{
  "experiment_id": "uuid"
}
```

Response

```json
{
  "job_id": "uuid"
}
```

---

## GET /nqre/{molecule_id}

Response

```json
{
  "reliability_score": 0.91,
  "confidence_score": 0.88
}
```

---

# Ranking APIs

## POST /ranking/run

Purpose:

Generate explainable rankings.

Request

```json
{
  "experiment_id": "uuid"
}
```

Response

```json
{
  "job_id": "uuid"
}
```

---

## GET /ranking/{experiment_id}

Response

```json
[
  {
    "rank": 1,
    "molecule_id": "uuid",
    "score": 92.4,
    "confidence": 0.91
  }
]
```

---

# AMDE APIs

## POST /amde/analyze

Purpose:

Analyze candidates and determine next action.

Request

```json
{
  "experiment_id": "uuid"
}
```

Response

```json
{
  "decision": "refine",
  "confidence": 0.87
}
```

---

## GET /amde/{experiment_id}/trace

Response

```json
[
  {
    "step": 1,
    "decision": "refine",
    "reason": "Low affinity"
  }
]
```

---

# Optimization APIs

## POST /optimization/run

Purpose:

Execute complete NovaQure pipeline.

Workflow:

```text
Generate
↓
Evaluate
↓
AQKC
↓
NQRE
↓
Rank
↓
AMDE
↓
Refine
```

Request

```json
{
  "experiment_id": "uuid",
  "iterations": 5
}
```

Response

```json
{
  "job_id": "uuid"
}
```

---

## GET /optimization/{experiment_id}

Response

```json
{
  "current_iteration": 3,
  "best_score": 94.2,
  "status": "running"
}
```

---

# Dashboard APIs

## GET /dashboard/{experiment_id}

Response

```json
{
  "generated_molecules": 100,
  "evaluated_molecules": 100,
  "top_score": 94.2,
  "best_reliability": 0.95
}
```

---

# WebSocket Events

## /ws/experiments/{experiment_id}

Events:

```json
{
  "event": "generation_completed"
}
```

```json
{
  "event": "evaluation_completed"
}
```

```json
{
  "event": "ranking_completed"
}
```

```json
{
  "event": "optimization_completed"
}
```

---

# Ownership Matrix

| Module       | Owner             |
| ------------ | ----------------- |
| Auth         | Platform Lead     |
| Projects     | Platform Lead     |
| Proteins     | Platform Lead     |
| Generation   | Generation Lead   |
| Evaluation   | Evaluation Lead   |
| AQKC         | Evaluation Lead   |
| NQRE         | Evaluation Lead   |
| Ranking      | Optimization Lead |
| AMDE         | Optimization Lead |
| Optimization | Optimization Lead |
| Dashboard    | Platform Lead     |

---

# API Versioning

Current:

```text
/api/v1
```

Future:

```text
/api/v2
```

No breaking changes are allowed inside the same API version.
