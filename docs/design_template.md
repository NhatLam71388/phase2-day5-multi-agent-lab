# Design: Offline-Safe Multi-Agent Research System

## Problem

Build a research assistant that answers broad technical questions by collecting evidence,
analyzing tradeoffs, writing a final answer, and leaving a trace that reviewers can inspect.

## Why multi-agent?

A single-agent baseline is simpler and faster, but it hides the intermediate reasoning and
evidence checks. The multi-agent workflow separates responsibilities so each handoff is visible:
research, analysis, writing, and review each produce a concrete artifact in shared state.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Choose the next route and stop when complete | Shared state | `route_history`, trace event | Stops at `MAX_ITERATIONS` |
| Researcher | Gather local/offline sources and notes | Query, source limit | `sources`, `research_notes` | Mock sources may be stale |
| Analyst | Extract claims, tradeoffs, and gaps | Research notes, sources | `analysis_notes` | Limited analysis if research is missing |
| Writer | Synthesize the final answer with citations | Research + analysis | `final_answer` | Weak citation coverage |
| Critic | Review evidence coverage and failure modes | Final answer, sources | `critic_notes` | Flags missing answer or weak support |

## Shared state

`ResearchState` is the single source of truth. It stores the request, iteration count,
route history, sources, research notes, analysis notes, final answer, critic notes,
agent results, trace events, and errors. This is enough to debug who acted, what they
produced, and why the workflow stopped.

## Routing policy

The workflow uses a deterministic route:

```text
supervisor -> researcher -> supervisor -> analyst -> supervisor -> writer
           -> supervisor -> critic -> supervisor -> done
```

The supervisor selects the first missing artifact in this order: research, analysis,
final answer, critic review. It records every route and stops when all artifacts exist
or `MAX_ITERATIONS` is reached.

## Guardrails

- Max iterations: configured by `MAX_ITERATIONS`, default `6`.
- Timeout: configured by `TIMEOUT_SECONDS`; provider-backed clients should enforce it.
- Retry: provider clients should retry inside service abstractions, not inside agents.
- Fallback: default LLM and search clients are deterministic and offline-safe.
- Validation: Pydantic schemas validate requests, sources, metrics, and state fields.

## Benchmark plan

The benchmark compares:

| Run | Expected outcome |
|---|---|
| Single-agent baseline | Lower complexity, fewer artifacts, lower trace detail |
| Multi-agent workflow | More trace events, explicit research/analysis/review artifacts |

Metrics:

- Latency: wall-clock time.
- Cost: `0.0` for offline mode, provider usage when integrated.
- Quality: heuristic score based on answer, intermediate artifacts, and review.
- Citation coverage: cited source IDs divided by available sources.
- Failure rate: whether the run raised an exception or completed with errors.
