# Benchmark Report

This report compares the single-agent baseline with the multi-agent workflow. The default lab implementation is offline-safe, so cost is reported as 0.0 unless a provider-backed client is added.

| Run | Latency (s) | Cost (USD) | Quality | Citation Coverage | Failed | Notes |
|---|---:|---:|---:|---:|:---:|---|
| single-agent-baseline | 0.00 | 0.0000 | 4.7 | 67% | no | 3 sources, 0 routes, 1 trace events |
| multi-agent-workflow | 0.00 | 0.0000 | 10.0 | 100% | no | 5 sources, 5 routes, 10 trace events |

## Failure Mode Notes

- Offline mock sources make runs reproducible, but production use should swap in fresh search results and preserve the same citation checks.
- Multi-agent runs may be slower than the baseline because each role writes a separate artifact; the tradeoff is better traceability and review.
