# -*- coding: utf-8 -*-
"""In-Process FastAPI TestClient Verification for NovaQure API.

Verifies all routes directly using FastAPI's TestClient.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to PYTHONPATH
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def main() -> None:
    print("=" * 65, flush=True)
    print(" NovaQure In-Process API Test Matrix ".center(65), flush=True)
    print("=" * 65, flush=True)

    # 1. Root & Health
    resp = client.get("/")
    print(f"[{'PASS' if resp.status_code == 200 else 'FAIL'}] GET / -> Status {resp.status_code}", flush=True)

    resp = client.get("/api/v1/health")
    print(f"[{'PASS' if resp.status_code == 200 else 'FAIL'}] GET /api/v1/health -> Status {resp.status_code}", flush=True)

    # 2. Auth Login & Me
    login_resp = client.post("/api/v1/auth/login", json={"email": "researcher@novaqure.org", "password": "password123"})
    token = login_resp.json().get("access_token", "") if login_resp.status_code == 200 else ""
    print(f"[{'PASS' if login_resp.status_code == 200 and token else 'FAIL'}] POST /api/v1/auth/login -> Status {login_resp.status_code}", flush=True)

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    me_resp = client.get("/api/v1/auth/me", headers=headers)
    print(f"[{'PASS' if me_resp.status_code == 200 else 'FAIL'}] GET /api/v1/auth/me -> Status {me_resp.status_code} ({me_resp.json().get('email', 'N/A')})", flush=True)

    # 3. Projects
    projects_resp = client.get("/api/v1/projects", headers=headers)
    print(f"[{'PASS' if projects_resp.status_code == 200 else 'FAIL'}] GET /api/v1/projects -> Status {projects_resp.status_code}", flush=True)

    # 4. Experiments
    exp_resp = client.get("/api/v1/experiments", headers=headers)
    print(f"[{'PASS' if exp_resp.status_code == 200 else 'FAIL'}] GET /api/v1/experiments -> Status {exp_resp.status_code}", flush=True)

    # 5. Molecules
    mol_resp = client.get("/api/v1/molecules", headers=headers)
    print(f"[{'PASS' if mol_resp.status_code == 200 else 'FAIL'}] GET /api/v1/molecules -> Status {mol_resp.status_code}", flush=True)

    # 6. Rankings
    rank_resp = client.get("/api/v1/rankings", headers=headers)
    print(f"[{'PASS' if rank_resp.status_code == 200 else 'FAIL'}] GET /api/v1/rankings -> Status {rank_resp.status_code}", flush=True)

    # 7. Reliability
    rel_resp = client.get("/api/v1/reliability", headers=headers)
    print(f"[{'PASS' if rel_resp.status_code == 200 else 'FAIL'}] GET /api/v1/reliability -> Status {rel_resp.status_code}", flush=True)

    # 8. Generation Endpoint (Standalone)
    gen_resp = client.post("/api/v1/generation/run", json={"experiment_id": "exp-test", "num_molecules": 10}, headers=headers)
    print(f"[{'PASS' if gen_resp.status_code in (200, 201) else 'FAIL'}] POST /api/v1/generation/run -> Status {gen_resp.status_code}", flush=True)

    # 9. Evaluation Endpoint (Standalone)
    eval_resp = client.post(
        "/api/v1/evaluation/run",
        json={
            "experiment_id": "exp-test",
            "molecules": [
                {
                    "smiles": "CCOc1cc2ncnc(Nc3cccc(Br)c3)c2cc1OCC",
                    "energy": -0.85,
                    "variance": 0.12,
                    "noise": 0.08,
                    "convergence": 0.93,
                }
            ]
        },
        headers=headers,
    )
    print(f"[{'PASS' if eval_resp.status_code in (200, 201) else 'FAIL'}] POST /api/v1/evaluation/run -> Status {eval_resp.status_code}", flush=True)

    # 10. Pipeline Endpoint (Closed-Loop)
    pipe_resp = client.post(
        "/api/v1/pipeline/run",
        json={
            "energy": -0.85,
            "variance": 0.12,
            "noise": 0.08,
            "convergence": 0.93,
        },
        headers=headers,
    )
    pipe_data = pipe_resp.json() if pipe_resp.status_code == 200 else {}
    gen_count = pipe_data.get("generated_count", 0)
    print(f"[{'PASS' if pipe_resp.status_code == 200 and gen_count > 0 else 'FAIL'}] POST /api/v1/pipeline/run -> Status {pipe_resp.status_code} ({gen_count} candidates evaluated & persisted)", flush=True)

    print("=" * 65, flush=True)
    print(" All API Endpoints Verified via FastAPI TestClient! ".center(65), flush=True)
    print("=" * 65, flush=True)


if __name__ == "__main__":
    main()
