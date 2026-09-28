# Casewake: real-product pilot direction

**Status:** Direction update, September 28, 2026. The first pilot product is configured locally; Casewake is not limited to one product.

Casewake should help test a configured, complete product against its product requirements. The checkout calculation already in this repository is an isolated learning fixture. It is not the chosen product demo, and extending its browser UI is not the next milestone.

## What the documents mean

A PRD or design specification is the source of expected behavior, not an executable test-case library by itself. Casewake should turn cited, current requirements into a separate library of reviewable cases. Each case needs a stable ID, source location, preconditions, steps or an existing test reference, expected result, applicability, and execution status. Where the document does not define an expected result, the case stays unresolved rather than guessing.

Historical defects are a second source of risk ideas, not the authority for current expected behavior. Existing automated tests are a third input: they show known coverage and should be reused when applicable. The resulting report links requirement → case → test attempt → observed evidence.

## First pilot candidate: a private mobile product

The local pilot candidate is an Expo/React Native product. It contains a design specification and automated tests for parts of its logic. Start from that design specification unless a separate, more authoritative PRD is supplied. Select one implemented feature for the first end-to-end slice after mapping the document to the current code and tests. Do not interpret a planned feature as already implemented.

Casewake should stay configurable for another product. A target profile should identify the local product root, approved requirements files, existing test inventory, allowed test commands, and supported execution adapter. The profile and imported source content remain local. Do not copy private product documents, secrets, or test artifacts into Casewake's public Git repository.

The current Playwright browser smoke test only checks Casewake's own minimal page. It does not test native mobile screens. The first pilot can execute the product's existing unit/integration tests through an approved command adapter. Mobile UI execution needs a separate feasibility check and adapter before Casewake can claim to run device-level tests.

## Revised sequence

1. **Source inventory:** select the authoritative product requirement document, identify one feature and its current implementation status, and inventory related existing tests. Record source versions and links/locations.
2. **Requirement and case model:** parse or curate a small set of explicit requirements into stable IDs. Draft cases with independently specified expectations; validate structure and flag ambiguity for review.
3. **Coverage view:** map cases to existing product tests. Mark each as covered, partially covered, uncovered, or unresolved, with evidence for the classification.
4. **First execution slice:** run one approved existing test or small test group against the product, capture command, revision, exit status, test results, and logs, then link the attempt to its requirement and case. A failing test is not automatically a product defect.
5. **Gap expansion:** propose new cases for uncovered or historically risky behavior; have a person confirm expectations before execution. Add a supported runner for new cases only after its actions and isolation are defined.
6. **Agent and retrieval:** once the manual source-to-evidence path works, add bounded model planning, historical retrieval, MCP tools, persistence, reporting, and comparative evaluation as described in the PRD.

**First useful outcome:** for one real feature, Casewake shows the source requirement, a concrete test case, whether an existing test covers it, and the observed result of an approved test run. This is a narrow, truthful slice of a full product, not a claim of complete coverage.
