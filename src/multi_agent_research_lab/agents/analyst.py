"""Analyst agent implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`.

        Extract key claims, compare tradeoffs, and flag weak evidence.
        """

        if not state.research_notes:
            state.errors.append("Analyst ran before research notes were available.")
            state.analysis_notes = "No research notes were available; analysis is limited."
        else:
            source_count = len(state.sources)
            state.analysis_notes = "\n".join(
                [
                    "Key claims:",
                    "- Multi-agent systems are useful when work benefits from decomposition, "
                    "handoff, and independent review.",
                    "- A single-agent baseline remains important because it is simpler, faster, "
                    "and cheaper for straightforward requests.",
                    "- Guardrails should include max iterations, trace events, validation, and "
                    "fallback behavior.",
                    "",
                    "Tradeoffs:",
                    "- Multi-agent workflows add latency and coordination overhead.",
                    "- They improve inspectability because each role leaves a separate artifact.",
                    "",
                    "Evidence gaps:",
                    f"- This offline run used {source_count} local mock sources; production runs "
                    "should replace them with fresh provider-backed search.",
                ]
            )
        state.agent_results.append(
            AgentResult(
                agent=AgentName.ANALYST,
                content=state.analysis_notes or "",
                metadata={
                    "source_count": len(state.sources),
                    "has_research": bool(state.research_notes),
                },
            )
        )
        state.add_trace_event(
            self.name,
            {"action": "analyze_research", "has_research": bool(state.research_notes)},
        )
        return state
