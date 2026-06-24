from multi_agent_research_lab.cli import run_multi_agent_workflow
from multi_agent_research_lab.evaluation.benchmark import run_benchmark


def test_benchmark_runs_offline() -> None:
    state, metrics = run_benchmark(
        "multi-agent-workflow",
        "Explain multi-agent systems",
        run_multi_agent_workflow,
    )

    assert state.final_answer
    assert metrics.latency_seconds >= 0
    assert metrics.quality_score and metrics.quality_score > 0
    assert metrics.citation_coverage and metrics.citation_coverage > 0
    assert not metrics.failed
