# Enterprise Dev Workflow Plugin Design

Date: 2026-08-24
Status: Approved with compatibility revisions; implementation authorized

## Purpose

Create a shareable, self-contained Codex plugin that raises software-delivery discipline toward enterprise standards without enabling the full Superpowers suite or spending premium-model tokens on mechanical work.

The plugin is a risk-aware delivery guard, not a claim of compliance certification or guaranteed production readiness. Projects that lack test infrastructure, CI, staging, observability, credentials, or suitable environments must report the affected checks as `NOT VERIFIED`.

## Compatibility Basis

The design follows current OpenAI skill behavior:

- Skills use progressive disclosure: hosts first see skill names and descriptions, then load full instructions only when a skill is selected.
- `agents/openai.yaml` supports invocation policy through `policy.allow_implicit_invocation`.
- Plugins are the supported distribution mechanism for bundling reusable skills.
- The GPT-5.6 family provides Sol for frontier capability, Terra for balanced engineering work, and Luna for efficient high-volume work.

References:

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/build-plugins
- https://developers.openai.com/api/docs/guides/latest-model

## Plugin Identity and Location

- Name: `enterprise-dev-workflow`
- Initial version: `0.1.0`
- Author display name: `Louyongqing`
- Plugin directory: `plugins/enterprise-dev-workflow`
- Marketplace: `.agents/plugins/marketplace.json` at the repository root
- Marketplace policy: `AVAILABLE`
- Authentication policy: `ON_INSTALL`
- Category: `Productivity`

The manifest must contain only fields accepted by the current plugin validator.

## Skill Inventory

The plugin is self-contained and exposes twelve skills:

1. `enterprise-delivery` - the primary workflow and risk router
2. `model-routing` - selects strong, standard, or economy models
3. `systematic-debugging`
4. `verification-before-completion`
5. `brainstorming`
6. `writing-plans`
7. `test-driven-development`
8. `requesting-code-review`
9. `dispatching-parallel-agents`
10. `subagent-driven-development`
11. `security-review`
12. `project-verification`

The eight selected Superpowers skills are vendored with required supporting files and adapted for Codex and enterprise workflow compatibility. The plugin intentionally excludes `using-superpowers`, `using-git-worktrees`, `executing-plans`, `finishing-a-development-branch`, and unrelated Superpowers skills.

`model-routing` comes from the user-provided skill. `enterprise-delivery`, `security-review`, and `project-verification` are original plugin skills. The last two must not copy text from local skills without explicit redistribution terms.

## One Primary Router

`enterprise-delivery` is the only skill allowed to participate in implicit invocation. Its metadata contains:

```yaml
policy:
  allow_implicit_invocation: true
```

Every other bundled skill contains:

```yaml
policy:
  allow_implicit_invocation: false
```

Those skills remain available for direct user invocation, but normal software work enters through `enterprise-delivery`, which explicitly selects the required workflow skills. This prevents independent skill descriptions from bypassing the L1/L2/L3 risk router.

## Risk Classification

The router classifies the task before implementation and upgrades the level if hidden complexity appears. It never silently downgrades a task after discovering higher risk.

Four explicit overrides prevent broad keywords from bypassing the intended contract:

- Permission-settings UI and configuration plumbing remain L2 when server-side authorization decisions and enforcement are unchanged; authorization enforcement is L3.
- An intermittent, nondeterministic, or not-yet-reproduced HTTP 500/API failure starts at L2. Only a deterministic, reproduced, isolated root cause may remain L1 when no higher-risk boundary applies.
- An approved plan intended for subagent-driven execution still loads `subagent-driven-development` and uses its serial fallback without attempting unavailable dispatch when subagents are unavailable.
- A Critical review finding explicitly loads `model-routing` and `requesting-code-review`, escalates adjudication to Sol, and requires resolution or a delivery block followed by re-review.

### L1 - Routine Change

Use when scope is clear, impact is isolated, risk is low, core architecture is unchanged, and no sensitive trust boundary is affected.

Flow:

1. Read applicable repository instructions and inspect workspace state.
2. Define observable acceptance criteria.
3. Decide whether TDD is useful and practical.
4. Make the smallest focused change.
5. Run `project-verification`.
6. Run `verification-before-completion`.
7. Report verified evidence and every `NOT VERIFIED` item.

L1 defaults:

- no `brainstorming`;
- no implementation-plan document;
- no subagent;
- no repeated independent review cycle.

### L2 - Complex Feature

Use for non-trivial features, multiple affected modules, meaningful design choices, public-interface changes, or architectural impact.

Flow:

1. Run `brainstorming` and obtain design approval.
2. Run `writing-plans`.
3. Implement with useful tests.
4. Request independent review.
5. Resolve findings.
6. Run `project-verification`.
7. Run `verification-before-completion`.

Sol owns requirements, architecture, decomposition, conflicting decisions, and final integration. Terra is the default for normal engineering implementation and review. Luna is used for bounded mechanical work.

### L3 - High-Risk Change

Use for authentication, authorization enforcement, payments, uploads, external URLs, commands, file paths, secrets, admin capabilities, database migrations, production data, concurrency, destructive actions, or material data-integrity risk.

Flow:

1. Run `brainstorming` and obtain design approval.
2. Run `writing-plans`.
3. Require a Sol risk decision for the affected trust boundary.
4. Implement with appropriate tests and rollback considerations.
5. Request independent review.
6. Run `security-review`.
7. Run `project-verification`.
8. Run `verification-before-completion`.

Sol involvement is mandatory for security-critical decisions, data-loss risk, migrations and rollback design, concurrency, architectural uncertainty, Critical review findings, conflicting requirements, and low-confidence investigations.

## Adapted Superpowers Skills

The vendored skills preserve their useful core behavior but must not retain dependencies on excluded skills or rules that conflict with the primary router.

### `brainstorming`

- Explicitly selected only for L2/L3 or direct user invocation.
- Retains design clarification and approval gates.
- Does not automatically upgrade L1 work.
- Hands approved designs to the adapted `writing-plans` skill.

### `writing-plans`

- Produces implementation-ready, test-aware plans.
- Removes required references to `using-git-worktrees` and `executing-plans`.
- Hands off to adapted `subagent-driven-development` only when multi-agent execution is authorized and worthwhile.
- Otherwise supports inline, single-writer execution in the current workspace.

### `systematic-debugging`

- Runs before implementation changes for bug fixes.
- Preserves evidence collection, root-cause analysis, controlled hypothesis testing, and regression verification.
- Does not permit speculative multi-fix patching.

### `test-driven-development`

- Uses conditional enterprise TDD rules defined below instead of an absolute test-first rule for every production-code change.

### `requesting-code-review`

- Defaults to independent Terra review.
- Allows Luna for tiny mechanical diffs.
- Escalates to Sol using the documented triggers.
- Falls back to main-agent self-review when subagents are unavailable, and reports the loss of independence.

### `dispatching-parallel-agents`

- Prioritizes parallel read-only work.
- Enforces the single-writer and disjoint-ownership rules below.
- Limits normal parallelism to two or three agents.

### `subagent-driven-development`

- Accepts an already approved implementation plan.
- Dispatches bounded assignments with minimum sufficient context.
- Collects results, obtains independent review, and returns integration responsibility to the main agent.
- Removes hard dependencies on worktree creation, branch finishing, merging, pushing, publishing, and automatic branch lifecycle.

### `verification-before-completion`

- Requires fresh, current-environment evidence before success claims.
- Uses the common Verified/Not Verified report format.

## Agent and Workspace Safety

Subagents are allowed only when:

- the user or an applicable skill authorizes multi-agent execution;
- each assignment has a bounded deliverable;
- delegation saves more time or context than it costs;
- the child receives only minimum sufficient context; and
- the workspace ownership rules can be satisfied.

Parallel read-only assignments are allowed for search, analysis, test triage, code review, log inspection, and documentation inspection.

Parallel writes are allowed only when file ownership is provably disjoint or existing isolated workspaces eliminate shared-state risk. Parallel writers must not modify the same interface or depend on shared uncommitted state.

When multi-agent execution is requested but the proposed writers overlap, the router classifies the request as L2, selects `model-routing` and `dispatching-parallel-agents` for the independence decision, rejects the unsafe writer split, serializes implementation through one writer, and retains only useful independent read-only work in parallel. `subagent-driven-development` is forbidden by default for this branch and is not selected merely to describe serialization.

Otherwise, implementation uses one writer and serial execution. Normal parallelism is two or three agents; a larger fan-out requires an explicit benefit. Missing multi-agent support or authorization falls back to serial main-agent execution. When an approved plan was intended for subagent-driven execution and support is already known to be unavailable, the router does not attempt dispatch; it still loads that skill and applies its defined fallback before continuing serially.

## Conditional TDD

### TDD Required

Use Red-Green-Regression-Verification when:

- runnable test infrastructure exists;
- changed behavior can be meaningfully observed automatically;
- a regression test represents the real requirement or bug; and
- test cost is proportionate to change risk.

The expected failure must be observed before implementation is treated as validated by the new test.

### TDD Not Practical

TDD is not required when:

- the project has no suitable test infrastructure;
- the current environment cannot run it;
- the change is generated code or purely declarative configuration; or
- a proposed test would create fake coverage without validating real behavior.

In these cases, continue with the best safe verification available and report precisely:

```text
NOT VERIFIED: automated regression test
Reason: <exact reason>
```

Absence of a test environment must never be described as tests passing.

## Bug Workflow

All bug fixes explicitly select `systematic-debugging` before changing implementation code:

1. Reproduce or collect evidence.
2. Identify the root cause.
3. Add a regression test when meaningful and practical.
4. Apply the smallest root-cause fix.
5. Run regression verification.
6. Run project-level verification.

Luna may collect logs, search files, and organize evidence. Terra or Sol handles cross-module root causes, high uncertainty, concurrency, security-related failures, and data-integrity issues.

## Model Routing

Preferred model classes are:

- Strong: `gpt-5.6-sol`
- Standard: `gpt-5.6-terra`
- Economy: `gpt-5.6-luna`

### Economy - Luna

Use for clear, mechanical, low-judgment work:

- search and file discovery;
- information extraction;
- mechanical edits with exact scope;
- formatting and repetitive changes;
- executing established tests;
- straightforward test code;
- configuration scanning.

Luna does clear work; it does not own complex decisions by default.

### Standard - Terra

Use for ordinary engineering judgment:

- routine feature implementation;
- multi-file work with clear boundaries;
- first-pass code review;
- bug-evidence analysis;
- API compatibility review;
- integration review;
- test design requiring moderate context.

Terra is the default independent reviewer. A small, mechanical diff may use Luna instead.

### Strong - Sol

Use for high-judgment work:

- requirements and architecture;
- task decomposition;
- security-sensitive decisions;
- concurrency and migrations;
- data-loss risk;
- critical-review adjudication;
- conflicting requirements;
- high-risk integration;
- low-confidence investigation;
- final responsibility decisions.

### Model Substitution

If an exact model is unavailable:

1. Inspect the current allowed model roster.
2. Choose the closest available capability tier for that role.
3. Record requested model, selected model, and reason.
4. Do not repeatedly retry a missing model or profile.
5. Do not skip a required review because the preferred model is unavailable.

Example:

```text
MODEL SUBSTITUTION
Requested: gpt-5.6-luna
Used: gpt-5.6-terra
Reason: requested model unavailable
```

## Code Review

Default flow:

```text
Implementation
-> independent Terra review
-> findings
-> focused fix
-> verification
```

The reviewer checks requirement coverage, defects, regressions, error handling, missing tests, compatibility, unsafe assumptions, and maintainability. Findings are grouped as Critical, Important, or Minor.

Escalate to Sol for Critical findings, security, concurrency, data-corruption risk, architecture, unclear intended behavior, conflicting requirements, low reviewer confidence, or two failed review/fix cycles.

Review reports findings only unless implementation was explicitly requested. It must not silently rewrite code.

## Security Gate

The original `security-review` skill performs a scoped trust-boundary review covering, when applicable:

- authentication, sessions, and credential handling;
- authorization and object-level access control;
- input validation, injection, and output encoding;
- secrets and sensitive-data exposure;
- uploads, path traversal, commands, and external URLs;
- database integrity, transactions, migrations, rollback, and retention;
- payment, admin, webhook, and replay/idempotency risks;
- dependency or configuration changes that materially affect the attack surface.

It applies focused remediation only. It must not expand into unrelated rewrites or mutate production data.

## Project Verification Gate

The original `project-verification` skill selects checks from repository instructions, manifests, CI workflows, changed files, affected behavior, and project tooling. Applicable checks include:

- build and package generation;
- type checking and linting;
- unit, integration, and end-to-end tests;
- browser behavior, console output, responsive states, and network failures for local web UI;
- API contracts and compatibility;
- migrations, rollback, constraints, and data integrity;
- security-sensitive paths;
- final Git status and diff review;
- secrets, debug artifacts, missing tests, and missing migrations.

Each unavailable check is reported as:

```text
NOT VERIFIED: <check>
Reason: <exact reason>
```

## Verification Before Completion

Final success claims require new evidence from the current environment. Phrases such as “should work,” “probably fixed,” “looks good,” or “tests should pass” are not verification.

Recommended report shape:

```text
VERIFIED
- build: PASS
- typecheck: PASS
- unit tests: 128 PASS

NOT VERIFIED
- E2E browser test
  Reason: browser environment unavailable
```

## Packaging and Attribution

Expected plugin structure:

```text
enterprise-dev-workflow/
|-- .codex-plugin/plugin.json
|-- README.md
|-- LICENSE
|-- THIRD_PARTY_NOTICES.md
|-- docs/
|   `-- design.md
|-- evals/
|   `-- routing-cases.json
|-- scripts/
|   `-- validate_routing_contract.py
`-- skills/
    |-- enterprise-delivery/
    |-- model-routing/
    |-- systematic-debugging/
    |-- verification-before-completion/
    |-- brainstorming/
    |-- writing-plans/
    |-- test-driven-development/
    |-- requesting-code-review/
    |-- dispatching-parallel-agents/
    |-- subagent-driven-development/
    |-- security-review/
    `-- project-verification/
```

The first release has no MCP server, app connector, hooks, icons, or screenshots.

The selected Superpowers source is the locally installed `obra/superpowers` plugin version `6.3.0`. It is distributed under MIT terms. `THIRD_PARTY_NOTICES.md` records:

- upstream project and source URL;
- exact version `6.3.0`;
- MIT license and preserved copyright;
- bundled skill directories;
- every adapted skill.

Original plugin content uses the MIT license. Adapted files must not be represented as unmodified upstream copies.

## Behavioral Routing Evaluation

Passing structure validators is necessary but does not establish workflow behavior.

The plugin includes machine-readable routing cases and a deterministic contract validator. Static validation confirms metadata policy, required routes, model tiers, references, and fallback rules. It does not claim that a model followed the workflow.

Runtime evaluation must be performed in a new conversation after installation because skill discovery and implicit routing occur at conversation startup. If the current Codex CLI or app environment cannot run these scenarios, runtime routing remains `NOT VERIFIED` rather than being inferred from static text.

Required scenarios:

1. L1 field addition: classify L1; no brainstorming, plan, or subagent by default; run applicable verification.
2. L2 cross-frontend/backend permission-settings UI/configuration feature that does not change authorization enforcement: require brainstorming, approval, plan, implementation, independent review, and verification.
3. L3 refresh-token/session renewal change: require Sol involvement, security review, regression verification, and project verification.
4. Intermittent HTTP 500 bug: classify L2 and select systematic debugging before implementation changes.
5. Missing test infrastructure: continue safe checks and report the automated regression test as `NOT VERIFIED`.
6. Missing Luna: choose an available equivalent, record substitution, and avoid repeated retries.
7. Missing subagent support: load `subagent-driven-development` without attempting unavailable dispatch, then fall back to serial main-agent execution.
8. Dirty worktree: preserve unrelated changes and stop only if safe isolation is impossible.
9. Critical review finding: load `model-routing` and `requesting-code-review`, escalate to Sol, resolve or block, and re-review.
10. Parallel write request with overlapping files: select the parallel-independence workflow, reject overlapping writers, serialize through one writer, and retain useful independent read-only parallel work.

## Failure Handling

- Missing preferred model: choose an available equivalent and record the substitution.
- Missing multi-agent capability or authorization: run serially with the main agent.
- Missing project test, CI, browser, database, or build environment: complete safe available checks and report the rest as `NOT VERIFIED`.
- Dirty worktree: preserve unrelated user changes and stop if safe isolation is impossible.
- Plugin or skill validation failure: do not claim completion or offer installation as successful.
- Marketplace update failure: leave the validated plugin source intact and provide the exact unresolved issue.
- Codex CLI unavailable in the desktop environment: validate files locally and mark CLI installation and runtime routing as `NOT VERIFIED`.

## Acceptance Criteria

The plugin source is structurally complete when:

1. The scaffolded manifest passes the plugin validator.
2. Every bundled skill passes the skill validator.
3. All referenced relative files exist inside the plugin.
4. Manifest name, folder name, marketplace entry, and skill paths agree.
5. No placeholder text or unsupported manifest field remains.
6. The repository marketplace entry contains installation policy, authentication policy, and category.
7. MIT licensing and third-party attribution are present.
8. The final file inventory contains no secrets, temporary files, or debug artifacts.
9. `enterprise-delivery` is the only implicitly invocable skill.
10. Adapted skills contain no hard references to excluded Superpowers skills.
11. Model routing contains Sol, Terra, and Luna roles plus substitution reporting.
12. The deterministic routing-contract tests pass.

The plugin is behaviorally validated only when the required runtime scenarios pass in a fresh conversation. Any unexecuted scenario remains explicitly `NOT VERIFIED`.

## Out of Scope

- Modifying existing projects, CI pipelines, or repository instructions
- Installing external applications or connectors
- Automatically enabling multi-agent support in user configuration
- Automatically creating worktrees, merging, pushing, publishing, or finishing branches
- Publishing to a public marketplace or remote Git repository
- Guaranteeing compliance certification or production readiness without project-specific evidence
