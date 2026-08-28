"""
NovaQure — Agent Layer

Exports the public interface for the ReAct agent orchestration subsystem.

Imports are lazy to avoid pulling in heavy dependencies (PyTorch, RDKit)
at module load time.
"""


def build_react_tools():
    from backend.agents.react_tools import build_react_tools as _build
    return _build()


def build_agent():
    from backend.agents.react_agent import build_agent as _build
    return _build()


def get_orchestrator(*args, **kwargs):
    from backend.agents.agent_service import AgenticOrchestratorService
    return AgenticOrchestratorService(*args, **kwargs)


__all__ = [
    "build_react_tools",
    "build_agent",
    "get_orchestrator",
]
