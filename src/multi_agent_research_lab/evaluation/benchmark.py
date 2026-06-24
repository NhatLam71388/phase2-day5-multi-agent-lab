"""Benchmark implementation for single-agent vs multi-agent."""

import re
from collections.abc import Callable
from time import perf_counter

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState

Runner = Callable[[str], ResearchState]


def run_benchmark(
    run_name: str,
    query: str,
    runner: Runner,
) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return benchmark metrics."""

    started = perf_counter()
    failed = False
    try:
        state = runner(query)
    except Exception as exc:
        failed = True
        from multi_agent_research_lab.core.schemas import ResearchQuery

        state = ResearchState(request=ResearchQuery(query=query), errors=[str(exc)])
    latency = perf_counter() - started
    coverage = _citation_coverage(state)
    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=0.0,
        quality_score=_quality_score(state, coverage, failed),
        citation_coverage=coverage,
        failed=failed or bool(state.errors),
        notes=_notes(state),
    )
    return state, metrics


def _citation_coverage(state: ResearchState) -> float:
    if not state.sources:
        return 0.0
    answer = state.final_answer or ""
    cited = len(set(re.findall(r"\[S(\d+)\]", answer)))
    return min(cited, len(state.sources)) / len(state.sources)


def _quality_score(state: ResearchState, citation_coverage: float, failed: bool) -> float:
    if failed or not state.final_answer:
        return 0.0
    score = 4.0
    score += 2.0 if state.research_notes else 0.0
    score += 2.0 if state.analysis_notes else 0.0
    score += 1.0 if state.critic_notes else 0.0
    score += citation_coverage
    return min(score, 10.0)


def _notes(state: ResearchState) -> str:
    if state.errors:
        return "Failed or completed with errors: " + "; ".join(state.errors)
    return (
        f"{len(state.sources)} sources, "
        f"{len(state.route_history)} routes, "
        f"{len(state.trace)} trace events"
    )
