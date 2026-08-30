---
name: subagent-driven-development
description: Use to execute an approved multi-task implementation plan with bounded implementer and reviewer roles, or to preserve its task boundaries through serial fallback when subagents are unavailable.
---

# Subagent-Driven Development

Execute an approved plan through bounded task assignments, task-level review, and main-agent integration. Use when multi-agent execution is authorized and delegation adds value, or when the enterprise router selects this skill to apply its fallback to a plan that was intended for subagent-driven execution.

If the host already reports that subagents are unavailable, do not attempt dispatch. Read the approved plan, preserve its task boundaries, and go directly to [Fallback](#fallback).

## Preconditions

- An approved implementation plan exists.
- Tasks and acceptance criteria are explicit.
- Repository instructions and workspace state are known.
- Task boundaries support isolated ownership.
- A single main agent is designated as integration owner.

If the plan is missing or materially ambiguous, return to design or planning. Do not use delegation to hide unclear requirements.

## Model Routing

Load [model-routing](../model-routing/SKILL.md) before dispatching roles.

- Luna handles complete, mechanical, bounded tasks.
- Terra is the default for ordinary multi-file implementation and review.
- Sol owns architecture, security, concurrency, data integrity, conflicting requirements, critical findings, and final high-risk integration judgment.

Specify a model for every assignment. Escalate after repeated failed hypotheses or review/fix cycles rather than repeatedly giving the same task to the same tier.

## Single-Writer Boundary

The main agent is the integration owner. Only one implementation writer operates at a time unless file and interface ownership is provably disjoint and isolated workspaces prevent shared-state conflicts.

Subagents must not merge, push, publish, delete shared state, manage the user's branch lifecycle, or expand scope without explicit authorization. A task implementer must not create another subagent.

## Setup

1. Read the approved plan and its linked specification.
2. Inspect repository instructions and current workspace state.
3. Record each task, dependencies, allowed paths, model, acceptance criteria, and verification command in a progress ledger.
4. Check tasks for shared files, shared interfaces, contradictory assumptions, and ordering constraints.
5. Resolve conflicts against the approved specification before dispatch.

The bundled scripts may create task briefs and review packages when compatible with the host:

- `scripts/sdd-workspace`
- `scripts/task-brief`
- `scripts/review-package`

They are helpers, not permission to create or delete workspaces automatically.

## Per-Task Loop

### 1. Brief the Implementer

Use [implementer-prompt.md](implementer-prompt.md) as a base. Give the implementer only the task-specific context it needs:

- objective and place in the approved plan;
- exact task brief path or complete bounded requirements;
- allowed and prohibited files;
- established interfaces from completed tasks;
- tests and evidence required;
- report path and result contract.

Record the task's base revision or equivalent workspace state before implementation.

### 2. Evaluate the Implementation Report

The report must identify changed paths, design decisions, test commands and results, open concerns, and any departure from the brief. Missing evidence is not a successful task result.

If blocked, distinguish missing context, insufficient model capability, a task that needs decomposition, and a defective plan. Change the cause before retrying.

### 3. Run Independent Task Review

Use [task-reviewer-prompt.md](task-reviewer-prompt.md) with the task brief, implementation report, exact diff, and binding global constraints. The reviewer must evaluate both requirement compliance and code quality.

The reviewer is independent of the implementer. Use Terra by default and Sol for high-risk judgment. If independent review is unavailable, the main agent performs structured self-review and records `NOT VERIFIED: independent task review` with the exact reason.

### 4. Fix and Re-review

Return confirmed Critical and Important findings to the implementer with the exact finding and expected evidence. Review only the resulting fix diff with [re-review-prompt.md](re-review-prompt.md).

After two unsuccessful fix/review cycles, escalate the model or re-evaluate the plan. Do not continue unbounded churn. Record any deferred finding with its severity, rationale, owner, and delivery impact.

### 5. Integrate

The main agent checks the report and review evidence, integrates the task, runs affected checks, updates the ledger, and only then advances dependent tasks.

## Final Integration Gate

After all tasks:

1. Review the combined diff against the approved design and plan.
2. Reconcile cross-task contracts and resolve deferred Critical or Important findings.
3. Run [project-verification](../project-verification/SKILL.md).
4. Run [verification-before-completion](../verification-before-completion/SKILL.md).
5. Report exact evidence and all `NOT VERIFIED` items.

Branch integration, commits, merges, pushes, publishing, installation, and workspace cleanup occur only when they are part of the approved task and separately authorized where required. This skill never implies those actions.

## Fallback

If subagents are unavailable or no longer justified, the main agent executes the remaining tasks serially from the same approved plan. When unavailability is known before execution, do not attempt dispatch. Preserve task boundaries, review the diff after each increment, and explicitly report any lost independence or concurrency.
