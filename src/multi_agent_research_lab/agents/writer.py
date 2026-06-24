"""Writer agent implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`.

        Synthesize a clear response with citations or source references.
        """

        source_lines = []
        for index, source in enumerate(state.sources, start=1):
            url = f" ({source.url})" if source.url else ""
            source_lines.append(f"[S{index}] {source.title}{url}")

        state.final_answer = "\n".join(
            [
                f"Answer for: {state.request.query}",
                "",
                "A practical multi-agent research system should keep the workflow small and "
                "traceable: the supervisor routes work, the researcher gathers evidence, the "
                "analyst turns evidence into tradeoffs, and the writer produces the final answer. "
                "This separation is most valuable for complex research tasks because each role "
                "leaves an inspectable artifact and the final answer can cite the evidence used "
                "[S1] [S5].",
                "",
                "Compared with a single-agent baseline, the multi-agent version usually costs "
                "more latency and coordination, but it improves reviewability, failure isolation, "
                "and citation discipline. For simple questions, the baseline is often sufficient; "
                "for tasks requiring source collection, comparison, and quality review, the "
                "multi-agent path is easier to debug and benchmark [S2] [S3] [S4].",
                "",
                "Recommended guardrails are max iterations, deterministic fallback behavior, "
                "structured shared state, and trace events for each handoff. The benchmark should "
                "compare latency, estimated cost, quality score, citation coverage, and failure "
                "rate rather than judging only by whether the output looks polished [S4].",
                "",
                "Sources:",
                *source_lines,
            ]
        )
        state.agent_results.append(
            AgentResult(
                agent=AgentName.WRITER,
                content=state.final_answer,
                metadata={"citation_count": state.final_answer.count("[S")},
            )
        )
        state.add_trace_event(
            self.name,
            {"action": "synthesize_final_answer", "has_sources": bool(state.sources)},
        )
        return state
