"""Command-line entrypoint for the completed lab."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_markdown_report
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging
from multi_agent_research_lab.services.search_client import SearchClient

app = typer.Typer(help="Multi-Agent Research Lab CLI")
console = Console()


def _init() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a deterministic single-agent baseline."""

    _init()
    state = run_single_agent_baseline(query)
    console.print(Panel.fit(state.final_answer or "", title="Single-Agent Baseline"))


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow."""

    _init()
    state = ResearchState(request=ResearchQuery(query=query))
    workflow = MultiAgentWorkflow()
    result = workflow.run(state)
    console.print(result.model_dump_json(indent=2))


@app.command()
def benchmark(
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Path to write the markdown report"),
    ] = Path("reports/benchmark_report.md"),
) -> None:
    """Run baseline and multi-agent benchmark and write a markdown report."""

    _init()
    query = "Research GraphRAG state-of-the-art and write a 500-word summary"
    _, baseline_metrics = run_benchmark("single-agent-baseline", query, run_single_agent_baseline)
    _, multi_metrics = run_benchmark("multi-agent-workflow", query, run_multi_agent_workflow)
    report = render_markdown_report([baseline_metrics, multi_metrics])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    console.print(Panel.fit(str(output), title="Benchmark report written"))


@app.command()
def trace(
    query: Annotated[
        str,
        typer.Option("--query", "-q", help="Research query"),
    ] = "Research GraphRAG state-of-the-art and write a 500-word summary",
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Path to write the markdown trace report"),
    ] = Path("reports/trace_report.md"),
    json_output: Annotated[
        Path,
        typer.Option("--json-output", help="Path to write the raw JSON trace"),
    ] = Path("reports/trace.json"),
) -> None:
    """Run the multi-agent workflow and write trace artifacts."""

    _init()
    state = run_multi_agent_workflow(query)
    output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_trace_report(state), encoding="utf-8")
    json_output.write_text(state.model_dump_json(indent=2), encoding="utf-8")
    console.print(Panel.fit(f"{output}\n{json_output}", title="Trace artifacts written"))


def run_single_agent_baseline(query: str) -> ResearchState:
    """Offline-safe baseline that performs all steps in one function."""

    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    state.sources = SearchClient().search(query, max_results=min(3, request.max_sources))
    state.final_answer = (
        f"Baseline answer for: {query}\n\n"
        "A single agent can answer by collecting a few sources, summarizing the tradeoffs, "
        "and producing a concise response. This is simple and fast, but it gives less "
        "visibility into separate research, analysis, and review steps [S1] [S2]."
    )
    state.add_trace_event(
        "baseline",
        {"action": "single_agent_answer", "source_count": len(state.sources)},
    )
    return state


def run_multi_agent_workflow(query: str) -> ResearchState:
    """Runner adapter used by the benchmark module."""

    return MultiAgentWorkflow().run(ResearchState(request=ResearchQuery(query=query)))


def render_trace_report(state: ResearchState) -> str:
    """Render workflow trace as a markdown artifact suitable for lab submission."""

    lines = [
        "# Multi-Agent Trace Report",
        "",
        f"Query: `{state.request.query}`",
        "",
        "## Route History",
        "",
        " -> ".join(state.route_history),
        "",
        "## Trace Events",
        "",
        "| Step | Name | Action | Details |",
        "|---:|---|---|---|",
    ]
    for index, event in enumerate(state.trace, start=1):
        payload = event.get("payload", {})
        action = payload.get("action", "")
        details = ", ".join(
            f"{key}={value}" for key, value in payload.items() if key != "action"
        )
        lines.append(f"| {index} | {event.get('name', '')} | {action} | {details} |")

    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- Sources: {len(state.sources)}",
            f"- Research notes: {'yes' if state.research_notes else 'no'}",
            f"- Analysis notes: {'yes' if state.analysis_notes else 'no'}",
            f"- Final answer: {'yes' if state.final_answer else 'no'}",
            f"- Critic notes: {'yes' if state.critic_notes else 'no'}",
            f"- Errors: {len(state.errors)}",
            "",
            "## Critic Notes",
            "",
            state.critic_notes or "No critic notes were produced.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    app()
