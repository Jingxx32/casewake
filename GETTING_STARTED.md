# QA Memory Agent: A Practical Getting-Started Guide

Written for this project on September 25, 2026.

**Your first goal is to build a tiny checkout application and make one automated test pass on its correct version and fail on a deliberately faulty version.** Once that works, add AI planning, historical knowledge, and the product interface in separate steps.

This guide assumes one developer working locally on macOS. The suggested business rules and implementation choices are starting defaults, not decisions already approved or implemented.

## 1. Understand where the project is today

The folder currently contains planning documents, not a runnable application:

| Document | How to use it |
| --- | --- |
| [PRD.md](/Users/xujingxuan/Documents/Projects/ai-agent-project/PRD.md) | The proposed scope, requirements, milestones, and evaluation criteria |
| [Original exploration](/Users/xujingxuan/Documents/Projects/ai-agent-project/agentic_rag_software_testing_assistant.md) | Background ideas, course connections, and possible extensions |
| This guide | A concrete sequence for moving from the documents to an implementation |

There is no existing server, dependency manifest, or startup command. The commands below are instructions for creating the foundation; they have not been executed as part of writing this guide.

Use the newer PRD as the planning baseline. In particular, its first release uses **one main agent**. You do not need to implement the older document's seven versions or its multi-agent stage. MCP and evaluation are part of the PRD's first release, even though they can be introduced after a simpler local prototype.

## 2. Describe the product in one concrete example

You are building two separate things:

1. **A small checkout application:** the website being tested. It has a correct version and controlled faulty variants.
2. **QA Memory Agent:** the system that reads requirements and historical bugs, proposes tests, runs them against that application, and explains the evidence.

The agent's eventual UI is also separate from the checkout page. Keep their responsibilities distinct even if they initially share a repository.

Example user request:

> Check whether gift cards still work correctly after adding checkout discounts.

Example workflow:

```text
Current checkout rules + historical bugs + existing tests
                         |
                  Select relevant context
                         |
                Propose 1–3 structured tests
                         |
                  Validate the test plan
                         |
                Execute with Playwright
                         |
          Save assertions, logs, screenshots, and traces
                         |
               Produce a report with sources
```

The product's hypothesis is that historical QA knowledge can help it select useful regression cases. You will measure whether that happens; improvement is not guaranteed.

## 3. Make these initial scope choices

Start with the checkout example already proposed in the PRD:

| Decision | Suggested initial choice |
| --- | --- |
| Feature | Discount plus gift-card checkout |
| Starting fixture | Subtotal 100.00, discount 20.00, gift-card balance 80.00 |
| Money representation | Integer cents, in one configured currency |
| First discount type | Fixed amount; percentage rounding can wait |
| Expected result | Gift-card debit 80.00; remaining payment 0.00 |
| Test scope | One local application, one browser, sequential execution |
| First knowledge set | About 3 requirements, 3 synthetic historical bugs, and 2 existing tests |
| First interface | Command line and saved JSON/Markdown reports |
| First agent | One planner with bounded follow-up decisions |

Write the money rules before writing the implementation. Suggested rules for nonnegative integer-cent inputs are:

```text
discounted_total = max(subtotal - fixed_discount, 0)
gift_card_debit  = min(gift_card_balance, discounted_total)
remaining_due   = discounted_total - gift_card_debit
remaining_card  = gift_card_balance - gift_card_debit
```

Also specify what happens with invalid inputs. For the first prototype, reject negative amounts and non-integer cents. Exclude tax, shipping, multiple currencies, and percentage discounts until explicitly defined.

For the initial faulty variant, deliberately calculate the debit against the original subtotal. The 100.00/20.00/80.00 fixture does **not** expose that particular bug: both implementations debit 80.00. Add a 100.00 card-balance case, where the correct debit is 80.00 but the faulty debit is 100.00. This is why your fixtures must actually distinguish correct and faulty behavior.

Keep the fault identity in an evaluator-only manifest. An agent-facing target label such as `target-001` must not disclose the injected defect.

## 4. Learn each component when you need it

| Component | Plain-English purpose | Introduce it when |
| --- | --- | --- |
| Python | Implements backend logic and testing operations | Immediately |
| FastAPI | Provides HTTP endpoints and can serve the small demo page | First local server |
| Playwright | Opens the browser, performs actions, and checks outcomes | First real test |
| Pydantic | Checks that plans and tool arguments have valid structure | Structured test runner |
| LLM | Selects test scenarios and interprets evidence | Reliable manual tests exist |
| RAG | Finds relevant documents and supplies them to the model | Planning works with supplied documents |
| Embeddings | Represent text numerically for similarity search | Adding semantic retrieval |
| PostgreSQL + pgvector | Stores durable records and supports vector search | Persisting runs and implementing retrieval |
| MCP | Gives clients a standard interface to the testing tools | Local tool functions work |
| LangGraph | Coordinates state, branches, and bounded decisions | End-to-end functions work |
| React + TypeScript | Displays setup, progress, reports, and history | Backend workflow is usable |

These are the PRD's proposed technologies, organized by dependency. You can build the first execution milestone without a model account, vector database, React application, or Docker installation.

## 5. Your first work session: get one local page under test

### Step 1: Prepare the Python environment

The environment inspection found Python, Git, and Node on the shell path. It did not find `uv` or `docker`; that does not prove they are absent from every location.

Use `uv` to manage the Python environment and dependencies. If Homebrew is available:

```bash
brew install uv
```

Otherwise, use the installation method appropriate to your machine from the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

Then initialize this directory once:

```bash
cd /Users/xujingxuan/Documents/Projects/ai-agent-project
uv init --bare --python 3.12
uv python pin 3.12
uv add fastapi uvicorn pydantic playwright
uv add --dev pytest pytest-playwright
uv run playwright install chromium
mkdir -p demo_app tests/e2e
touch demo_app/__init__.py
```

Python 3.12 is a suggested starting version. Keep the generated `pyproject.toml`, `uv.lock`, and `.python-version` in version control once dependencies resolve. `uv init --bare` creates a minimal project; if a `pyproject.toml` already exists by the time you use this guide, inspect it instead of reinitializing. See [uv project creation](https://docs.astral.sh/uv/concepts/projects/init/).

### Step 2: Create a tiny server

Create `/Users/xujingxuan/Documents/Projects/ai-agent-project/demo_app/main.py` with:

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home():
    return "<main><h1>Checkout demo</h1></main>"
```

From the project directory, start it:

```bash
uv run uvicorn demo_app.main:app --reload --port 8001
```

Keep that terminal open. Visit [the local demo](http://127.0.0.1:8001) and [the health endpoint](http://127.0.0.1:8001/health). You should see the heading and `{"status":"ok"}` respectively. FastAPI's [first-steps tutorial](https://fastapi.tiangolo.com/tutorial/first-steps/) explains this route structure.

### Step 3: Make the browser test pass

Create `/Users/xujingxuan/Documents/Projects/ai-agent-project/tests/e2e/test_demo_smoke.py` with:

```python
from playwright.sync_api import Page, expect


def test_demo_is_reachable(page: Page):
    page.goto("http://127.0.0.1:8001")
    expect(page.get_by_role("heading", name="Checkout demo")).to_be_visible()
```

Open a second terminal in the project directory and run:

```bash
uv run pytest tests/e2e/test_demo_smoke.py -q
```

Expected result: one passing test. This only checks your server and browser setup; it does not validate checkout behavior yet. Playwright's [Python installation guide](https://playwright.dev/python/docs/intro) covers its pytest integration and browser installation.

### Step 4: Establish version-control hygiene

Create a `.gitignore` before adding generated files. Include at least:

```gitignore
.venv/
__pycache__/
.pytest_cache/
.env
.env.*
!.env.example
artifacts/
test-results/
playwright-report/
node_modules/
.DS_Store
```

Initialize Git if this project is not already inside a repository. Commit source code, synthetic fixtures, dependency lockfiles, and documentation. Review `git status` before committing. Put placeholder configuration names in `.env.example`; real API keys belong in the ignored `.env` file or your environment.

**Stop here for your first session if necessary. A running page and one green browser test are a useful first result.**

## 6. Milestone 1: prove the execution foundation

Extend the demo with a checkout form, calculation endpoint, and visible result fields. Keep calculation logic on the server so the page exercises real application behavior.

Implement this in order:

1. A pure calculation function implementing the written money rules.
2. Unit tests with independently specified expected values.
3. A checkout page that calls the calculation endpoint and shows debit, remaining payment, and remaining card balance.
4. A reset operation that restores the same fixture before each test. If the prototype is stateless, explicitly initialize inputs and create a fresh browser context each time.
5. A hand-written Playwright test covering the reference scenario.
6. A separately selectable faulty implementation and a test that exposes its defect.
7. Screenshot/trace collection on failure, plus structured expected and actual values.

Do not calculate your test's expected results by calling the same application function being tested. Write expectations from the requirements.

Use a small scenario table to guide the first tests:

| Subtotal | Discount | Card balance | Expected debit | Expected payment | Expected card remaining |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 100.00 | 20.00 | 80.00 | 80.00 | 0.00 | 0.00 |
| 100.00 | 20.00 | 100.00 | 80.00 | 0.00 | 20.00 |
| 100.00 | 20.00 | 50.00 | 50.00 | 30.00 | 0.00 |

**Done when:** the reference test passes on the correct application, the discriminating test fails on the faulty application, and both behaviors repeat across three clean resets. A screenshot alone is insufficient; retain the assertion and its expected/actual values.

Before committing to a model integration, also perform a small capability check using an available model in your intended provider account: one ordinary response, one schema-valid plan, and one simple tool-call request. Record unsupported capabilities rather than assuming every model offers them. Use the [official Nebius cookbook](https://github.com/nebius/token-factory-cookbook) to find current account/API examples. Exact model availability and hackathon suitability still need confirmation.

## 7. Milestone 2: turn a JSON plan into an executable test

Before asking the model to create tests, decide exactly what your runner can execute.

Start with a few named operations:

```text
open_checkout
set_subtotal
set_fixed_discount
set_gift_card_balance
submit_checkout
```

Your code maps these operations to fixed Playwright locators. The planner supplies values and chooses supported operations; it does not supply arbitrary Python, JavaScript, shell commands, or destination URLs.

An illustrative case could look like this:

```json
{
  "case_id": "CASE-001",
  "classification": "new",
  "requirement_ids": ["REQ-001", "REQ-002"],
  "historical_source_ids": ["BUG-001"],
  "rationale": "Check that a card covering the original subtotal is debited only after the discount.",
  "preconditions": {"fixture_id": "checkout-empty"},
  "steps": [
    {"action": "open_checkout"},
    {"action": "set_subtotal", "amount_cents": 10000},
    {"action": "set_fixed_discount", "amount_cents": 2000},
    {"action": "set_gift_card_balance", "amount_cents": 10000},
    {"action": "submit_checkout"}
  ],
  "expected": {
    "gift_card_debit_cents": 8000,
    "remaining_due_cents": 0,
    "remaining_card_cents": 2000
  }
}
```

This is a proposed schema, not an existing interface. Create the referenced source records before using these IDs.

Validate action names, argument types/ranges, required fields, source IDs, and legal operation order. Use strict types and reject unexpected fields. Validate the complete plan before executing any step, then freeze its expectations for that run.

Save a result containing `run_id`, `case_id`, `attempt_id`, target revision, fixture, timestamps, assertion outcomes, execution errors, and artifact paths. Keep these outcomes distinct:

- `passed`: assertions completed and matched.
- `failed_assertion`: observed behavior differed from a frozen expectation.
- `execution_error`: the browser, environment, or tool failed to complete the check.
- `not_executed`: the case never ran, with a reason.

**Done when:** a manually authored JSON plan executes successfully, unsupported actions are rejected before execution, and each of those outcomes can be represented honestly.

## 8. Milestone 3: add grounded model planning

First supply a small set of documents directly to the model. This isolates planning problems from retrieval problems.

Create three types of source record:

| Type | What to record | How it should influence the plan |
| --- | --- | --- |
| Requirement | Stable ID, source, module, applicability, status, rule | Defines expected behavior |
| Historical bug | Stable ID, provenance, affected versions, trigger, observation, verified resolution | Suggests a risk worth checking |
| Existing test | Stable ID, covered requirements, fixture, steps, expectations, applicability | Supports reuse and overlap detection |

Label invented historical bugs as synthetic. Do not present your own fixtures as real customer incidents.

Give the planner the current goal, applicable requirements, available history, test inventory, and action schema. Ask for up to three cases, source references, a rationale, and a `reuse`, `extension`, or `new` classification.

Parse the response through the same validator as the manual plan. A schema-valid response still needs applicable sources and justified expectations. Deduplicate exact cases; disclose uncertain semantic overlap. Allow a bounded correction attempt for invalid output, counted against the run's model-call limit.

**Done when:** generated plans execute through the existing runner, cite real applicable records, and handle missing or ambiguous requirements by leaving affected cases unexecuted with an explanation.

## 9. Milestone 4: add retrieval and durable storage

Now replace the hand-selected historical context with retrieval. Start with keyword search so you have an understandable baseline. Then add semantic search and compare them.

Use PostgreSQL for source records, runs, attempts, and events. Add pgvector for embeddings; the [official pgvector repository](https://github.com/pgvector/pgvector) documents setup and similarity queries. A local container is one option; introduce Docker here if useful, after the browser prototype works.

Build this sequence:

```text
Local Markdown/JSON records
    → validate metadata
    → import by stable ID and content hash
    → index keywords and embeddings
    → filter by module and version applicability
    → retrieve candidate records
    → supply context with source IDs to the planner
```

For short synthetic records, use one record per chunk initially. Store the embedding model ID and vector dimension. Reimporting unchanged records should not duplicate them; changed records must replace or invalidate stale index entries. Keep the source documents as the source of truth.

Start with exact vector search on this small dataset. Tune indexes or add reranking only if measurements justify the extra work.

Optional follow-up: the [Jev integration plan](JEV_INTEGRATION_PLAN.md) details relevance scoring for historical records. First freeze the retrieval baseline, then run Jev in shadow mode without changing planner context. Enable reranking only after development-set checks; keep current requirements, the existing test inventory, and executable assertions outside its selection authority. This experiment is not a prerequisite for the milestones below.

Preserve the knowledge snapshot, prompt/configuration identifiers, target revision, and selected model with each run. Write execution results immediately, before asking the model for analysis. Local JSON artifacts are adequate for an early prototype; the first release also needs durable run metadata and history.

**Done when:** repeated import is idempotent, applicable records are traceable, empty retrieval works, and superseded/conflicting records are handled explicitly.

## 10. Milestone 5: connect MCP and bounded orchestration

Wrap the tested execution functions in a small MCP server. Begin with local stdio transport and use the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) for server/client examples.

Proposed tool responsibilities:

| Tool | Responsibility |
| --- | --- |
| `reset_environment` | Prepare the configured fixture for a run |
| `run_test_plan` | Execute a validated plan against that run's configured target |
| `get_test_result` | Fetch persisted attempt results |
| `get_logs` | Fetch allowed, redacted execution logs |

Every call carries a run identifier. The service must reject unknown runs, unsupported operations, and access outside the configured target/artifact locations. Demonstrate the same server from a separate minimal client before integrating it into the main workflow.

Then place the workflow in LangGraph. It supports explicit state and mixtures of deterministic and model-driven steps; see the [official overview](https://docs.langchain.com/oss/python/langgraph/overview). You do not need a second agent framework.

Suggested flow:

```text
load_run → retrieve → plan → validate → ready
                                      |
                              user starts execution
                                      |
                               execute via MCP
                                      |
                    collect evidence → analyze → report
```

The model can choose relevant scenarios and request useful follow-up evidence. Ordinary code handles validation, resets, assertions, persistence, and stopping rules.

Use the PRD's proposed limits initially: three tests, six model calls, two retrieval rounds including the initial round, one additional execution attempt per case, 180 seconds per attempt, and a ten-minute run deadline. Count all calls, including repairs and analysis. The total deadline overrides remaining allowances. Persist the stopping reason and completed evidence on exhaustion.

Preserve both attempts after a rerun. Do not change the expected outcome to make a failed case pass. In the report, distinguish observed facts, tentative explanations, and proposed next checks.

**Done when:** the real workflow invokes MCP, a separate client can invoke it, limits are enforced by code, and partial/error outcomes produce useful reports.

## 11. Milestone 6: add the API, worker, and product UI

Move long-running execution into a separate worker process. The API creates a persisted run; the worker claims it and stores progress/results. A single worker and database-backed job table are sufficient initially. UI polling can be your first progress mechanism.

On restart, reconcile unfinished runs and mark abandoned work as interrupted. Automatic resume is P1 in the PRD. Closing the browser should not stop backend execution, and completed results should survive a backend restart.

Suggested API endpoints, to implement later:

| Endpoint | Purpose |
| --- | --- |
| `POST /runs` | Create a planning job |
| `GET /runs/{id}` | Read lifecycle, plan, progress, and results |
| `POST /runs/{id}/execute` | Start a validated ready plan |
| `GET /runs` | List saved runs |
| `GET /runs/{id}/report` | Export Markdown and/or structured results |

Build only three React views: task setup, run detail, and history. The detail view should expose sources, expected/actual values, artifacts, and usage. Display run lifecycle separately from individual test outcomes: a completed run may contain failed tests.

**Done when:** someone can create a run, inspect its plan, execute it, refresh the page, revisit results, and export the evidence without losing state or exposing credentials.

## 12. Evaluate throughout development

Create a tiny development task set during Milestone 1, so every layer has repeatable examples. Expand it for final evaluation after the pipeline is stable.

Follow the PRD's four comparison conditions:

| Condition | Context |
| --- | --- |
| A | Current requirements and existing tests |
| B | A plus keyword-retrieved history |
| C | A plus semantic/hybrid-retrieved history |
| D | A plus all frozen historical records, when they fit |

Keep the model, tools, fixtures, execution budget, and orchestration policy consistent. Measure actual token use and latency separately. Condition D helps test whether retrieval is needed for such a small dataset.

Prepare held-out tasks for known regression, related-risk transfer, and distractor/conflict cases. For transfer tasks, withhold the target defect's exact trigger, fix, and diagnosis. The agent must not see evaluator labels or benchmark answers. Freeze these tasks after development tuning.

The PRD suggests 12 held-out tasks with three repeats per model-driven condition. Budget the workload before running it: 12 tasks × 4 conditions × 3 repeats is 144 runs for one target variant per task; running a separate correct and faulty variant for every task doubles that to 288. Actual counts depend on which variants apply.

Report defect detection, false positives on correct controls, execution completion, useful new cases, citation validity, tokens/calls, and duration. Include raw counts, per-task results, and variation across repeats. Infrastructure failures are not detected defects. A negative or inconclusive result is still a valid engineering finding.

## 13. Suggested repository layout

This is a target structure to grow into, not a list of files that already exist. Keep shared Python code in one environment initially.

```text
ai-agent-project/
├── PRD.md
├── GETTING_STARTED.md
├── README.md                  # Actual install/run commands as they become available
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── demo_app/                  # Checkout application under test
├── qa_agent/
│   ├── schemas.py             # Plans, source records, results
│   ├── runner.py              # Supported actions and assertions
│   ├── planner.py             # Model request and output validation
│   ├── retrieval.py           # Keyword/semantic context selection
│   ├── workflow.py            # Orchestration and limits
│   ├── storage.py             # Durable records
│   ├── mcp_server.py          # Testing tools
│   ├── api.py                 # Product HTTP endpoints
│   └── worker.py              # Background execution
├── frontend/                  # Agent UI, added later
├── knowledge/                 # Curated agent-visible records
├── evaluation/                # Development/held-out manifests and evaluator
├── tests/                     # Tests of your implementation
├── artifacts/                 # Generated run evidence; ignored by Git
└── docs/                      # Rules, architecture, decisions, evaluation report
```

The evaluator and runner may access hidden fixtures; only the curated context is passed to the model. Separate folders alone do not enforce this boundary—your context-building code must enforce it.

## 14. Plan your first seven work sessions

Treat these as sessions with visible deliverables, not guaranteed calendar days. Split a session if you need time to learn its prerequisite.

| Session | Deliverable | Stop condition |
| --- | --- | --- |
| 1 | Environment, tiny server, browser smoke test | One passing browser test |
| 2 | Written rules and correct checkout calculator | Reference values match independent tests |
| 3 | Checkout page and hand-written browser test | Real UI flow passes after reset |
| 4 | Faulty variant and discriminating scenario | Same expectation catches the injected bug |
| 5 | JSON schema, action runner, saved evidence | Valid plan runs; invalid plan is rejected |
| 6 | Small curated source dataset and provider capability check | IDs/provenance are explicit; model capability is recorded |
| 7 | First model-generated supported plan | Plan validates, cites sources, and executes |

After that, proceed through retrieval, MCP/orchestration, worker/UI, and final evaluation. Do not commit to a hackathon schedule until you confirm the event, current rules, available hours, and inference/hosting budget.

When you need implementation help, request one verifiable increment. For example:

> Implement the first execution milestone from GETTING_STARTED.md: the checkout rules, a minimal local checkout app, resettable fixtures, a separately selectable faulty variant, and a hand-written Playwright test. Use integer cents. Show how the same frozen expectation passes on the correct version and fails on the faulty version across three clean resets. Explain the files and run commands.

## 15. Common blockers and the next useful action

| Symptom | What to check |
| --- | --- |
| `uv: command not found` | Finish uv installation, reopen the terminal, and check `uv --version` |
| Browser executable missing | Run `uv run playwright install chromium` in the project environment |
| Connection refused on port 8001 | Ensure the demo server is running and its port matches the test URL |
| Python cannot import `demo_app` | Run commands from the project root and confirm the module file exists |
| Correct and faulty versions both pass | Check that the fixture exposes the intended defect and the test asserts the affected field |
| Model returns invalid plans | Inspect schema/response, reduce allowed actions, and enforce a bounded correction path |
| Model invents requirements | Check cited IDs and applicability; leave undefined expectations unresolved |
| Retrieval seems irrelevant | Inspect source records, filters, and keyword results before changing embeddings |
| Browser failure is described as a product bug | Fix result classification before adding diagnosis features |
| Closing the UI loses the run | Move execution to the worker and persist lifecycle/events |
| Too many unfinished components | Return to the earliest unmet milestone exit condition |

Your next concrete action is Section 5: get the local page running and the first browser test passing. That gives every later component a working foundation.
