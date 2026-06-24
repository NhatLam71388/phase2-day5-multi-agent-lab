# Failure Mode and Fix

## Failure Mode

The offline lab uses deterministic mock sources so the workflow can run without API
keys. This is good for reproducible demos, but it can hide a production risk: the
final answer may look well cited even when the underlying sources are stale, generic,
or not specific enough for a real research question.

## Impact

- The writer may produce a polished answer with citations that do not prove every
  important claim.
- The benchmark can overestimate quality because mock sources are stable and never
  fail.
- Users may trust the trace because it is complete, even though the evidence source
  is not live.

## Fix

- Replace `SearchClient` with a provider-backed search implementation such as Tavily,
  Bing, SerpAPI, or an internal document index.
- Keep the current `CriticAgent` citation coverage check, then extend it to verify
  claim-level support instead of only checking whether source IDs appear.
- Store raw search metadata in `SourceDocument.metadata` so reviewers can inspect
  provider, rank, timestamp, and retrieval query.
- Keep the deterministic fallback for tests and offline demos, but mark those runs
  clearly in benchmark notes.

## Current Guardrails

- `MAX_ITERATIONS` prevents endless routing.
- The supervisor records every route in `route_history`.
- Every agent writes trace events.
- The benchmark records failure status, quality score, citation coverage, latency,
  and cost.
