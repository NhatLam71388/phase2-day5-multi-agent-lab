"""Critic agent implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings.

        Add fact-check, citation coverage, and failure-mode checks.
        """

        if not state.final_answer:
            state.errors.append("Critic ran before final answer was available.")
            state.critic_notes = "Critic review failed: no final answer was available."
        else:
            cited = sum(
                1
                for index in range(1, len(state.sources) + 1)
                if f"[S{index}]" in state.final_answer
            )
            coverage = cited / len(state.sources) if state.sources else 0.0
            verdict = "pass" if coverage >= 0.5 and not state.errors else "needs_attention"
            state.critic_notes = "\n".join(
                [
                    f"Critic verdict: {verdict}",
                    "Citation coverage: "
                    f"{coverage:.0%} ({cited}/{len(state.sources)} sources cited)",
                    "Failure mode to monitor: stale or mock sources can make a polished answer "
                    "look better supported than it is.",
                ]
            )
        state.agent_results.append(
            AgentResult(
                agent=AgentName.CRITIC,
                content=state.critic_notes or "",
                metadata={"error_count": len(state.errors)},
            )
        )
        state.add_trace_event(
            self.name,
            {"action": "review_final_answer", "error_count": len(state.errors)},
        )
        return state
