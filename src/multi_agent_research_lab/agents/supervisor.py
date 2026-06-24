"""Supervisor / router implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route.

        The policy is intentionally small and inspectable for the lab:
        researcher -> analyst -> writer -> critic -> done.
        """

        settings = get_settings()
        if state.iteration >= settings.max_iterations:
            next_route = "done"
            state.errors.append("Supervisor stopped workflow at max_iterations.")
        elif not state.research_notes or not state.sources:
            next_route = "researcher"
        elif not state.analysis_notes:
            next_route = "analyst"
        elif not state.final_answer:
            next_route = "writer"
        elif not state.critic_notes:
            next_route = "critic"
        else:
            next_route = "done"

        state.record_route(next_route)
        state.agent_results.append(
            AgentResult(
                agent=AgentName.SUPERVISOR,
                content=f"Next route: {next_route}",
                metadata={"iteration": state.iteration},
            )
        )
        state.add_trace_event(
            self.name,
            {"action": "route", "next_route": next_route, "iteration": state.iteration},
        )
        return state
