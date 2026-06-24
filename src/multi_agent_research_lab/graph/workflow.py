"""Workflow orchestration implementation."""

from collections.abc import Callable

from multi_agent_research_lab.agents import (
    AnalystAgent,
    CriticAgent,
    ResearcherAgent,
    SupervisorAgent,
    WriterAgent,
)
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import AgentExecutionError
from multi_agent_research_lab.core.state import ResearchState

WorkflowNode = Callable[[ResearchState], ResearchState]


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def build(self) -> dict[str, WorkflowNode]:
        """Create the workflow node map.

        LangGraph can replace this deterministic map later without changing the
        agent contract. The lab keeps it dependency-light and offline-safe.
        """

        return {
            "supervisor": SupervisorAgent().run,
            "researcher": ResearcherAgent().run,
            "analyst": AnalystAgent().run,
            "writer": WriterAgent().run,
            "critic": CriticAgent().run,
        }

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""

        settings = get_settings()
        nodes = self.build()
        for _ in range(settings.max_iterations):
            state = nodes["supervisor"](state)
            route = state.route_history[-1]
            if route == "done":
                state.add_trace_event("workflow", {"action": "stop", "reason": "done"})
                return state
            worker = nodes.get(route)
            if worker is None:
                message = f"Unknown workflow route: {route}"
                state.errors.append(message)
                raise AgentExecutionError(message)
            try:
                state = worker(state)
            except Exception as exc:
                message = f"{route} failed: {exc}"
                state.errors.append(message)
                state.add_trace_event("workflow", {"action": "worker_failed", "route": route})
                raise AgentExecutionError(message) from exc

        state.errors.append("Workflow exhausted max_iterations without reaching done.")
        state.add_trace_event("workflow", {"action": "stop", "reason": "max_iterations"})
        return state
