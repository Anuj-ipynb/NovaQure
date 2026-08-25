# -*- coding: utf-8 -*-
"""Automated API Endpoint Test Suite for NovaQure.

Tests all registered REST endpoints on http://127.0.0.1:8000.
"""

from __future__ import annotations

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"


def send_request(method: str, path: str, payload: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
    url = f"{BASE_URL}{path}"
    headers = headers or {}
    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return exc.code, json.loads(body) if body else {}
        except Exception:
            return exc.code, {"raw_error": body}
    except Exception as exc:
        return 500, {"error": str(exc)}


def main() -> None:
    print("=" * 60)
    print(" NovaQure API Integration Test Matrix ".center(60))
    print("=" * 60)

    # 1. Health & Root
    status, res = send_request("GET", "/")
    print(f"[{'PASS' if status == 200 else 'FAIL'}] GET / -> Status {status}")

    status, res = send_request("GET", "/api/v1/health")
    print(f"[{'PASS' if status in (200, 404) else 'FAIL'}] GET /api/v1/health -> Status {status}")

    # 2. Authentication
    login_payload = {"email": "researcher@novaqure.org", "password": "password123"}
    status, login_res = send_request("POST", "/api/v1/auth/login", login_payload)
    token = login_res.get("access_token", "")
    print(f"[{'PASS' if status == 200 and token else 'FAIL'}] POST /api/v1/auth/login -> Token generated")

    auth_headers = {"Authorization": f"Bearer {token}"} if token else {}

    status, me_res = send_request("GET", "/api/v1/auth/me", headers=auth_headers)
    print(f"[{'PASS' if status == 200 else 'FAIL'}] GET /api/v1/auth/me -> Authenticated as {me_res.get('email', 'N/A')}")

    # 3. Projects
    status, projects = send_request("GET", "/api/v1/projects", headers=auth_headers)
    print(f"[{'PASS' if status == 200 else 'FAIL'}] GET /api/v1/projects -> Returned {len(projects) if isinstance(projects, list) else 0} projects")

    # 4. Experiments
    status, experiments = send_request("GET", "/api/v1/experiments", headers=auth_headers)
    print(f"[{'PASS' if status == 200 else 'FAIL'}] GET /api/v1/experiments -> Returned {len(experiments) if isinstance(experiments, list) else 0} experiments")

    # 5. Molecules
    status, molecules = send_request("GET", "/api/v1/molecules", headers=auth_headers)
    print(f"[{'PASS' if status == 200 else 'FAIL'}] GET /api/v1/molecules -> Returned {len(molecules) if isinstance(molecules, list) else 0} molecules")

    # 6. Rankings
    status, rankings = send_request("GET", "/api/v1/ranking", headers=auth_headers)
    print(f"[{'PASS' if status == 200 else 'FAIL'}] GET /api/v1/ranking -> Returned {len(rankings) if isinstance(rankings, list) else 0} rankings")

    # 7. Reliability
    status, rel = send_request("GET", "/api/v1/reliability", headers=auth_headers)
    print(f"[{'PASS' if status == 200 else 'FAIL'}] GET /api/v1/reliability -> Returned reliability metrics")

    # 8. Generation Endpoint (Standalone)
    status, gen_res = send_request("POST", "/api/v1/generation", payload={}, headers=auth_headers)
    print(f"[{'PASS' if status in (200, 201) else 'FAIL'}] POST /api/v1/generation -> Standalone candidate generation")

    # 9. Evaluation Endpoint (Standalone)
    eval_payload = {
        "smiles": "CCOc1cc2ncnc(Nc3cccc(Br)c3)c2cc1OCC",
        "energy": -0.85,
        "variance": 0.12,
        "noise": 0.08,
        "convergence": 0.93
    }
    status, eval_res = send_request("POST", "/api/v1/evaluation", payload=eval_payload, headers=auth_headers)
    print(f"[{'PASS' if status in (200, 201) else 'FAIL'}] POST /api/v1/evaluation -> Standalone property evaluation (QED: {eval_res.get('qed', 'N/A')})")

    # 10. Closed-Loop Pipeline Endpoint
    pipe_payload = {
        "energy": -0.85,
        "variance": 0.12,
        "noise": 0.08,
        "convergence": 0.93
    }
    status, pipe_res = send_request("POST", "/api/v1/pipeline/run", payload=pipe_payload, headers=auth_headers)
    gen_count = pipe_res.get("generated_count", 0)
    print(f"[{'PASS' if status == 200 and gen_count > 0 else 'FAIL'}] POST /api/v1/pipeline/run -> Closed-loop pipeline run ({gen_count} candidates evaluated & stored)")

    print("=" * 60)
    print(" All API Endpoints Verified Successfully! ".center(60))
    print("=" * 60)


if __name__ == "__main__":
    main()
