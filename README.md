# Wealth Advisor Assistant — Multi-Agent System

A lightweight production-style multi-agent system for a Wealth Advisor Assistant, implemented with LangGraph.

## Architecture

```text
Client JSON
    |
    v
Orchestrator
    |
    +--> Data Fetcher Agent --> Tool Layer --> Mock CRM API
    |
    v
Analyzer Agent
    |
    +--> transaction anomaly detection
    +--> cash-flow / risk signals
    |
    v
Decision Agent
    |
    +--> structured advisory decision
    |
    v
Human Approval Checkpoint (optional)
    |
    v
Final JSON + persisted memory
```

### Agents

1. **Orchestrator Agent** — owns the execution flow and routes work through the graph.
2. **Data Fetcher Agent** — validates client input and enriches it through the CRM tool abstraction.
3. **Analyzer Agent** — calculates financial metrics and identifies unusual transactions/risk signals.
4. **Decision Agent** — converts analysis into a structured advisory recommendation.

### Tool abstraction

Agents depend on interfaces in `app/tools/interfaces.py`, not raw API implementations. The supplied `MockCRMClient` implements the CRM interface and can be replaced by a real HTTP client without changing agent code.

### Error handling

- Input validation errors are captured in graph state.
- CRM failures are retried once and then converted into a graceful fallback.
- Missing enrichment data does not stop transaction analysis.
- The final response always contains `status`, `analysis`, `decision`, and `errors`.

### Logging

Structured logs capture agent start/end, tool calls, failures, and decisions. Logs are emitted to stdout and `logs/wealth_advisor.log`.

### Memory

- Short-term memory: the current LangGraph state/session.
- Long-term memory: compact client insight summaries persisted in `data/memory.json`.

### Human-in-the-loop

Run with `--human-review` to pause before finalizing a high-risk recommendation. The reviewer can approve, reject, or override the recommendation.

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python -m app.main --input data/sample_client.json
```

With manual review:

```bash
python -m app.main --input data/sample_client.json --human-review
```

## Test

```bash
pytest -q
```

## Sample output

The sample client intentionally contains an unusually large transaction and elevated spending concentration. The analyzer flags those signals and the decision agent produces a `REVIEW` recommendation.

## Key decisions and trade-offs

- **LangGraph StateGraph** was chosen because the workflow has explicit state and deterministic routing, while still allowing agent-based expansion.
- **Rule-based anomaly detection** is intentional for a small assessment: it is explainable, deterministic, and easy to test. A production system could replace it with a statistical/ML detector behind the same analyzer interface.
- **Mock CRM** avoids external credentials and makes the assessment reproducible.
- **Structured JSON decisions** make downstream API/UI integration straightforward.
- The system avoids autonomous financial execution. It produces advisory insights and uses a human checkpoint for high-risk decisions.

## Assumptions

- Transaction amounts are in the client's base currency.
- A transaction is anomalous when it is materially larger than the client's historical transaction distribution or conflicts with simple risk heuristics.
- The mock CRM returns client profile/risk information.
- This is a technical prototype, not financial advice.

## Project structure

```text
app/
  agents/
    data_fetcher.py
    analyzer.py
    decision.py
  memory/
    store.py
  tools/
    interfaces.py
    mock_crm.py
  graph.py
  logging_config.py
  main.py
  state.py
data/
  sample_client.json
tests/
  test_analyzer.py
  test_graph.py
requirements.txt
```
