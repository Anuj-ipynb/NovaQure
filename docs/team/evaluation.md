## MASTER PROMPT FOR IMPLEMENTATION
You are the Lead Quantum Evaluation Engineer for NovaQure.

Context:

NovaQure performs molecular evaluation after generation.

Pipeline:

Molecule
↓
RDKit
↓
Chemprop
↓
AQKC
↓
NQRE
↓
Ranking

You own:

* Evaluation Engine
* RDKit Metrics
* Chemprop Integration
* AQKC
* NQRE

Requirements:

1. Use Python 3.12.
2. Follow Service Layer architecture.
3. Every calculation must be explainable.
4. Reliability outputs must be traceable.
5. No hardcoded values.

Tasks:

Step 1:
Implement RDKit scoring.

Deliver:

* qed_service.py
* lipinski_service.py
* sa_service.py

Step 2:
Implement evaluation aggregator.

Deliver:

* evaluation_service.py

Output:

{
"qed": float,
"sa": float,
"lipinski": bool
}

Step 3:
Implement Chemprop integration.

Deliver:

* affinity_service.py

Step 4:
Design AQKC.

Inputs:

* Energy
* Variance
* Noise

Outputs:

* Corrected Energy
* Noise Score

Deliver:

* aqkc_service.py
* aqkc_config.py

Step 5:
Design NQRE.

Inputs:

* Corrected Energy
* Variance
* Noise
* Convergence

Outputs:

* Reliability Score
* Confidence Score

Deliver:

* nqre_service.py

Output:

{
"reliability_score": float,
"confidence_score": float
}

Provide:

* formulas
* assumptions
* code
* tests
* integration hooks

Do not simplify AQKC or NQRE.
Preserve scientific explainability.


# NovaQure Evaluation Lead

## Mission

Evaluate molecules and compute reliability-aware quantum metrics.

---

## You Own

```text
backend/evaluation/
backend/aqkc/
backend/nqre/
```

---

## Branch

```bash
git checkout -b feature/evaluation
```

---

## Phase 1

Implement RDKit scoring.

Files:

```text
qed_service.py
sa_service.py
lipinski_service.py
```

---

## Phase 2

Implement affinity prediction.

Files:

```text
affinity_service.py
```

---

## Phase 3

Implement AQKC.

Inputs:

```text
Energy
Variance
Noise
```

Outputs:

```json
{
  "corrected_energy": -1.23,
  "noise_score": 0.14
}
```

---

## Phase 4

Implement NQRE.

Outputs:

```json
{
  "reliability_score": 0.91,
  "confidence_score": 0.88
}
```

---

## Integration Input

```text
generated_molecules.json
```

---

## Integration Output

```text
evaluations.json
reliability_scores.json
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

## Definition of Done

* Tests pass
* AQKC documented
* NQRE documented
* JSON output valid
* Contract respected
