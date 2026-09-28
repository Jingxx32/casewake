# Agentic RAG Software Testing Assistant

## 1. Project Overview

### Working Title
**Agentic RAG Software Testing Assistant**

### One-Sentence Description
A knowledge-grounded AI testing system that uses product documentation, historical bugs, previous test cases, and test execution data to plan tests, execute them through tools, diagnose failures, and generate reports.

### Core Idea
The project combines:

- **RAG** for retrieving product and QA knowledge
- **LLM agents** for reasoning and decision-making
- **Tool calling** for test execution and supporting actions
- **LangGraph** for orchestration, state, branching, retries, and reflection
- **MCP** for exposing testing capabilities through a standardized interface
- **Playwright** or similar tooling for browser test execution
- **FastAPI** for the backend
- **React** for the UI
- **Vector database / hybrid retrieval** for knowledge retrieval

The key design goal is not simply to build an AI that writes tests. The system should use a company's accumulated QA knowledge to generate better tests and diagnose failures more effectively.

---

# 2. Problem Statement

Traditional AI testing demos often follow this pattern:

```text
User prompt
   ↓
LLM
   ↓
Generate test cases
```

This project aims to build a more useful system:

```text
User requirement
   ↓
Retrieve relevant QA knowledge
   ↓
Plan tests
   ↓
Execute tests
   ↓
Analyze results
   ↓
If failure occurs:
    retrieve similar bugs / previous failures
   ↓
Diagnose likely cause
   ↓
Generate report
```

The central product question is:

> Can an AI testing agent use accumulated QA knowledge—requirements, historical bugs, previous tests, failures, and logs—to generate higher-value tests and provide more accurate failure diagnosis?

---

# 3. Recommended Positioning

## Primary Positioning
**Knowledge-Grounded Agentic Testing**

Alternative names:

- **Agentic RAG Software Testing Assistant**
- **AI Test Engineer**
- **QA Memory Agent**
- **Knowledge-Grounded Testing Agent**

## Recommended Portfolio Description

> An AI testing agent that retrieves product requirements, historical defects, and previous test cases; generates context-aware test plans; executes tests through external tools; and diagnoses failures using logs and historical QA knowledge.

This positioning is stronger than a generic:

> "AI agent that generates tests."

because many commercial products already support test generation and execution.

The differentiating idea is:

> **AI that uses an organization's QA memory.**

---

# 4. Core System Architecture

```text
                    React UI
                       │
                       ↓
                FastAPI Backend
                       │
                       ↓
                LangGraph Agent
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       RAG Layer    Reasoning     MCP Client
          │                          │
          ↓                          ↓
      Vector DB                  MCP Server
   ┌──────┼───────┐          ┌──────┼─────────┐
   ↓      ↓       ↓          ↓      ↓         ↓
  PRD   Bugs   Past Tests  run_test logs screenshot
                          browser_action reset_env
```

## Technology Responsibilities

| Technology | Responsibility |
|---|---|
| RAG | Give the agent product and QA knowledge |
| Vector DB | Store embeddings / searchable QA artifacts |
| LangGraph | Control workflow, state, branching, retry, reflection |
| Tool Calling | Let the agent choose actions dynamically |
| MCP | Standardize access to testing tools |
| Playwright | Perform browser testing |
| FastAPI | Expose backend APIs and agent execution |
| React | User interface |
| LLM | Reasoning, planning, diagnosis, report generation |

---

# 5. Knowledge Base Design

The RAG knowledge base can contain:

## Product Knowledge
- Product requirements
- PRDs
- Feature documentation
- API documentation
- Release notes
- Product rules
- User flows

## QA Knowledge
- Historical bugs
- Previous test cases
- Previous failed tests
- Regression cases
- Known edge cases
- Test execution reports
- Testing guidelines
- Historical logs

## Optional Code Context
- Code documentation
- Function/module summaries
- Commit summaries
- Known ownership or subsystem information

---

# 6. Two Core RAG Use Cases

## 6.1 Planning RAG

Question:

> What should the system test?

The agent retrieves:

```text
Requirements
Historical bugs
Previous test cases
Known edge cases
```

Example:

```text
User:
"Test the checkout flow."
```

RAG might retrieve:

```text
Requirement:
Coupon and gift card can be used together.

Historical bug:
Checkout crashed when gift card balance was lower than order value.

Existing tests:
- normal credit card payment
- invalid card
- expired card
```

The agent can then generate:

```text
Existing tests
+
new edge cases
+
historical regression tests
```

---

## 6.2 Diagnostic RAG

Question:

> Why did this test fail?

The agent retrieves:

```text
Historical bugs
Previous failures
Logs
Known issues
Relevant documentation
Similar test failures
```

Example workflow:

```text
Test failed
   ↓
get_logs()
   ↓
retrieve similar bugs
   ↓
retrieve previous failures
   ↓
reason about root cause
   ↓
generate diagnosis
```

---

# 7. LangGraph Workflow

A natural testing graph:

```text
START
  ↓
retrieve_context
  ↓
plan_tests
  ↓
review_plan
  ↓
execute_tests
  ↓
analyze_result
  ↓
      ┌── PASS ──→ generate_report
      │
      └── FAIL
            ↓
      retrieve_similar_bugs
            ↓
          diagnose
            ↓
      generate_report
```

## Example State

```python
state = {
    "requirement": "",
    "retrieved_docs": [],
    "test_cases": [],
    "test_results": [],
    "logs": [],
    "similar_bugs": [],
    "diagnosis": "",
    "report": ""
}
```

---

# 8. Reflection / Self-Improving Agent Design

"Self-improving" should not be interpreted as autonomous model retraining.

Instead, use structured reflection:

```text
Generate test plan
      ↓
Review test plan
      ↓
Are important cases missing?
      ↓
Revise plan
      ↓
Execute
```

Example:

Initial plan:

```text
1. valid login
2. invalid password
3. empty password
```

Reflection may identify:

```text
Missing:
- invalid email format
- locked account
- rate limiting
```

Then the agent improves the plan before execution.

This directly maps to:

```text
evaluate
→ feedback
→ refine
```

---

# 9. Multi-Agent Design

Avoid creating too many agents.

A strong initial design uses only three:

## 1. Test Planner
Responsibilities:

- Retrieve requirements
- Retrieve historical bugs
- Retrieve previous tests
- Generate test plan
- Perform optional reflection

## 2. Test Executor
Responsibilities:

- Run tests
- Control browser
- Capture screenshots
- Collect logs
- Reset environment

## 3. Failure Analyzer
Responsibilities:

- Retrieve similar historical failures
- Retrieve relevant bugs
- Analyze logs
- Generate probable root cause
- Produce debugging suggestions

Architecture:

```text
Test Planner
     ↓
Test Executor
     ↓
Failure Analyzer
```

### Why Not Use Many Agents?

Avoid designs such as:

```text
Planner Agent
Research Agent
RAG Agent
Browser Agent
Screenshot Agent
Logging Agent
Reviewer Agent
Report Agent
```

This often creates complexity without meaningful benefit.

Use multi-agent architecture only where separation of responsibilities is useful.

---

# 10. MCP Design

## Goal

Expose testing capabilities through a standard protocol.

Example:

```text
AI Testing Agent
       ↓
   MCP Client
       ↓
   MCP Server
       ↓
Testing Infrastructure
```

## Example MCP Tools

```text
run_test
get_device
open_browser
browser_action
take_screenshot
get_logs
reset_environment
get_test_result
save_report
```

Possible architecture:

```text
            LangGraph Agent
                   ↓
              MCP Client
                   ↓
          Testing MCP Server
          ├── run_test
          ├── browser_action
          ├── screenshot
          ├── get_logs
          └── reset_env
```

MCP should not be included only as a buzzword.

Its actual purpose is:

> Provide a standardized interface between the agent and testing capabilities.

---

# 11. Tool Calling MVP

The first version does not need LangGraph or multi-agent logic.

Possible tools:

```python
generate_test_case()
run_test()
get_test_result()
get_logs()
save_report()
```

Basic workflow:

```text
User input
   ↓
LLM
   ↓
select tool
   ↓
execute
   ↓
observe result
   ↓
select next tool
```

The important tool-calling pattern:

```text
Python function
      ↓
Tool
      ↓
Bind to LLM
      ↓
LLM selects tool
      ↓
Application executes tool
      ↓
Result returned to LLM
```

Important distinction:

The LLM does **not** directly execute Python.

It produces something conceptually like:

```text
Call:
multiply(a=5, b=8)
```

The application executes the function.

---

# 12. Course-to-Project Mapping

The IBM RAG and Agentic AI Professional Certificate can be used as a development roadmap.

## Course 6 — Fundamentals of Building AI Agents

Use for:

- Tool definition
- Tool descriptions
- Parameter schemas
- Tool calling
- Dynamic tool selection
- Agent basics
- Tool orchestration

### Project Version
**V1 — Tool Calling**

```text
User
 ↓
LLM
 ↓
Testing tools
 ↓
Result
```

---

## Course 7 — Agentic AI with LangChain and LangGraph

Use for:

- LangGraph workflow
- State management
- Nodes and edges
- Conditional branches
- ReAct
- Reflection
- Reflexion
- Agentic RAG
- Multi-agent orchestration

### Project Versions

**V2 — LangGraph Workflow**

```text
Retrieve
   ↓
Plan
   ↓
Execute
   ↓
Analyze
```

**V3 — Reflection**

```text
Plan
 ↓
Review
 ↓
Improve
 ↓
Execute
```

**V4 — Agentic RAG**

```text
Agent
 ↓
decides what to retrieve
 ↓
RAG
 ↓
reason
 ↓
retrieve again if necessary
```

---

## Course 8 — LangGraph, CrewAI, AutoGen / AG2, BeeAI

Use this course primarily to understand framework trade-offs.

Recommended final project framework:

> **LangGraph**

Why LangGraph fits this project:

- explicit state management
- conditional branching
- retries
- deterministic control
- long-running workflow support
- natural fit for testing pipelines

### CrewAI
Use as a comparison experiment.

Example:

```text
Planner
 ↓
Tester
 ↓
Reviewer
```

### BeeAI / AG2
Learn enough to understand their models and use cases.

They do not need to appear in the final project.

Do not build:

```text
LangGraph + CrewAI + BeeAI + AutoGen
```

just to list frameworks.

A better README statement:

> LangGraph was selected because the testing workflow requires explicit state management, conditional branching, retries, and deterministic control.

---

## Course 9 — Build AI Agents Using MCP

Use for:

- MCP Server
- MCP Client
- MCP Host
- Tools
- Resources
- Prompts
- STDIO transport
- Streamable HTTP
- security considerations
- lifecycle management

### Project Version
**V5 / V6 — MCP Integration**

```text
LangGraph
   ↓
MCP Client
   ↓
Testing MCP Server
   ↓
Playwright / browser / logs
```

---

## Course 10 — RAG and Agentic AI Capstone

Use the capstone concepts for:

- end-to-end RAG system
- retrieval
- reranking
- evaluation
- multimodal ideas
- final system integration
- portfolio presentation

The project's final architecture can combine:

```text
RAG
+
Agent
+
LangGraph
+
MCP
+
Testing Tools
+
React UI
```

---

# 13. Suggested Development Roadmap

## Version 1 — Tool Calling

Goal:

> LLM autonomously selects tools and completes one simple testing workflow.

Build:

- 3–5 Python tools
- basic LLM tool calling
- one test scenario
- test result output

---

## Version 2 — RAG

Add:

- requirements ingestion
- historical bug ingestion
- past test case ingestion
- embeddings
- vector DB
- retrieval pipeline

Goal:

> Test planning is grounded in retrieved QA knowledge.

---

## Version 3 — LangGraph

Add:

- workflow state
- nodes
- conditional edges
- retries
- failure path

Goal:

> Convert the linear agent into a controlled testing workflow.

---

## Version 4 — Reflection

Add:

- test-plan reviewer
- missing-edge-case detection
- plan revision

Goal:

> Improve generated test plans before execution.

---

## Version 5 — Multi-Agent

Add:

- Planner
- Executor
- Analyzer

Goal:

> Separate reasoning responsibilities without overcomplicating the system.

---

## Version 6 — MCP

Add:

- custom MCP server
- MCP client
- testing tools exposed through MCP

Goal:

> Standardize the tool interface.

---

## Version 7 — Full Product

Add:

- React UI
- FastAPI backend
- reporting
- test history
- evaluation dashboard

---

# 14. Possible UI

```text
┌──────────────────────────────────────┐
│ Agentic RAG Testing Assistant        │
├──────────────────────────────────────┤
│ Requirement                          │
│                                      │
│ Test the login flow...               │
│                                      │
│              [ Run Test ]            │
├──────────────────────────────────────┤
│ Retrieved Context                    │
│ - Login requirement                  │
│ - Previous authentication bug        │
│ - Existing regression tests          │
├──────────────────────────────────────┤
│ Test Plan                            │
│ ✓ Empty password                     │
│ ✓ Wrong password                     │
│ ✓ Correct credentials                │
│ ✓ Locked account                     │
├──────────────────────────────────────┤
│ Results                              │
│ ✓ Test 1 passed                      │
│ ✗ Test 2 failed                      │
│                                      │
│ Diagnosis: ...                       │
└──────────────────────────────────────┘
```

---

# 15. Competitive Landscape

## Overall Market Direction

AI testing products are increasingly moving from:

```text
AI writes Selenium code
```

toward:

```text
AI understands intent
       ↓
plans
       ↓
retrieves context
       ↓
runs tools
       ↓
observes results
       ↓
diagnoses failures
       ↓
repairs / retries
```

This is increasingly an **agent architecture** problem rather than a simple test-generation problem.

---

# 16. Competitor Summary

## 16.1 TestSprite

### Publicly Visible Capabilities

- Understand PRD / codebase context
- Generate test plans
- Generate tests
- Execute UI / API / E2E tests
- Analyze failures
- Auto-heal test issues
- Integrate through MCP
- Use AI agents for exploration in some workflows

Approximate product flow:

```text
PRD / Codebase
      ↓
Understand intent
      ↓
Plan tests
      ↓
Generate tests
      ↓
Execute
      ↓
Analyze failures
      ↓
Heal
      ↓
Report
```

### Overlap With This Project

| Capability | TestSprite | Proposed Project |
|---|---|---|
| PRD understanding | Yes | Yes |
| Codebase context | Yes | Optional |
| Test generation | Yes | Yes |
| Test execution | Yes | Yes |
| Failure diagnosis | Yes | Yes |
| Self-healing | Yes | Optional |
| MCP | Yes | Yes |
| Multi-agent | Some public evidence | Yes |
| Historical bug RAG | Not clearly disclosed | Core feature |
| Historical test RAG | Not clearly disclosed | Core feature |
| LangGraph | Not publicly disclosed | Planned |

Important distinction:

> A product can test RAG applications without itself being implemented using RAG.

---

## 16.2 Momentic

Publicly described data/context sources include:

- docs
- guides
- codebase
- Jira
- Linear
- Figma
- session recordings

Capabilities include:

- write tests
- run tests
- update tests
- analyze failures
- auto-heal
- codebase-aware diagnosis
- product terminology / user-flow understanding

Momentic also appears to build product knowledge and user-flow structure.

However:

> Public information does not clearly establish that its internal implementation is a standard embedding + vector DB + RAG pipeline.

---

## 16.3 mabl

Notable capabilities:

- MCP Server
- local and cloud MCP integrations
- test creation
- test execution
- test data querying
- result analysis
- failure analysis
- semantic search over existing flows and tests

This is particularly relevant because semantic retrieval over existing tests resembles RAG-style design.

Approximate concept:

```text
Requirement
    ↓
Semantic retrieval
    ↓
Existing tests / flows
    ↓
LLM
    ↓
New test
```

Public terminology should be kept precise:

> mabl explicitly describes semantic search; that does not necessarily prove a specific internal RAG architecture.

---

## 16.4 BrowserStack

BrowserStack has multiple specialized AI testing agents, including:

- Test Case Generator Agent
- Test Maintenance Agent
- Test Data Generator Agent
- Test Deduplication Agent
- Test Selection Agent
- Test Failure Analysis Agent
- Self-Healing Agent

Its failure analysis can use:

```text
logs
screenshots
metadata
test history
similar failures
stack traces
```

to generate:

```text
root cause
failure category
suggested fix
```

This overlaps strongly with the proposed diagnostic RAG idea.

BrowserStack also provides MCP integration and multi-step orchestration through AI tooling.

---

## 16.5 KaneAI / TestMu AI (formerly LambdaTest ecosystem)

Capabilities include:

- natural-language test generation
- test planning
- execution
- Jira / documentation context
- edge-case generation
- API dependency awareness
- AI root-cause analysis
- MCP integration
- test orchestration

This overlaps strongly with knowledge-aware agentic testing, but public information does not clearly prove its exact internal RAG or orchestration stack.

---

## 16.6 Functionize

Functionize describes an **Agentic Loop** with specialized roles such as:

```text
Create Agent
     ↓
Execute Agent
     ↓
Diagnose Agent
     ↓
Maintain Agent
     ↓
Document Agent
```

It also uses historical test information for failure diagnosis and remediation.

This is highly relevant to:

```text
historical execution knowledge
+
agent
```

---

## 16.7 Autify Aximo

Aximo focuses on autonomous testing using:

- natural-language goals
- visual recognition
- agent-driven execution

It emphasizes direct interaction with applications rather than purely script-based testing.

It also supports MCP-style integration into coding-agent workflows.

It appears less focused—at least in public materials—on historical bug RAG and long-term QA memory than the proposed project.

---

# 17. Technology Comparison With Competitors

| Technology / Capability | Public Market Evidence |
|---|---|
| LLM / GenAI | Widely used |
| AI agents | Widely used |
| Tool calling | Implied or explicit in many products |
| MCP | Used by multiple competitors |
| Semantic retrieval | Explicitly used by some vendors |
| Historical test data | Used by multiple vendors |
| PRD / docs context | Common |
| Codebase context | Common in newer tools |
| Multi-agent design | Publicly described by some vendors |
| Explicit RAG architecture | Often unclear |
| Vector DB | Usually not publicly disclosed |
| LangGraph | Usually not publicly disclosed |
| CrewAI / AutoGen | Usually not publicly disclosed |

Important conclusion:

> Similar product behavior does not prove identical internal architecture.

Many vendors expose knowledge-grounded or context-aware behavior without publicly disclosing whether they use LangGraph, vector databases, standard RAG pipelines, proprietary retrieval systems, graphs, or hybrid approaches.

---

# 18. Competitive Differentiation

A generic version:

> AI agent generates and runs tests.

is not sufficiently differentiated.

A stronger project focus:

> **Knowledge-Grounded Agentic Testing**

Core differentiator:

```text
              QA Knowledge Base
        ┌────────┼─────────┐
        ↓        ↓         ↓
 Requirements  Bugs    Past Tests
        └────────┼─────────┘
                 ↓
          Hybrid Retrieval
                 ↓
              Agent
                 ↓
           Test Planning
                 ↓
             Execution
                 ↓
              Failure
                 ↓
       Retrieve similar bugs
                 ↓
             Diagnosis
```

The system should demonstrate that historical QA memory improves testing quality.

---

# 19. Research / Engineering Evaluation

The project should include a measurable comparison rather than only a demo.

## Baseline

```text
LLM only
→ generate tests
```

## Proposed System

```text
LLM
+
RAG
+
historical QA knowledge
```

## Possible Metrics

### Test Planning
- Edge-case coverage
- Historical regression coverage
- Duplicate test rate
- Requirement coverage

### Retrieval
- Retrieval relevance
- Top-k precision
- Useful-context rate

### Failure Diagnosis
- Root-cause accuracy
- Similar-bug retrieval accuracy
- Diagnosis usefulness

### Agent Behavior
- Tool-selection accuracy
- Number of unnecessary tool calls
- Retry count
- Completion rate

### Quality / Cost
- LLM token usage
- Latency
- execution time

---

# 20. Recommended Experiment

A simple portfolio-friendly experiment:

## Dataset
Create a small synthetic or open-source product knowledge base containing:

- 20–50 requirements
- 20–50 historical bugs
- 30–100 test cases
- several test logs / failure reports

## Experiment

### System A
LLM receives only the user requirement.

### System B
LLM receives:

- retrieved requirements
- similar historical bugs
- previous test cases

Compare the generated test plans.

Then repeat for failure diagnosis:

### System A
LLM receives only current logs.

### System B
LLM receives:

- current logs
- similar historical failures
- related bugs
- relevant documentation

This makes the project an engineering evaluation rather than just a UI demo.

---

# 21. Recommended Final Tech Stack

## Frontend
- React
- TypeScript

## Backend
- Python
- FastAPI

## Agent Layer
- LangChain
- LangGraph

## RAG
- Embeddings
- Vector database
- optional reranker
- optional hybrid vector + keyword retrieval

Possible vector stores:

- Chroma
- FAISS
- Qdrant
- PostgreSQL + pgvector

## Testing
- Playwright

## Tool Integration
- MCP

## Infrastructure
- Docker

Optional later additions:

- PostgreSQL
- Redis
- object storage
- observability / tracing

---

# 22. MVP Scope Recommendation

Avoid recreating full BrowserStack / TestSprite functionality.

The MVP should prove only one strong end-to-end story.

## MVP Scenario

Example target application:

> A small demo e-commerce or login application.

## MVP Inputs

- one requirement document
- historical bug dataset
- previous test cases

## MVP Flow

```text
User requirement
   ↓
retrieve context
   ↓
generate test plan
   ↓
review test plan
   ↓
execute 1–3 Playwright tests
   ↓
collect result
   ↓
if failure:
    retrieve similar bugs
   ↓
diagnose
   ↓
generate report
```

## MVP Deliverables

- working backend
- RAG pipeline
- LangGraph workflow
- Playwright execution
- simple UI
- test report
- evaluation comparison

MCP can be added after the basic system is stable.

---

# 23. What Not to Build Initially

Avoid:

- full device farm
- mobile testing infrastructure
- dozens of agents
- many agent frameworks at once
- enterprise authentication
- large-scale browser infrastructure
- autonomous code fixing
- complex self-healing
- advanced reinforcement learning
- production multi-tenant SaaS architecture

These can be discussed as future work.

---

# 24. Suggested README Story

A strong README can follow this structure:

## Problem
LLMs can generate tests, but they often lack access to an organization's historical QA knowledge.

## Insight
Testing teams already possess valuable information in:

- requirements
- historical defects
- past tests
- execution logs
- known edge cases

## Solution
Build an agentic testing system that retrieves this knowledge before planning and diagnosing tests.

## Architecture
Show:

```text
RAG + LangGraph + MCP + Playwright
```

## Evaluation
Compare:

```text
LLM-only
vs
RAG-grounded agent
```

## Results
Report:

- test coverage
- regression coverage
- diagnosis accuracy
- retrieval quality

---

# 25. Key Design Principles

1. **RAG must solve a real problem.**  
   Do not add retrieval only to claim the project uses RAG.

2. **Agents should make decisions.**  
   If the workflow is fully deterministic, use normal workflow code.

3. **Use LangGraph where state and branching matter.**

4. **Use MCP as an interface layer, not a buzzword.**

5. **Do not overuse multi-agent architecture.**

6. **Historical QA knowledge is the project's main differentiator.**

7. **Evaluation is as important as the demo.**

8. **Build incrementally.**

---

# 26. Final Target Architecture

```text
                    ┌─────────────────┐
                    │    React UI     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │     FastAPI     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    LangGraph    │
                    │  Orchestrator   │
                    └───────┬─────────┘
                            │
              ┌─────────────┴─────────────┐
              ↓                           ↓
      ┌───────────────┐           ┌───────────────┐
      │   RAG Layer   │           │  MCP Client   │
      └───────┬───────┘           └───────┬───────┘
              ↓                           ↓
      ┌───────────────┐           ┌───────────────┐
      │   Vector DB   │           │  MCP Server   │
      └───────┬───────┘           └───────┬───────┘
              │                           │
     ┌────────┼────────┐          ┌───────┼───────────┐
     ↓        ↓        ↓          ↓       ↓           ↓
  PRDs     Bugs    Past Tests  Playwright Logs   Screenshots
```

Failure branch:

```text
Execute test
    ↓
Failed?
    ↓
Collect logs
    ↓
Retrieve similar historical bugs
    ↓
Retrieve similar historical failures
    ↓
Analyze probable root cause
    ↓
Generate diagnosis and report
```

---

# 27. Current Recommended Build Order

```text
1. Tool Calling
      ↓
2. RAG
      ↓
3. LangGraph
      ↓
4. Reflection
      ↓
5. Multi-Agent
      ↓
6. MCP
      ↓
7. React UI
      ↓
8. Evaluation
```

This sequence keeps the project manageable and aligns closely with the IBM course progression.

---

# 28. Competitive Research References

Public materials reviewed during initial competitor research:

- TestSprite  
  https://www.testsprite.com/

- Momentic  
  https://momentic.ai/

- mabl  
  https://www.mabl.com/

- BrowserStack AI / Testing Agents  
  https://www.browserstack.com/

- LambdaTest / KaneAI / TestMu AI  
  https://www.lambdatest.com/

- Functionize  
  https://www.functionize.com/

- Autify / Aximo  
  https://autify.com/

A related research direction was also identified around:

> Agentic RAG for software testing using hybrid retrieval and multi-agent orchestration.

This provides evidence that the proposed architecture aligns with an active research and commercialization direction in AI-assisted software testing.

---

# 29. Project Thesis

The strongest version of this project is not:

> "I built an AI agent that can test a website."

It is:

> **I built and evaluated a knowledge-grounded testing agent that uses an organization's accumulated QA memory to generate better tests and diagnose failures more effectively.**

That thesis should guide architecture decisions, development scope, evaluation, and portfolio presentation.
