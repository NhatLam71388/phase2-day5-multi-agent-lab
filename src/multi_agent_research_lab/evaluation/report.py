"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown."""

    lines = [
        "# Benchmark Report",
        "",
        "This report compares the single-agent baseline with the multi-agent workflow. "
        "The default lab implementation is offline-safe, so cost is reported as 0.0 "
        "unless a provider-backed client is added.",
        "",
        "| Run | Latency (s) | Cost (USD) | Quality | Citation Coverage | Failed | Notes |",
        "|---|---:|---:|---:|---:|:---:|---|",
    ]
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"{item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        coverage = "" if item.citation_coverage is None else f"{item.citation_coverage:.0%}"
        failed = "yes" if item.failed else "no"
        notes = item.notes.replace("|", "\\|")
        lines.append(
            f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | "
            f"{coverage} | {failed} | {notes} |"
        )
    lines.extend(
        [
            "",
            "## Failure Mode Notes",
            "",
            "- Offline mock sources make runs reproducible, but production use should swap in "
            "fresh search results and preserve the same citation checks.",
            "- Multi-agent runs may be slower than the baseline because each role writes a "
            "separate artifact; the tradeoff is better traceability and review.",
        ]
    )
    return "\n".join(lines) + "\n"
