"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query.

        The lab must run offline, so the default implementation returns deterministic
        local sources. A real provider can replace this class without changing agents.
        """

        normalized = " ".join(query.split())
        topics = [
            (
                "Agent orchestration patterns",
                "Role-specific agents work best when each handoff has a clear state contract, "
                "bounded iteration count, and explicit stop condition.",
                "https://example.local/agent-orchestration",
            ),
            (
                "Research workflow guardrails",
                "Production research assistants should capture sources, validate final claims, "
                "and fall back to deterministic behavior when external providers are unavailable.",
                "https://example.local/research-guardrails",
            ),
            (
                "Single-agent versus multi-agent tradeoffs",
                "Single-agent baselines are cheaper and simpler, while multi-agent workflows can "
                "improve decomposition, reviewability, and citation discipline on complex tasks.",
                "https://example.local/single-vs-multi-agent",
            ),
            (
                "Benchmarking LLM systems",
                "Useful evaluations combine latency, quality rubrics, citation coverage, cost, "
                "and failure rate instead of relying on a single subjective output.",
                "https://example.local/benchmarking-llm-systems",
            ),
            (
                "Traceable shared state",
                "Shared state should preserve request context, intermediate notes, route history, "
                "errors, and trace events so a reviewer can reconstruct the workflow.",
                "https://example.local/shared-state-tracing",
            ),
        ]
        sources: list[SourceDocument] = []
        for index, (title, snippet, url) in enumerate(topics[:max_results], start=1):
            sources.append(
                SourceDocument(
                    title=title,
                    url=url,
                    snippet=f"{snippet} Query focus: {normalized}.",
                    metadata={"rank": index, "provider": "local_mock", "citation_id": f"S{index}"},
                )
            )
        return sources
