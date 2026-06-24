# Lab 20: Multi-Agent Research System

Repo hoàn chỉnh cho bài lab **Multi-Agent Systems**: xây dựng hệ thống nghiên cứu gồm **Supervisor + Researcher + Analyst + Writer + Critic** và benchmark với single-agent baseline.

> Repo này đã được hoàn thiện thành bản lab chạy end-to-end, ưu tiên offline-safe để
> học viên có thể benchmark và review trace ngay cả khi chưa có API key.

## Learning outcomes

Sau 2 giờ lab, học viên cần có thể:

1. Thiết kế role rõ ràng cho nhiều agent.
2. Xây dựng shared state đủ thông tin cho handoff.
3. Thêm guardrail tối thiểu: max iterations, timeout, retry/fallback, validation.
4. Trace được luồng chạy và giải thích agent nào làm gì.
5. Benchmark single-agent vs multi-agent theo quality, latency, cost.

## Architecture mục tiêu

```text
User Query
   |
   v
Supervisor / Router
   |------> Researcher Agent  -> research_notes
   |------> Analyst Agent     -> analysis_notes
   |------> Writer Agent      -> final_answer
   |------> Critic Agent      -> critic_notes
   |
   v
Trace + Benchmark Report
```

## Cấu trúc repo

```text
.
├── src/multi_agent_research_lab/
│   ├── agents/              # Agent interfaces + implementations
│   ├── core/                # Config, state, schemas, errors
│   ├── graph/               # Multi-agent workflow orchestration
│   ├── services/            # LLM, search, storage clients
│   ├── evaluation/          # Benchmark/evaluation implementation
│   ├── observability/       # Logging/tracing hooks
│   └── cli.py               # CLI entrypoint
├── configs/                 # YAML configs for lab variants
├── docs/                    # Lab guide, rubric, design notes
├── tests/                   # Unit tests for workflow behavior
├── notebooks/               # Optional notebook entrypoint
├── scripts/                 # Helper scripts
├── .env.example             # Environment variables template
├── pyproject.toml           # Python project config
├── Dockerfile               # Containerized dev/runtime
└── Makefile                 # Common commands
```

## Quickstart

### 1. Tạo môi trường

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e "[dev]"
cp .env.example .env
```

### 2. Cấu hình API keys

Mở `.env` và điền key cần thiết.

```bash
OPENAI_API_KEY=...
# optional
LANGSMITH_API_KEY=...
TAVILY_API_KEY=...
```

### 3. Chạy smoke test

```bash
make test
python -m multi_agent_research_lab.cli --help
```

### 4. Chạy baseline

```bash
python -m multi_agent_research_lab.cli baseline \
  --query "Research GraphRAG state-of-the-art and write a 500-word summary"
```

Lệnh này chạy baseline single-agent deterministic để so sánh với workflow nhiều agent.

### 5. Chạy multi-agent workflow

```bash
python -m multi_agent_research_lab.cli multi-agent \
  --query "Research GraphRAG state-of-the-art and write a 500-word summary"
```

Mặc định lệnh chạy offline bằng local search mock, ghi route history và trace trong state.

### 6. Tạo benchmark report

```bash
python -m multi_agent_research_lab.cli benchmark
```

Report được ghi tại `reports/benchmark_report.md`.

### 7. Tạo trace artifact

```bash
python -m multi_agent_research_lab.cli trace
```

Trace report được ghi tại `reports/trace_report.md`; raw trace JSON được ghi tại
`reports/trace.json`.

## Milestones trong 2 giờ lab

| Thời lượng | Milestone | File gợi ý |
|---:|---|---|
| 0-15' | Setup, chạy baseline | `cli.py`, `services/llm_client.py` |
| 15-45' | Build Supervisor / router | `agents/supervisor.py`, `graph/workflow.py` |
| 45-75' | Thêm Researcher, Analyst, Writer | `agents/*.py`, `core/state.py` |
| 75-95' | Trace + benchmark single vs multi | `observability/tracing.py`, `evaluation/benchmark.py` |
| 95-115' | Peer review theo rubric | `docs/peer_review_rubric.md` |
| 115-120' | Exit ticket | `docs/lab_guide.md` |

## Quy ước production trong repo

- Tách rõ `agents`, `services`, `core`, `graph`, `evaluation`, `observability`.
- Không hard-code API key trong code.
- Tất cả input/output chính dùng Pydantic schema.
- Có type hints, linting, formatting, unit test tối thiểu.
- Có logging/tracing hook ngay từ đầu.
- Không để agent chạy vô hạn: dùng `max_iterations`, `timeout_seconds`.
- Có benchmark report thay vì chỉ demo output đẹp.

## Extension ideas

1. Thay local mock search bằng Tavily, Bing, SerpAPI hoặc internal docs.
2. Thay deterministic `LLMClient` bằng OpenAI/Azure OpenAI provider thật.
3. Gửi trace sang LangSmith, Langfuse hoặc OpenTelemetry.
4. Thêm human/peer review quality score vào benchmark report.

## Deliverables

Học viên nộp:

1. GitHub repo cá nhân.
2. Screenshot trace hoặc link trace: `reports/trace_report.md` và `reports/trace.json`.
3. `reports/benchmark_report.md` so sánh single vs multi-agent.
4. Một đoạn giải thích failure mode và cách fix: `reports/failure_mode.md`.

## References

- Anthropic: Building effective agents — https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents SDK orchestration/handoffs — https://developers.openai.com/api/docs/guides/agents/orchestration
- LangGraph concepts — https://langchain-ai.github.io/langgraph/concepts/
- LangSmith tracing — https://docs.smith.langchain.com/
- Langfuse tracing — https://langfuse.com/docs
