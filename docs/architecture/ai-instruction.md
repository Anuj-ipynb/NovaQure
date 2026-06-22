# AI Instructions - NovaQure

## Project Overview

NovaQure is a modular AI–Quantum Drug Discovery Platform focused on:

* Molecular Generation
* Quantum-Inspired Evaluation
* Reliability-Aware Scoring (NQRE)
* Agentic Optimization (AMDE)
* Explainable Molecular Ranking
* Research Reproducibility

The platform follows a strict iterative workflow:

```text
Generate
→ Evaluate
→ Analyze
→ Refine
→ Regenerate
```

Never design one-shot pipelines.

Every implementation must support future iterative optimization.

---

# Tech Stack Constraints

## Frontend

Allowed:

```text
React 19+
TypeScript
Vite
TailwindCSS
TanStack Query
React Hook Form
Zod
Plotly.js
3Dmol.js
```

Forbidden:

```text
Bootstrap
Material UI
jQuery
Redux
MobX
Class Components
```

Requirements:

* Functional components only
* TypeScript strict mode
* Tailwind utility-first styling
* No inline styles
* No CSS frameworks other than Tailwind

---

## Backend

Allowed:

```text
Python 3.12
FastAPI
Pydantic v2
SQLAlchemy 2.x
Alembic
```

Forbidden:

```text
Flask
Django
FastAPI sync endpoints
```

Requirements:

* Async-first APIs
* Dependency Injection
* Pydantic request/response models
* Service layer abstraction

---

## Database

Development:

```text
SQLite
```

Production:

```text
PostgreSQL
```

Never:

```text
MongoDB
Firebase
Supabase Database
```

PostgreSQL is the source of truth.

---

## Queue & Workers

Allowed:

```text
Celery
Redis
```

Forbidden:

```text
Background tasks inside API requests
Long-running synchronous jobs
```

Every expensive task must run through workers.

---

## AI Stack

Allowed:

```text
PyTorch
RDKit
Chemprop
PennyLane
NumPy
SciPy
SELFIES
LangChain
```

Forbidden:

```text
TensorFlow
Keras
AutoML tools
Black-box proprietary chemistry APIs
```

---

# Architecture Rules

Follow Modular Monolith architecture.

Current modules:

```text
auth/
projects/
proteins/
generation/
sampling/
evaluation/
nqre/
amde/
ranking/
visualization/
```

Never directly couple modules.

Communication must occur through:

```python
Service Layer
Repository Layer
DTOs
```

Never import internal database models across modules.

---

# Directory Structure

Required structure:

```text
backend/

├── api/
├── core/
├── database/
├── auth/
├── projects/
├── proteins/
├── generation/
├── sampling/
├── evaluation/
├── nqre/
├── amde/
├── ranking/
├── workers/
├── services/
├── schemas/
├── repositories/
└── tests/
```

Do not create arbitrary folders.

---

# Code Style Rules

## General

Prefer:

```python
pure functions
small functions
dependency injection
composition
```

Avoid:

```python
global state
singletons
god classes
utility dumping grounds
```

---

## Function Size

Target:

```text
10-30 lines
```

Maximum:

```text
50 lines
```

---

## Class Size

Target:

```text
100-200 lines
```

Refactor larger classes.

---

## Naming

Use explicit names.

Good:

```python
calculate_reliability_score()
generate_molecule_batch()
evaluate_binding_affinity()
```

Bad:

```python
process()
handle()
run()
```

---

# Frontend Design Rules

Use:

```text
Container Components
Presentational Components
Custom Hooks
```

Pattern:

```text
UI Components
↓
Hooks
↓
API Layer
↓
Backend
```

Never:

```text
Fetch directly inside UI components
Business logic inside JSX
```

---

## Component Structure

```text
components/
hooks/
services/
types/
pages/
```

Keep concerns separated.

---

# Backend Design Rules

Use:

```python
Router
↓
Service
↓
Repository
↓
Database
```

Never:

```python
Router → Database
```

directly.

---

# Error Handling Paradigm

## API Layer

All endpoints must:

```python
try:
    ...
except DomainException:
    ...
except Exception:
    ...
```

Return structured errors.

Required format:

```json
{
  "error": true,
  "code": "MOLECULE_GENERATION_FAILED",
  "message": "Generation process failed"
}
```

Never return:

```python
str(exception)
```

to clients.

---

## Custom Exceptions

Use domain exceptions:

```python
ProteinNotFoundException
MoleculeGenerationException
EvaluationException
ReliabilityCalculationException
```

Avoid generic exceptions.

---

## Logging

Use structured logging.

Required:

```python
logger.info()
logger.warning()
logger.error()
```

Include:

```text
experiment_id
run_id
module_name
execution_time
```

Never use:

```python
print()
```

---

## Global Error Middleware

Must exist.

Responsibilities:

* capture unhandled exceptions
* log stack traces
* return safe responses

---

# Security Guardrails

## Authentication

Use:

```text
Supabase Auth
JWT
```

Every protected endpoint must verify:

```python
user_id
role
project ownership
```

before accessing data.

---

## Authorization

Always check:

```python
current_user.id == resource.owner_id
```

or:

```python
role == admin
```

Never trust frontend authorization.

---

## Environment Variables

Allowed:

```python
os.getenv()
pydantic-settings
```

Forbidden:

```python
hardcoded secrets
API keys in source code
```

Secrets must only exist in:

```text
.env
AWS Secrets Manager
GitHub Secrets
```

---

## Input Validation

Validate all input using:

```python
Pydantic
Zod
```

Never trust:

```text
query params
request bodies
uploaded files
```

without validation.

---

## File Upload Rules

Always:

* validate file type
* validate file size
* sanitize file names

Never execute uploaded content.

---

# Database Rules

Use:

```python
SQLAlchemy ORM
Alembic Migrations
```

Never:

```python
raw SQL everywhere
```

Indexes required on:

```text
foreign keys
status fields
created_at
experiment_id
project_id
```

Soft-delete records using:

```text
deleted_at
```

Never permanently delete research data.

---

# Testing Rules

Minimum:

```text
Unit Tests
Integration Tests
```

Required coverage:

```text
80%
```

Every service requires tests.

---

# NQRE Rules

NQRE is a primary research contribution.

Any modifications must preserve:

Inputs:

```text
Energy
Variance
Noise
Convergence
```

Outputs:

```text
Reliability Score
Confidence Score
```

Do not replace with simplistic averages.

Maintain explainability.

---

# AMDE Rules

AMDE is a primary research contribution.

Every decision must produce:

```json
{
  "decision": "",
  "reason": "",
  "confidence": 0.0
}
```

No black-box decisions.

All actions must be traceable.

---

# Output Preferences For AI Assistant

Always:

* Generate complete code.
* Provide production-ready implementations.
* Include imports.
* Include type hints.
* Include error handling.
* Include tests when relevant.

Avoid:

* TODO comments
* Placeholder implementations
* Pseudocode
* Incomplete snippets

When multiple approaches exist:

1. Recommend one approach.
2. Briefly explain trade-offs.
3. Implement the recommended solution.

Keep explanations concise.

Prioritize maintainability, reproducibility, explainability, and modularity over cleverness.

---

# Core Principle

Every contribution to NovaQure must improve at least one of:

* Reliability
* Reproducibility
* Explainability
* Modularity
* Scalability
* Scientific Validity

If a change does not improve one of these dimensions, redesign it.
