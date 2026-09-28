# Casewake

Casewake is an AI-assisted QA project that uses current requirements, historical defects, and existing tests to propose and run evidence-backed regression checks.

The repository is at the first execution milestone. It contains a minimal demo server, a browser smoke test, and a pure checkout calculation in `demo_app/checkout.py`. The money and input rules are in [docs/checkout_rules.md](docs/checkout_rules.md). The browser page does not use the calculation yet. The agent, retrieval, MCP service, and reports are planned in [PRD.md](PRD.md) and sequenced in [GETTING_STARTED.md](GETTING_STARTED.md).

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from the repository root:

```bash
uv sync
uv run playwright install chromium
uv run uvicorn demo_app.main:app --reload --port 8001
```

Open <http://127.0.0.1:8001> to see the demo page. The health endpoint is <http://127.0.0.1:8001/health>.

In a second terminal, run the browser smoke test:

```bash
uv run pytest tests/e2e/test_demo_smoke.py -q
```

The test expects the server to be running on port 8001. It verifies that Chromium can open the page and find the heading; checkout behavior is not implemented yet.

The calculation tests run without starting the server:

```bash
uv run pytest tests/unit -q
```
