---
name: writing-plans
description: Use when approved L2/L3 software work needs a new or revised implementation plan, or a plan is explicitly requested. Reuse current plans.
---

# Writing Plans

Produce the smallest plan that makes implementation and verification unambiguous.

## Reuse and Scale

First check the approved design and existing plan. When scope, interfaces, risk, and repository state remain compatible, continue from unfinished tasks; do not ask the user to approve the same work again.

- Bounded L2: a concise in-chat/task plan is sufficient unless the user or repository requires a file.
- Architectural, L3, multi-session, or explicitly documented work: persist a plan in the repository's chosen location, otherwise `docs/enterprise-dev-workflow/plans/YYYY-MM-DD-<feature>.md`.

Reference the approval message or design path. Do not invent a design-file requirement when the approved design exists only in conversation. New material decisions return to [brainstorming](../brainstorming/SKILL.md); formatting or faithful decomposition alone does not reset approval.

## Required Content

Include only what execution needs:
- observable outcome and acceptance criteria;
- architecture/stack and constraints that affect decisions;
- approval source, scope exclusions, and relevant permissions;
- exact affected files, interfaces, task dependencies, and ownership;
- meaningful tests and exact verification commands;
- for L3, applicable threat/failure modes, compatibility, migration, integrity and rollback requirements.

A task is an independently reviewable deliverable, not a fixed number of minutes or micro-steps. Define the rule, interface or example behind "validation" or "error handling"; avoid vague instructions.

Plan test-first steps when runnable behavior tests justify them. If not practical, identify the reason and best observable substitute; do not invent source-wording tests or fake coverage.

## Self-Review and Execution

Map each approved requirement to implementation and verification. Check paths, names, contracts, safety constraints, and exclusions for consistency.

Continue with one writer when the user has authorized implementation. Do not stop merely to offer execution-mode choices. Use subagents only when authorized, useful, and safely scoped; load [subagent-driven-development](../subagent-driven-development/SKILL.md) for that execution mode.

Plans do not authorize worktrees, branches, commits, merges, pushes, releases, production changes, or destructive cleanup. Follow the repository lifecycle and actual user authorization.
