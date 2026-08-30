---
name: enterprise-delivery
description: Use for implementing, fixing, reviewing, refactoring, or preparing to deliver software. Selects risk-scaled planning, testing, review, and verification workflows.
---

# Enterprise Delivery

Use the lightest workflow that protects the requested outcome. Read repository instructions, inspect workspace state, preserve unrelated changes, and define observable acceptance criteria.

## Request Boundary

Explanations, status reports, diagnoses, and read-only reviews do not authorize implementation. Inspect and report; classify a proposed change if useful without starting its implementation lifecycle. For changes, use the workflow below.

Load only skills needed for the current decision or stage. A routing-only turn may name later required gates without opening them all; do not inspect every linked workflow preemptively.

## Risk First, Scheduling Second

Choose the highest applicable level. A scheduling, approval, fallback, or cost rule cannot lower a security/data risk. Upgrade as evidence appears; any later reduction needs explicit root-cause/scope evidence and a stated rationale.

| Level | Actual affected behavior | Minimum workflow |
|---|---|---|
| L1 | Clear, isolated, reversible work; no architectural/public-contract change or sensitive boundary | Focused implementation, useful tests, final verification |
| L2 | Non-trivial or cross-module work, meaningful design choices, public-contract change, uncertain diagnosis | Approved design, proportionate plan, review, final verification |
| L3 | Changes to authorization enforcement, authentication/session handling, payment integrity, untrusted uploads/URL/file/command handling, secrets, tenant isolation, migrations, production data, concurrency, destructive operations or material integrity | L2 plus Strong-model safety decisions, rollback/failure requirements and scoped security review |

Mentioning a URL, file, command, or permission label is not enough for L3: inspect the changed behavior and trust boundary. A settings UI/configuration interface is L2 when server authorization and tenant isolation are unchanged; enforcement changes remain L3.

An intermittent, nondeterministic, or not-yet-reproduced API failure has an L2 floor; a security/data/concurrency boundary still makes it L3. A deterministic, reproduced, isolated bug can be L1 only with no higher-risk boundary.

## Design and Plan

L1 needs neither brainstorming nor a plan document by default.

For L2/L3, check whether the user has already approved the applicable design and implementation scope:
- Reuse that approval and any current plan when requirements, interfaces, affected risks, and allowed actions remain unchanged. Cite the approval message or artifact; do not ask for the same approval again.
- Without applicable approval, or when a material design/scope/risk change needs a new decision, load [brainstorming](../brainstorming/SKILL.md). Reapprove only the changed decision, without treating a general "continue" as permission for new external or destructive actions.
- Load [writing-plans](../writing-plans/SKILL.md) when a plan is missing or needs revision. A bounded L2 plan can be concise; architectural/L3 work needs a durable plan covering safety, compatibility, failure and rollback where applicable.

For L3, obtain a Sol/available Strong-tier decision on the affected boundary and safety approach before implementation; use [model-routing](../model-routing/SKILL.md) if model availability or delegation needs resolution. Never label a lower-tier self-review as Strong adjudication.

## Implementation and Bugs

Every bug fix loads [systematic-debugging](../systematic-debugging/SKILL.md) before implementation changes: collect reproduction evidence, establish a root cause, add a practical regression check, apply a focused fix, and recheck the original failure.

Load [test-driven-development](../test-driven-development/SKILL.md) when test infrastructure runs, behavior is observable, and test cost is proportionate. Otherwise use safe observable alternatives and report the missing automated regression check as NOT VERIFIED with its reason. Never manufacture wording tests or pretend missing tests passed.

## Agents and Review

One writer is the default. Do not delegate work that the main agent can finish more cheaply than coordination. Delegation needs user or applicable-skill authorization and a bounded assignment.

For requested multi-agent work with overlapping files, shared interfaces, or shared uncommitted state, use at least L2, retaining L3 whenever applicable. Load [model-routing](../model-routing/SKILL.md) and [dispatching-parallel-agents](../dispatching-parallel-agents/SKILL.md) for the independence decision. Reject overlapping writers, serialize implementation, and retain only useful independent read-only parallel work. This branch replaces SDD selection for the overlap decision: do not load or inspect SDD merely to explain serialization, even if the original request asked for multiple agents.

For an approved plan intended for subagent execution, load [subagent-driven-development](../subagent-driven-development/SKILL.md). If the host already reports subagents unavailable, still load its serial fallback, do not attempt dispatch, preserve task boundaries, and disclose lost independence.

L2/L3 implementation requires [requesting-code-review](../requesting-code-review/SKILL.md). It defines reviewer choice and the honest self-review fallback when independence is unavailable. Critical findings require explicit [model-routing](../model-routing/SKILL.md) and review workflow selection, Sol/available Strong adjudication, resolution or a delivery block, then re-review of the fix.

After L3 review, load [security-review](../security-review/SKILL.md) for the affected boundaries. Resolve confirmed Critical/Important findings before final verification.

## Completion

Load [project-verification](../project-verification/SKILL.md) to select checks and maintain one current evidence ledger. Then load [verification-before-completion](../verification-before-completion/SKILL.md) to validate the claims against that same ledger, not to duplicate unchanged checks.

Report exact commands/results, FAILED required gates, and every NOT VERIFIED check with its reason. Final diff/status inspection and relevant post-change verification remain mandatory.
