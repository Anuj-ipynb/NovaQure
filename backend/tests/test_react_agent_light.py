"""
NovaQure — Lightweight ReAct Agent Verification

Tests the agent's data models and reasoning logic without importing
heavy dependencies (PyTorch, RDKit Contrib, etc.) that may not be
fully configured in all environments.

Run with: python -m backend.tests.test_react_agent_light
"""

from __future__ import annotations

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


# ------------------------------------------------------------------
# Test ReActTrace and ReActStep data models (no heavy imports)
# ------------------------------------------------------------------

def test_react_trace_dataclass():
    """Verify the ReActTrace and ReActStep data models work correctly."""
    # Direct import from the module file, bypassing __init__.py
    from backend.agents.react_agent import ReActStep, ReActTrace

    step = ReActStep(
        thought="Need to evaluate molecule",
        action="EvaluateMolecule",
        action_input='{"smiles": "CCO"}',
        observation='{"qed": 0.75}',
    )

    trace = ReActTrace(steps=[step], final_answer="Molecule accepted")
    d = trace.to_dict()

    assert len(d["steps"]) == 1
    assert d["steps"][0]["thought"] == "Need to evaluate molecule"
    assert d["steps"][0]["action"] == "EvaluateMolecule"
    assert d["final_answer"] == "Molecule accepted"
    print("[PASS] ReActTrace data model serialisation works")


def test_empty_trace():
    """Empty trace should serialise cleanly."""
    from backend.agents.react_agent import ReActTrace

    trace = ReActTrace()
    d = trace.to_dict()

    assert d["steps"] == []
    assert d["final_answer"] == ""
    print("[PASS] Empty ReActTrace serialisation works")


def test_trace_observation_truncation():
    """Long observations should be truncated to 500 chars."""
    from backend.agents.react_agent import ReActStep, ReActTrace

    long_obs = "x" * 1000
    step = ReActStep(
        thought="test",
        action="Test",
        action_input="{}",
        observation=long_obs,
    )
    trace = ReActTrace(steps=[step])
    d = trace.to_dict()

    assert len(d["steps"][0]["observation"]) == 500
    print("[PASS] Observation truncation works")


def test_langchain_agent_builder_fallback():
    """Agent builder should fall back to deterministic mode when no LLM is available."""

    # Ensure no LLM provider is configured
    old_provider = os.environ.get("LLM_PROVIDER", "")
    old_nvidia = os.environ.get("NVIDIA_API_KEY", "")
    os.environ["LLM_PROVIDER"] = "none"
    os.environ["NVIDIA_API_KEY"] = ""

    try:
        # Need to reload the config module to pick up the env changes
        import importlib
        import backend.configs.llm_config
        importlib.reload(backend.configs.llm_config)

        from backend.agents.react_agent import _try_build_langchain_agent

        result = _try_build_langchain_agent()
        assert result is None, "Should return None when LLM_PROVIDER is 'none'"
        print("[PASS] LangChain agent builder falls back correctly")
    finally:
        os.environ["LLM_PROVIDER"] = old_provider
        os.environ["NVIDIA_API_KEY"] = old_nvidia


if __name__ == "__main__":
    test_react_trace_dataclass()
    test_empty_trace()
    test_trace_observation_truncation()
    test_langchain_agent_builder_fallback()
    print("\n=== All lightweight agent tests passed ===")
