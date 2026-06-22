# NovaQure Optimization Lead

## Mission

Build ranking, explainability, AMDE, and closed-loop optimization.

---

## You Own

```text
backend/ranking/
backend/amde/
backend/orchestrator/
```

---

## Branch

```bash
git checkout -b feature/optimization
```

---

## Phase 1

Ranking Engine.

Implement:

```text
ranking_service.py
```

Input:

```json
{
  "qed":0.8,
  "sa":0.7,
  "affinity":-8.2,
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

## Phase 2

AMDE.

Implement:

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

## Phase 3

Optimization Loop.

Implement:

```text
optimization_pipeline.py
```

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

---

## Integration Input

```text
reliability_scores.json
```

---

## Integration Output

```text
rankings.json
agent_decisions.json
```

---

## Verification

Run:

```text
5 optimization cycles
```

Show improvement trend.

---

## Definition of Done

* Explainable ranking
* Explainable decisions
* Optimization memory
* Tests pass


## MASTER PROMPT FOR IMPLEMENTATION
You are the Lead Optimization Engineer for NovaQure.

Context:

NovaQure is not a one-shot generator.

Pipeline:

Generate
↓
Evaluate
↓
Analyze
↓
Refine
↓
Regenerate

You own:

* Explainable Ranking Engine
* AMDE
* ReAct Agent
* Optimization Loop
* Decision Trace System

Requirements:

1. Every decision must be explainable.
2. Every optimization cycle must be logged.
3. No black-box ranking.
4. No hidden agent state.

Tasks:

Step 1:
Implement ranking engine.

Inputs:

* QED
* SA
* Affinity
* Reliability

Outputs:

* Final Score
* Rank

Deliver:

* ranking_service.py

Step 2:
Implement explanation engine.

Deliver:

* explanation_service.py

Output:

{
"reason": "...",
"score_breakdown": {}
}

Step 3:
Implement AMDE.

Deliver:

* amde_service.py

Outputs:

{
"decision": "refine",
"reason": "...",
"confidence": 0.85
}

Step 4:
Implement optimization memory.

Deliver:

* optimization_history.py

Step 5:
Implement closed-loop orchestrator.

Deliver:

* optimization_pipeline.py

Provide:

* architecture
* code
* tests
* integration instructions

Always generate complete implementations.
Never generate placeholders.
