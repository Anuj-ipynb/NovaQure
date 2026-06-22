# architecture.md

# NovaQure System Architecture

**Project:** NovaQure — Noise-Adaptive Hybrid AI–Quantum Framework for Intelligent Drug Discovery

**Version:** 1.0

**Architecture Owner:** NovaQure Engineering Team

---

# 1. High-Level Architecture Pattern

## Selected Pattern

### Modular Monolith + Event-Driven Processing

```text
React Frontend
        │
        ▼
 FastAPI Gateway
        │
 ┌──────┼──────┐
 │      │      │
 ▼      ▼      ▼

Auth  Project  Experiment
Module Module   Module

 │
 ▼

AI–Quantum Engine

 ├── Protein Engine
 ├── Generation Engine
 ├── Sampling Engine
 ├── Evaluation Engine
 ├── NQRE Engine
 ├── AMDE Agent Engine
 └── Ranking Engine

        │
        ▼

PostgreSQL + Redis

        │
        ▼

Background Workers
```

---

## Why Not Microservices Initially?

Microservices would introduce:

* Service discovery
* Distributed tracing
* Network latency
* Operational complexity
* DevOps overhead

without delivering significant value for:

* academic research,
* single-team development,
* limited user scale.

---

> ADR-001
>
> NovaQure shall be implemented as a Modular Monolith in Version 1.
>
> All modules must communicate through internal interfaces rather than direct imports.
>
> This enables future migration into independently deployable microservices.

---

## Future Evolution

### Phase 1

```text
Local Research Platform
```

### Phase 2

```text
Multi-User Research Platform
```

### Phase 3

```text
Service-Oriented Architecture
```

### Phase 4

```text
Cloud Native Microservices
```

---

# 2. Tech Stack Selection

---

## Frontend

### Technology

```text
React
TypeScript
TailwindCSS
TanStack Query
3Dmol.js
Plotly.js
```

### Justification

| Technology     | Reason                    |
| -------------- | ------------------------- |
| React          | Large ecosystem           |
| TypeScript     | Type safety               |
| TailwindCSS    | Rapid UI development      |
| TanStack Query | API state management      |
| Plotly         | Scientific visualizations |
| 3Dmol.js       | Molecular visualization   |

---

## Backend

### Technology

```text
FastAPI
Python 3.12
Pydantic
SQLAlchemy
Alembic
```

### Justification

| Technology | Reason                      |
| ---------- | --------------------------- |
| FastAPI    | High-performance async APIs |
| Python     | Native AI ecosystem         |
| Pydantic   | Validation                  |
| SQLAlchemy | ORM flexibility             |
| Alembic    | Database migrations         |

---

## AI/Quantum Layer

```text
PyTorch
RDKit
Chemprop
PennyLane
NumPy
SciPy
LangChain
```

### Justification

Supports:

* JTVAE
* QCBM-inspired sampling
* VQE simulation
* Reliability scoring
* ReAct optimization loop

---

## Database

### Primary

```text
PostgreSQL
```

### Justification

Supports:

* ACID transactions
* JSON storage
* indexing
* scalability

---

> ADR-002
>
> PostgreSQL is the source of truth.
>
> No business-critical data shall be stored exclusively in cache.

---

## Caching Layer

### Technology

```text
Redis
```

### Responsibilities

* Session caching
* Experiment state caching
* Agent memory caching
* Queue backend

---

## Queue System

### Technology

```text
Celery
Redis Broker
```

### Worker Types

```text
Generation Worker
Evaluation Worker
Quantum Worker
Optimization Worker
Report Worker
```

---

> ADR-003
>
> Long-running AI and quantum computations must never execute in API request threads.

---

# 3. Authentication & Authorization Strategy

## Selected Provider

### Supabase Auth

---

## Why Supabase?

Provides:

* JWT authentication
* OAuth support
* User management
* Role support
* PostgreSQL integration

without maintaining custom auth infrastructure.

---

## Authentication Flow

```text
User Login
      │
      ▼

Supabase Auth

      │
      ▼

JWT Token Issued

      │
      ▼

Frontend Stores Token

      │
      ▼

API Requests

      │
      ▼

FastAPI JWT Verification

      │
      ▼

Authorized Resource Access
```

---

## Authorization Model

### Role-Based Access Control

Roles:

```text
Researcher
Admin
System
```

---

## Permission Matrix

| Resource        | Researcher | Admin |
| --------------- | ---------- | ----- |
| Own Projects    | Yes        | Yes   |
| Own Experiments | Yes        | Yes   |
| User Management | No         | Yes   |
| System Settings | No         | Yes   |

---

> ADR-004
>
> Authorization decisions must occur server-side.
>
> Frontend role checks are UI convenience only.

---

# 4. Data Flow & System Boundaries

---

## High-Level Request Flow

```text
Browser
   │
   ▼

React Frontend

   │ HTTPS
   ▼

FastAPI API Layer

   │
   ▼

Business Services

   │
   ▼

PostgreSQL
Redis
Workers
```

---

## Molecule Discovery Flow

```text
User Selects Protein
        │
        ▼

Protein Engine

        │
        ▼

Generation Engine
(JTVAE)

        │
        ▼

QCBM Sampling

        │
        ▼

Candidate Molecules

        │
        ▼

Property Evaluation

        │
        ▼

NQRE Reliability

        │
        ▼

AMDE Agent Analysis

        │
        ▼

Refinement Decision

        │
        ▼

Regenerate OR Rank

        │
        ▼

Dashboard
```

---

## External Systems

### Protein Data Bank

```text
PDB API
```

Purpose:

* Protein metadata
* Structure retrieval

---

### Future Integrations

```text
ChEMBL
BindingDB
PubChem
DrugBank
```

---

## Webhook Architecture

```text
Worker Completes Job
        │
        ▼

Event Published

        │
        ▼

Frontend Notification

        │
        ▼

Dashboard Update
```

---

# 5. Scale & Performance Guardrails

---

## Load Balancing

### Production

```text
NGINX
AWS Application Load Balancer
```

---

## Rate Limiting

### FastAPI Middleware

Limits:

```text
100 requests/minute/user
```

Special endpoints:

```text
Experiment Creation:
10 requests/minute
```

---

> ADR-005
>
> AI computation endpoints shall always have stricter limits than standard API endpoints.

---

## Database Bottleneck Prevention

### Connection Pooling

```text
PgBouncer
```

Target:

```text
Max Pool Size: 50
```

---

## Indexing Strategy

Mandatory indexes:

```sql
users.id
projects.id
experiments.id
molecules.id
evaluations.id
```

Composite indexes:

```sql
(project_id, created_at)
(experiment_id, molecule_id)
```

---

## Query Optimization

Rules:

* Avoid N+1 queries
* Use pagination
* Use projections
* Cache expensive reads

---

## Storage Strategy

Store separately:

```text
Structured Data → PostgreSQL

Large Artifacts →
Object Storage
```

Examples:

```text
Molecule Images
Reports
Logs
Model Outputs
```

---

## Async Execution

Never execute:

```text
JTVAE Generation
VQE Simulation
Optimization Loops
```

inside request threads.

Always:

```text
API
 ↓
Queue
 ↓
Worker
 ↓
Database
```

---

# 6. Infrastructure & Deployment Pipeline

---

## Development Environment

```text
Docker Compose
```

Services:

```text
frontend
backend
postgres
redis
worker
```

---

## Cloud Platform

### AWS

Primary Services:

| Service           | Purpose    |
| ----------------- | ---------- |
| ECS Fargate       | Containers |
| RDS PostgreSQL    | Database   |
| ElastiCache Redis | Cache      |
| S3                | Storage    |
| CloudWatch        | Monitoring |

---

## Container Strategy

All services containerized.

```text
Frontend Container
Backend Container
Worker Container
```

---

## CI/CD Pipeline

### GitHub Actions

Workflow:

```text
Push
 │
 ▼

Lint

 │
 ▼

Unit Tests

 │
 ▼

Integration Tests

 │
 ▼

Build Docker Images

 │
 ▼

Deploy Staging

 │
 ▼

Deploy Production
```

---

## Environment Separation

```text
Local
Development
Staging
Production
```

Each environment must have:

```text
Independent Database
Independent Redis
Independent Secrets
```

---

## Monitoring Stack

### Observability

```text
Prometheus
Grafana
CloudWatch
```

Metrics:

* API latency
* Queue depth
* Job success rate
* Experiment completion rate
* Database load

---

# Final Architecture Principle

NovaQure is designed as a modular, reliability-first AI–Quantum research platform where every computational component can be replaced, upgraded, or scaled independently without requiring system-wide redesign.

The architecture prioritizes:

1. Scientific reproducibility.
2. Explainability.
3. Reliability-aware evaluation.
4. Iterative molecular optimization.
5. Future cloud scalability.
6. Patent-oriented extensibility.
