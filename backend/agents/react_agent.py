"""
NovaQure

ReAct Agent — Core Agent Construction

Builds a LangChain ReAct agent equipped with the NovaQure evaluation,
mutation, ranking, and explanation tools.  The agent follows a
Thought → Action → Observation → Thought cycle to autonomously refine
drug candidates.

Provides two execution modes:

1. **LLM-driven** — Uses the configured Ollama / NVIDIA endpoint for
   natural-language reasoning via ``create_react_agent``.
2. **Deterministic fallback** — When no LLM endpoint is available,
   executes a hard-coded Thought/Action/Observation trace that mirrors
   the same evaluation-decide-mutate pipeline, ensuring the system
   never fails due to external dependencies.

Author:
    NovaQure Agent Team
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from backend.agents.react_tools import build_react_tools
from backend.configs.llm_config import get_active_llm_info

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Structured reasoning trace
# ------------------------------------------------------------------

@dataclass
class ReActStep:
    """One step in a ReAct reasoning trace."""
    thought: str
    action: str
    action_input: str
    observation: str


@dataclass
class ReActTrace:
    """Complete trace of a single agent execution."""
    steps: List[ReActStep] = field(default_factory=list)
    final_answer: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "steps": [
                {
                    "thought": s.thought,
                    "action": s.action,
                    "action_input": s.action_input,
                    "observation": s.observation[:500],  # truncate large outputs
                }
                for s in self.steps
            ],
            "final_answer": self.final_answer,
        }


# ------------------------------------------------------------------
# LLM-backed ReAct Agent (LangChain)
# ------------------------------------------------------------------

def _try_build_langchain_agent():
    """
    Attempt to construct a LangChain agent graph using the configured
    LLM provider.  Returns ``None`` if the provider is unavailable or if
    LangChain agent construction fails for any reason.
    """
    info = get_active_llm_info()

    if info["type"] == "none":
        logger.info("No LLM provider configured; falling back to deterministic agent.")
        return None

    try:
        from langchain.agents import create_agent

        tools = build_react_tools()

        # Convert Tool objects to callable functions for create_agent
        tool_funcs = []
        for t in tools:
            # create_agent expects callables with docstrings
            def make_tool_func(tool_obj):
                def wrapper(input_str: str) -> str:
                    return tool_obj.func(input_str)
                wrapper.__name__ = tool_obj.name
                wrapper.__doc__ = tool_obj.description
                return wrapper
            tool_funcs.append(make_tool_func(t))

        if info["type"] == "ollama":
            try:
                from langchain_ollama import ChatOllama
            except ImportError:
                try:
                    from langchain_community.chat_models.ollama import ChatOllama
                except ImportError:
                    from langchain_community.chat_models import ChatOllama

            model = ChatOllama(
                model=info["model"],
                base_url=info["endpoint"].replace("/api/generate", ""),
                timeout=15,
            )
        elif info["type"] == "nvidia":
            # Use model string format for NVIDIA
            model = f"nvidia:{info['model']}"
        else:
            return None

        agent_graph = create_agent(
            model=model,
            tools=tool_funcs,
            system_prompt=(
                "You are the NovaQure Drug Discovery Agent. Your job is to evaluate, "
                "refine, and rank drug candidate molecules using your available tools. "
                "Always evaluate first, then decide whether to keep, refine, or regenerate, "
                "and finally explain your reasoning."
            ),
            name="novaqure_react_agent",
        )

        logger.info("LangChain agent graph built with provider: %s (%s)", info["provider"], info["model"])
        return agent_graph

    except Exception as exc:
        logger.warning("Failed to build LangChain agent (%s); using deterministic fallback.", exc)
        return None


# ------------------------------------------------------------------
# Deterministic Fallback ReAct Agent
# ------------------------------------------------------------------

class DeterministicReActAgent:
    """
    A rule-based agent that executes the same Thought → Action → Observation
    loop without an external LLM.  This guarantees zero-failure operation
    when running offline or in CI.
    """

    def __init__(self) -> None:
        self.tools = {t.name: t for t in build_react_tools()}

    def run(
        self,
        smiles: str,
        selfies: str,
        molecule_id: str,
        energy: float = -0.85,
        variance: float = 0.12,
        noise: float = 0.08,
        convergence: float = 0.93,
    ) -> Dict[str, Any]:
        """Execute the deterministic evaluation-decide-explain cycle."""

        trace = ReActTrace()

        # ---- Step 1: Evaluate the molecule ----
        step1_thought = (
            f"I need to evaluate molecule {molecule_id} (SMILES: {smiles}) "
            "using the full quantum-classical pipeline."
        )
        eval_input = json.dumps({
            "smiles": smiles,
            "energy": energy,
            "variance": variance,
            "noise": noise,
            "convergence": convergence,
        })
        eval_output = self.tools["EvaluateMolecule"].func(eval_input)
        trace.steps.append(ReActStep(
            thought=step1_thought,
            action="EvaluateMolecule",
            action_input=eval_input,
            observation=eval_output,
        ))

        try:
            eval_data = json.loads(eval_output)
        except json.JSONDecodeError:
            eval_data = {}

        # ---- Step 2: Decide (keep / refine / regenerate) ----
        qed = eval_data.get("qed", 0.0)
        reliability = eval_data.get("reliability_score", 0.0)
        affinity = eval_data.get("affinity", 0.0)

        if qed >= 0.6 and reliability >= 50.0:
            decision = "keep"
            reason = "molecule meets drug-likeness and reliability thresholds"
        elif reliability < 50.0:
            decision = "regenerate"
            reason = "reliability below acceptable threshold"
        else:
            decision = "refine"
            reason = "drug-likeness or affinity needs improvement"

        step2_thought = (
            f"Evaluation complete. QED={qed:.3f}, reliability={reliability:.1f}, "
            f"affinity={affinity:.3f}. Decision: {decision} because {reason}."
        )
        trace.steps.append(ReActStep(
            thought=step2_thought,
            action="Decision",
            action_input=json.dumps({"decision": decision, "reason": reason}),
            observation=f"Agent decided to {decision}.",
        ))

        # ---- Step 3: If refine, mutate the molecule ----
        mutated_smiles = None
        mutated_selfies = None
        if decision == "refine":
            step3_thought = "Decision is 'refine'. Applying structural mutation to improve candidate."
            mutate_input = json.dumps({"selfies": selfies})
            mutate_output = self.tools["MutateMolecule"].func(mutate_input)
            trace.steps.append(ReActStep(
                thought=step3_thought,
                action="MutateMolecule",
                action_input=mutate_input,
                observation=mutate_output,
            ))
            try:
                mut_data = json.loads(mutate_output)
                mutated_smiles = mut_data.get("mutated_smiles")
                mutated_selfies = mut_data.get("mutated_selfies")
            except json.JSONDecodeError:
                pass

        # ---- Step 4: Explain ----
        step4_thought = "Generating plain-language explanation for this candidate."
        explain_input = json.dumps({
            "components": {
                "qed": qed,
                "affinity_score": abs(affinity) / 10.0,
                "reliability_score": reliability / 100.0,
            }
        })
        explain_output = self.tools["ExplainMolecule"].func(explain_input)
        trace.steps.append(ReActStep(
            thought=step4_thought,
            action="ExplainMolecule",
            action_input=explain_input,
            observation=explain_output,
        ))

        try:
            explanation = json.loads(explain_output)
        except json.JSONDecodeError:
            explanation = {"reason": "explanation unavailable"}

        # ---- Final Answer ----
        trace.final_answer = (
            f"Molecule {molecule_id}: decision='{decision}' | "
            f"QED={qed:.3f} | Reliability={reliability:.1f}% | "
            f"Reason: {reason}"
        )

        return {
            "molecule_id": molecule_id,
            "smiles": smiles,
            "selfies": selfies,
            "decision": decision,
            "reason": reason,
            "evaluation": eval_data,
            "explanation": explanation,
            "mutated_smiles": mutated_smiles,
            "mutated_selfies": mutated_selfies,
            "react_trace": trace.to_dict(),
        }


# ------------------------------------------------------------------
# Public Factory
# ------------------------------------------------------------------

def build_agent() -> DeterministicReActAgent:
    """
    Build and return the NovaQure ReAct agent.

    Attempts to construct a LangChain-powered agent first.  If the LLM
    endpoint is unreachable the deterministic fallback is returned instead.
    """
    # We store the LangChain executor on the deterministic agent so callers
    # get a single consistent interface.
    agent = DeterministicReActAgent()

    executor = _try_build_langchain_agent()
    if executor is not None:
        agent._langchain_executor = executor
        logger.info("LangChain executor attached to agent (LLM-driven mode).")
    else:
        agent._langchain_executor = None
        logger.info("Agent running in deterministic fallback mode.")

    return agent
