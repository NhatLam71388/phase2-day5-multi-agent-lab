"""Researcher agent implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def __init__(self, search_client: SearchClient | None = None) -> None:
        self.search_client = search_client or SearchClient()

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`.

        Uses a deterministic local search source by default so the lab runs offline.
        """

        sources = self.search_client.search(state.request.query, state.request.max_sources)
        state.sources = sources
        bullets = [
            f"- [S{index}] {source.title}: {source.snippet}"
            for index, source in enumerate(sources, start=1)
        ]
        state.research_notes = "\n".join(
            [
                f"Research focus: {state.request.query}",
                f"Audience: {state.request.audience}",
                "Evidence gathered:",
                *bullets,
            ]
        )
        state.agent_results.append(
            AgentResult(
                agent=AgentName.RESEARCHER,
                content=state.research_notes,
                metadata={"source_count": len(sources)},
            )
        )
        state.add_trace_event(
            self.name,
            {"action": "search_and_summarize", "source_count": len(sources)},
        )
        return state
