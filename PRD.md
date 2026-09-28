# Casewake — Product Requirements Document

> **Direction update (September 28, 2026):** The user wants Casewake to test a configured, complete product using its PRD or design specification as the basis for a reviewable test-case library. The checkout scenario below is an earlier proposal and an isolated learning fixture, not the selected demo. See [the real-product direction](docs/real_product_direction.md). The draft requirements and acceptance criteria below need a full pass against this updated target before implementation.

| Field | Value |
| --- | --- |
| Version | 0.1 |
| Status | Draft for implementation planning |
| Date | September 22, 2026 |
| Primary project objective | Build a credible portfolio project for AI application engineering roles |
| Secondary objective | Deliver a working hackathon submission |
| Working product name | Casewake |

## 1. Purpose and decision status

This document defines the proposed first release: its users, scope, behavior, evidence requirements, and acceptance criteria. It translates the broader ideas in [the original project exploration](agentic_rag_software_testing_assistant.md) into a bounded product proposal. That document remains background material; its seven-version roadmap is not a requirement to implement every framework or feature.

**Confirmed goals:** prioritize employability, gain practical experience with agents, RAG, vector databases, and MCP, and participate in a Nebius/NVIDIA hackathon.

**Current direction:** test a configured complete product using its PRD or design specification as the requirements source. The earlier small e-commerce application is only a technical fixture. One main agent, structured executable plans, and a focus on regression coverage gaps remain proposed implementation choices.

**Unvalidated assumptions:** target users need this workflow; historical QA knowledge improves outcomes; the candidate hackathon identified in Section 13 is the intended event. No user research, implementation benchmarks, or performance improvements have been established.

**Optional Jev experiment (planned September 25, 2026):** [Jev integration plan](JEV_INTEGRATION_PLAN.md) specifies historical-record relevance scoring after retrieval, progressing from shadow evaluation to optional reranking. It defines inputs, fallback behavior, separate inference budgets, and controlled comparisons. This is an optional extension; it does not replace P0 requirements, current-rule authority, or deterministic assertions. The base six-call budget below remains unchanged; the experimental profile explicitly allows up to six main-model attempts plus two Jev attempts and reports all usage.

## 2. Product summary

QA Memory Agent helps developers identify regression scenarios that existing tests may miss. It combines current requirements, historical defects, and existing tests to propose a small, evidence-backed test plan, execute supported cases, and produce an auditable report.

The first release supports one configured application and a limited set of business operations. Its principal contribution is the connection between historical knowledge, test selection or expansion, and executable evidence.

**Product promise:** explain why a test matters, execute it against a known environment, and show what the result establishes.

**Research hypothesis:** under a fixed execution budget, relevant historical QA knowledge can improve defect detection over the same agent without that knowledge. The evaluation must also measure cases where retrieval is unhelpful or misleading.

## 3. Users and problem

### Primary user: a developer validating a business change

The developer understands the feature being changed but may not remember past incidents or all interactions with adjacent features. Before merging a change, they want a small set of relevant regression checks and usable evidence if a check fails.

Job to be done:

> When I change a business flow, help me identify and validate important cases I might overlook, using the product's existing requirements and defect history.

### Secondary user: a QA engineer maintaining regression coverage

The QA engineer wants to convert defect knowledge into tests, identify gaps in existing coverage, and inspect failures without manually reconstructing the history of each issue.

### Why existing tests are not always enough

The proposed value is strongest when a recorded defect has no automated regression test, an existing test covers only its original trigger, or a new requirement introduces a related combination of conditions. If an existing test already covers the risk, the system should reuse it rather than generate a duplicate.

An empty or poorly maintained knowledge base limits the value of the product. The first release includes a curated dataset to make the workflow reproducible; enterprise data ingestion is outside its scope.

### Early validation

Recruit two or three developers or QA engineers for exploratory walkthroughs. Record which suggested tests they would retain, which they reject, and whether they can understand the evidence without assistance. This is qualitative feedback, not proof of broad market demand. Recruitment and outreach are future work.

## 4. Goals and non-goals

### Release goals

- Complete a requirement-to-execution-to-report workflow on the configured application.
- Trace test suggestions to current requirements and relevant historical evidence.
- Distinguish reused tests from newly proposed cases and explain potential coverage gaps.
- Preserve factual execution evidence separately from model-generated interpretation.
- Compare retrieval approaches using reproducible tasks and an explicit resource budget.
- Demonstrate practical agent orchestration, vector retrieval, and reusable MCP tools.
- Let another developer run the project and evaluation using documented setup instructions.

### Non-goals for the first release

- Testing arbitrary applications without a configured target, supported execution adapter, and controlled test environment; testing production payment systems.
- Replacing a QA team or claiming complete coverage.
- Unrestricted generated-code execution, autonomous application fixes, or self-healing assertions.
- Guaranteed root-cause identification.
- Multiple collaborating agents, model fine-tuning, or reinforcement learning.
- Enterprise authentication, multi-tenant SaaS, device farms, or distributed browser scaling.
- Live Jira/GitHub synchronization, automatic PR creation, or external issue submission.
- Automatic promotion of model-generated diagnoses into trusted historical knowledge.

## 5. Reference scenario and user journey

### Earlier checkout example (not selected as the demo)

The original proposal used a small checkout application with explicit rules for discounts and gift cards. It can remain an isolated technical fixture with resettable data and controlled faulty variants, but it is not the chosen real-product pilot. The intended pilot is described in [the real-product direction](docs/real_product_direction.md).

Proposed rule fixture: an order totals 100 units, a discount reduces it to 80, and a gift card has a balance of 80. Discounts apply before gift-card redemption. Expected gift-card debit is 80; additional payment is zero. Currency handling and rounding rules must be specified before implementation.

A historical defect describes an incorrect partial gift-card payment calculation. The current requirement introduces discount ordering. The agent should consider boundary conditions created by combining these facts. It must not infer expected behavior solely from the application's current output.

### Main journey

1. The user selects the configured application version, a supported feature, and a testing goal. Version labels shown to the agent must not reveal hidden benchmark defects.
2. The system retrieves current rules, related historical defects, and existing tests.
3. The system proposes up to three tests, with preconditions, steps, expected results, sources, and a reuse/new-case label.
4. The user can inspect the plan and start execution. This is a usability control; the release does not require an enterprise approval workflow.
5. The system prepares isolated test data and executes supported steps through testing tools.
6. For failures, the agent can request additional evidence or one controlled rerun within the configured budget.
7. The report presents results, artifacts, relevant history, and any unresolved questions.
8. The user can revisit the completed run or export its report and structured test plan.

### Alternate outcomes

| Situation | Required behavior |
| --- | --- |
| No relevant historical evidence | Continue from available requirements and label the run as having no useful historical context |
| Ambiguous expected behavior | Identify the missing rule and leave the affected case unexecuted until clarified |
| Unsupported action or feature | Explain the boundary; do not invent an executable capability |
| Conflicting or obsolete records | Show the conflict or exclusion; do not silently treat old behavior as current truth |
| Browser or environment failure | Report an execution error, not a confirmed product defect |
| Model or tool budget exhausted | Stop with a partial report and an explicit stopping reason |
| Interrupted process | Retain completed evidence and mark the unfinished run as interrupted |

## 6. Functional requirements

P0 requirements define the first release. P1 requirements are optional follow-up work after the P0 workflow is stable.

| ID | Priority | Requirement | Acceptance criteria |
| --- | --- | --- | --- |
| FR-01 | P0 | Import a curated knowledge dataset from local Markdown and JSON files | A documented command validates required metadata and reports rejected records; reimporting unchanged records does not create duplicates |
| FR-02 | P0 | Retrieve requirements, historical defects, and existing tests | Retrieved records include source IDs and applicable context; version/module filters are applied where metadata permits; empty results are supported |
| FR-03 | P0 | Generate a structured test plan | Each case contains preconditions, supported actions, expected outcomes, requirement references, and rationale; historical sources are cited when used |
| FR-04 | P0 | Recognize existing coverage | Each case is labeled as reuse, extension, or new; exact duplicates are removed, while uncertain semantic overlap is disclosed |
| FR-05 | P0 | Execute supported cases | Validated steps map to configured Playwright operations; unsupported steps are rejected before execution; expectations are frozen for the run |
| FR-06 | P0 | Capture execution evidence | Every executed case records assertion outcomes and a run/test identifier; failures include available logs, screenshots, or traces, and disclose missing artifacts |
| FR-07 | P0 | Provide bounded failure analysis | Reports distinguish observed facts, failure-category hypotheses, and possible next checks; insufficient evidence is an allowed result |
| FR-08 | P0 | Expose testing capabilities through MCP | The workflow uses the MCP service; a separate minimal client can invoke the same service; invalid arguments and tool errors return structured responses |
| FR-09 | P0 | Persist run history | Refreshing or closing the browser does not discard an active backend run; completed evidence survives backend restart; unfinished runs have an honest interrupted status |
| FR-10 | P0 | Enforce execution limits | Configured call, test, timeout, and retry limits are enforced by application code; exhaustion produces a stopping reason and preserves partial results |
| FR-11 | P0 | Present and export reports | Users can inspect sources, expected/actual results, artifacts, and usage; Markdown reports and JSON plans/results can be exported without credentials |
| FR-12 | P0 | Run reproducible comparisons | A documented evaluation command runs named configurations against the same task manifest and exports per-task results plus aggregate metrics |
| FR-13 | P1 | Resume interrupted work | Recovery reconciles external operations before rerunning them and does not duplicate a known completed action |
| FR-14 | P1 | Integrate with CI | A non-interactive command executes a defined suite and returns documented exit codes and artifacts |

## 7. Product experience

The interface should answer four questions: what is being tested, why these cases were selected, what happened, and what is still uncertain.

The first release needs a task setup view, a run detail view, and a small history list. Run details show the plan, compact progress events, retrieved evidence, and case results. Show concise decision summaries and tool activity rather than hidden model reasoning.

Use separate labels for:

- **Run lifecycle:** queued, planning, ready, executing, analyzing, completed, partial, interrupted, or error.
- **Case outcome:** passed, failed assertion, execution error, or not executed.
- **Analysis status:** supported hypothesis, tentative hypothesis, or insufficient evidence.

A completed run can contain failed tests. An assertion failure establishes a mismatch with the specified expectation; it does not, by itself, establish the implementation root cause. A rerun must preserve its original attempt and must not automatically erase a failure or declare it flaky.

## 8. Knowledge and evidence model

| Entity | Minimum information |
| --- | --- |
| Requirement | ID, source, module, version/applicability, business rule, status |
| Historical defect | ID, source, affected versions, trigger, observed behavior, verified resolution if available |
| Existing test | ID, covered requirements/risks, preconditions, steps or executable reference, applicability |
| Planned case | ID, reuse/extension/new label, expected results, source references, supported steps |
| Run | ID, target revision, knowledge snapshot, model/prompt/configuration identifiers, limits, lifecycle, usage |
| Test attempt | Run/case/attempt IDs, data fixture, assertions, timestamps, execution errors, artifact references |
| Diagnosis | Supporting evidence IDs, candidate category/cause, uncertainty, proposed verification |

Requirements define intended behavior. Historical defects suggest risks. Existing tests represent documented checks, not proof of complete coverage. Execution records describe specific observations.

Source records remain the source of truth; vector entries are searchable indexes that can be rebuilt. Updating a source must replace or invalidate its stale indexed content. Each run preserves the knowledge snapshot needed to interpret its report.

Store raw execution evidence immediately. Store model diagnoses as unverified interpretations. For the first release, only deliberately curated records enter the trusted historical dataset; there is no autonomous memory-promotion loop.

## 9. Proposed technical boundaries

These choices support the product requirements and may change after an initial technical spike.

| Component | Proposed choice | Responsibility |
| --- | --- | --- |
| UI | React and TypeScript | Goal entry, progress, evidence, history |
| API | FastAPI | Run creation, status, report access |
| Background execution | A single worker initially | Continue jobs independently of browser requests |
| Orchestration | LangGraph with one main agent | State transitions and bounded tool decisions |
| Persistence and retrieval | PostgreSQL with pgvector plus keyword search | Run metadata, source records, semantic retrieval |
| Tool interface | A small custom MCP service | Validated testing operations and artifact access |
| Test runner | Playwright in an isolated environment | Deterministic operations, assertions, evidence capture |
| Inference | A suitable NVIDIA model through Nebius Token Factory | Planning and evidence-based interpretation |

The agent chooses relevant risks and follow-up evidence. Application code validates arguments, enforces budgets, resets environments, evaluates assertions, and persists outcomes.

Suggested MCP capabilities are `run_test_plan`, `get_test_result`, `get_logs`, and `reset_environment`. Exact schemas belong in the technical design. Every operation should carry a run identifier. MCP is an interface protocol; the implementation remains responsible for execution isolation and access boundaries.

Plans use supported structured actions rather than unrestricted model-generated code. Document this limitation in the UI and README. Testing infrastructure, graph libraries, and model serving should be reused; custom work should focus on knowledge handling, risk expansion, evidence traceability, and evaluation.

## 10. Reliability, resource, and data requirements

- Each execution starts from a known fixture, with one application version per run and no cross-run test-data contamination.
- Infrastructure errors and assertion failures remain distinct throughout storage, reports, and evaluation.
- Credentials are not included in model context, exported reports, or committed fixtures. First-release data is synthetic or explicitly reusable public data.
- Browser and tool actions are restricted to the configured testing environment. Retrieved text cannot expand those permissions.
- Every tool call records its name, validated inputs, outcome, duration, and run ID. Retained logs must redact credentials.
- Model output is schema-validated. Invalid plans may be corrected within the same finite call budget; otherwise the run stops with a useful error.
- Application code must not weaken an expected result, skip a failing assertion, or modify the target application to produce a passing outcome.

**Initial proposed defaults, subject to the technical spike:** three planned tests per run, six total model calls, two retrieval rounds including the initial retrieval, one additional execution attempt per case, 180 seconds per attempt, and a ten-minute total run deadline. The total deadline overrides remaining per-step budgets. These are configuration proposals, not measured performance claims.

Record input/output tokens, model-call count, execution duration, and available cost estimates. Cost estimates must include their pricing source/date; unavailable pricing is shown as unavailable rather than zero. Latency and reliability targets should be set after the first end-to-end measurements.

## 11. Evaluation plan

### Questions

1. Does historical knowledge improve useful test selection or expansion?
2. Does semantic retrieval add value over keyword search or supplying the complete small knowledge base?
3. How often do irrelevant or obsolete records degrade results?
4. What execution reliability and resource cost accompany any observed benefit?

### Task groups and data split

- **Known regression:** the historical defect is available; measure conversion of known knowledge into a test.
- **Related risk transfer:** related history is available, but the target defect's trigger, diagnosis, and fix are withheld.
- **Distractor/conflict:** include irrelevant records and explicitly superseded rules; measure whether the system respects current requirements.

Use a separate development set for prompt and retrieval tuning. Freeze evaluation tasks, expected outcomes, and knowledge snapshots before the final comparison. Agent-visible logs may naturally reveal runtime symptoms; hidden defect labels, expected benchmark answers, and target-fix records must not be supplied to the agent.

An initial exploratory evaluation can use 12 held-out tasks, distributed across these groups, each with a correct control version and a faulty variant where applicable. Repeat model-driven runs three times. These are proposed dataset sizes; results from this small set do not establish general performance across applications. Clearly label injected defects, and add a real historical case only if its source and reproduction can be verified.

### Comparison configurations

| Configuration | Context access |
| --- | --- |
| A: No historical retrieval | Current requirements and existing test inventory |
| B: Keyword retrieval | A plus historical records retrieved with keyword search |
| C: Semantic/hybrid retrieval | A plus historical records retrieved with the proposed retrieval method |
| D: Full context, when feasible | A plus the complete frozen historical dataset if it fits the context limit |

All groups use the same model, tools, fixtures, test-execution limit, and orchestration policy. Record actual token use and latency; equal test budgets do not imply equal inference costs. Full-context results test whether retrieval is necessary at this dataset size. If dynamic retrieval is later evaluated, isolate that change in an additional comparison rather than attributing all gains to RAG.

### Metrics

| Metric | Definition |
| --- | --- |
| Defect detection rate | Eligible faulty tasks in which a test exposes the labeled defect through a correct assertion, divided by all eligible faulty tasks; execution errors do not count as detections |
| False-positive rate | Correct-control tasks with at least one incorrect assertion failure, divided by evaluated correct-control tasks; report infrastructure errors separately |
| Execution completion rate | Attempted cases that reach a valid assertion outcome, divided by attempted cases |
| Useful new-case count | Non-duplicate proposed cases accepted against a predefined human-reviewed rubric, reported separately from reused tests |
| Citation validity | Sampled factual claims whose cited records support them and apply to the target context, divided by sampled claims |
| Resource cost | Token use, model/tool calls, wall-clock time, and available cost estimates per run |

Publish raw numerators and denominators, per-task outcomes, variability across repeats, and representative failures. Do not rely solely on an LLM judge, count multiple tests for the same defect as multiple discoveries, or describe an observed uplift as statistically established without supporting analysis.

No improvement percentage is promised. The engineering release may be complete with a negative experimental result; claims about superior defect detection must be withheld or narrowed accordingly.

## 12. Milestones and release acceptance

The following is a proposed sequence, not a committed schedule. Available weekly hours and team size are unknown.

| Milestone | Exit condition |
| --- | --- |
| M1: Execution foundation | Rules and fixtures are explicit; a hand-authored test passes on the correct version and fails on its faulty counterpart across three clean resets; selected model passes basic schema/tool-call checks |
| M2: Grounded planning | Imported knowledge is traceable; supported test plans cite applicable rules; empty and conflicting retrieval cases behave as specified |
| M3: End-to-end agent | A real workflow invokes MCP tools, executes tests, captures evidence, and enforces limits; partial/error paths are visible |
| M4: Product and evaluation | UI/history/export work; frozen baseline comparisons run; results and limitations are documented |
| M5: Delivery | Another developer can reproduce the demo; English documentation and presentation materials accurately match the implemented behavior |

Release acceptance requires all P0 requirements to pass, the reference scenario to be reproducible, and evaluation artifacts to be available. If execution is unstable, stop feature expansion. If retrieval adds no measurable value, investigate the task/data design and publish the finding before adding further agent complexity.

### Portfolio deliverables

- Working application with a documented local setup and a shareable demo or test build.
- Architecture explanation, supported-scope statement, and design tradeoffs.
- Curated dataset with provenance and a reproducible evaluation command.
- Reports showing successful detection, a correct control, and at least one limitation or failure.
- A short demo and factual resume-ready description with measured results only.

## 13. Candidate hackathon alignment

The intended event still needs confirmation. The following notes apply only to the **Nebius x NVIDIA Global AI Hackathon** identified during research, not to every Nebius/NVIDIA event.

According to the [official rules](https://nebiusglobalaihackathon.devpost.com/rules), checked September 22, 2026:

- Submission closes October 30, 2026 at 10:00 a.m. PDT, or 1:00 p.m. Toronto time.
- A project must use an NVIDIA open-source model and either call Token Factory during runtime or execute on Nebius AI Cloud.
- Deliverables include a working demo/test build, public open-source repository with setup instructions, and a public YouTube demonstration under three minutes. Materials require English or English translations.
- The project must remain accessible for evaluation through the judging period, which ends December 15, 2026.

Proposed track: Coding and Agentic Engineering if the implementation fits its stated sandbox-based development/testing workflow; otherwise assess Best Apps and Agents. Confirm the event and track before treating these constraints as the release calendar. Registration, eligibility, and submission are separate future actions.

The demonstration should show a requirement, relevant historical evidence, a resulting test, an actual failure on a labeled faulty version, and the same expectation passing on the correct version. Historical regression and transfer to a new boundary case must be described accurately. Measured comparisons belong in the accompanying project materials.

## 14. Risks and open decisions

| Risk | Response |
| --- | --- |
| Thin or artificial knowledge makes retrieval gains trivial | Separate known regressions from transfer tasks; include distractors and full-context/keyword baselines |
| Browser automation consumes the project timeline | Limit supported operations and freeze the demo app before expanding scope |
| Existing tests already cover every meaningful scenario | Reuse those tests honestly; test the gap-expansion hypothesis on explicit uncovered combinations |
| The selected model produces unreliable tool arguments | Run an early capability spike; validate schemas and bound correction attempts |
| Confident but unsupported diagnosis | Separate observations from hypotheses and allow insufficient evidence |
| Too many technologies prevent completion | Keep one main agent, one database, one worker, and one target application initially |
| A polished demo overstates generality | Publish scope, fixtures, raw outcomes, and known limitations |

Resolve before committing to implementation scope:

1. Which hackathon and track are intended?
2. How many development hours per week and how many contributors are available?
3. Which demo application and business rules will serve as the initial target?
4. Which NVIDIA model is available and suitable within the actual inference budget?
5. Will PostgreSQL with pgvector meet the learning objective, or is a separate vector database a deliberate priority?
6. What hosting and inference budget can sustain the demo through evaluation?

The next technical design should define schemas, tool contracts, worker behavior, and execution isolation against these requirements. Product claims should remain bounded by what the eventual implementation and evaluation demonstrate.
