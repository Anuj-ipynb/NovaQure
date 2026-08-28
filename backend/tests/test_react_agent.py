"""
NovaQure — ReAct Agent Unit Tests

Tests the LangChain tool wrappers, deterministic agent execution,
and full orchestrator loop without requiring an external LLM.
"""

from __future__ import annotations

import json
import pytest

from backend.agents.react_tools import build_react_tools
from backend.agents.react_agent import (
    build_agent,
    DeterministicReActAgent,
    ReActStep,
    ReActTrace,
)


# ------------------------------------------------------------------
# Tool Construction
# ------------------------------------------------------------------

class TestReActTools:
    """Verify that all four LangChain tools are constructed correctly."""

    def test_tool_count(self):
        tools = build_react_tools()
        assert len(tools) == 4

    def test_tool_names(self):
        tools = build_react_tools()
        names = {t.name for t in tools}
        assert names == {
            "EvaluateMolecule",
            "MutateMolecule",
            "RankCandidates",
            "ExplainMolecule",
        }

    def test_all_tools_callable(self):
        tools = build_react_tools()
        for tool in tools:
            assert callable(tool.func)


# ------------------------------------------------------------------
# Deterministic Agent
# ------------------------------------------------------------------

class TestDeterministicAgent:
    """Validate the deterministic fallback ReAct agent."""

    SAMPLE_SMILES = "c1ccccc1"    # benzene
    SAMPLE_SELFIES = "[C][=C][C][=C][C][=C][Ring1][=Branch1]"

    def test_agent_construction(self):
        agent = build_agent()
        assert isinstance(agent, DeterministicReActAgent)

    def test_agent_run_returns_dict(self):
        agent = build_agent()
        result = agent.run(
            smiles=self.SAMPLE_SMILES,
            selfies=self.SAMPLE_SELFIES,
            molecule_id="test-mol-001",
        )
        assert isinstance(result, dict)

    def test_agent_result_has_required_keys(self):
        agent = build_agent()
        result = agent.run(
            smiles=self.SAMPLE_SMILES,
            selfies=self.SAMPLE_SELFIES,
            molecule_id="test-mol-002",
        )
        required_keys = {
            "molecule_id",
            "smiles",
            "selfies",
            "decision",
            "reason",
            "evaluation",
            "explanation",
            "react_trace",
        }
        assert required_keys.issubset(result.keys())

    def test_decision_is_valid(self):
        agent = build_agent()
        result = agent.run(
            smiles=self.SAMPLE_SMILES,
            selfies=self.SAMPLE_SELFIES,
            molecule_id="test-mol-003",
        )
        assert result["decision"] in ("keep", "refine", "regenerate")

    def test_trace_has_steps(self):
        agent = build_agent()
        result = agent.run(
            smiles=self.SAMPLE_SMILES,
            selfies=self.SAMPLE_SELFIES,
            molecule_id="test-mol-004",
        )
        trace = result["react_trace"]
        assert "steps" in trace
        # Should have at least Evaluate + Decision + Explain = 3 steps
        assert len(trace["steps"]) >= 3

    def test_trace_step_structure(self):
        agent = build_agent()
        result = agent.run(
            smiles=self.SAMPLE_SMILES,
            selfies=self.SAMPLE_SELFIES,
            molecule_id="test-mol-005",
        )
        for step in result["react_trace"]["steps"]:
            assert "thought" in step
            assert "action" in step
            assert "observation" in step

    def test_evaluation_contains_metrics(self):
        agent = build_agent()
        result = agent.run(
            smiles=self.SAMPLE_SMILES,
            selfies=self.SAMPLE_SELFIES,
            molecule_id="test-mol-006",
        )
        eval_data = result["evaluation"]
        expected_metrics = ["qed", "sa_score", "reliability_score", "confidence_score"]
        for metric in expected_metrics:
            assert metric in eval_data, f"Missing metric: {metric}"


# ------------------------------------------------------------------
# ReActTrace Model
# ------------------------------------------------------------------

class TestReActTrace:
    """Unit tests for the ReActTrace data model."""

    def test_empty_trace_serializes(self):
        trace = ReActTrace()
        d = trace.to_dict()
        assert d["steps"] == []
        assert d["final_answer"] == ""

    def test_trace_with_step(self):
        step = ReActStep(
            thought="test thought",
            action="TestAction",
            action_input="{}",
            observation="result",
        )
        trace = ReActTrace(steps=[step], final_answer="done")
        d = trace.to_dict()
        assert len(d["steps"]) == 1
        assert d["steps"][0]["thought"] == "test thought"
        assert d["final_answer"] == "done"
