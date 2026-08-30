---
name: brainstorming
description: Use when an L2/L3 software change lacks an approved design, a material decision has changed, or the user requests design exploration. Reuse applicable prior approval.
---

# Brainstorming

Turn consequential uncertainty into an approved design. Preserve the router's risk level and the user's scope.

## Check Existing Decisions First

Read relevant repository context and the user's approval message or artifact. If the design, acceptance criteria, interfaces, risks, and allowed actions remain applicable, summarize what is being reused and continue; do not recreate the design or request duplicate approval.

A material change to those decisions requires approval of the delta. An ambiguous "continue" does not authorize unrelated work or new external/destructive actions.

## Resolve Only Material Uncertainty

Inspect existing architecture, tests, and constraints before questions. Ask one material question at a time; make low-risk assumptions when the context already answers it.

- Bounded changes: present a short design covering behavior, affected files/interfaces, acceptance criteria, and relevant risks.
- Architectural changes: compare viable approaches and explain ownership, data flow, failure behavior, security, compatibility/migration, rollback, and verification as applicable.

Split genuinely independent subsystems only when separate delivery and approval help. Do not create speculative capabilities or documentation ceremony.

## Approval and Durable Design

When no applicable approval exists, present the design and wait for explicit approval before implementation. When revising an approved design, ask only about material changes.

For architectural work, save the approved design to the repository's location or:
`docs/enterprise-dev-workflow/specs/YYYY-MM-DD-<topic>-design.md`

A faithful transcription of an approved design does not require another approval unless the user/repository requires written approval. If writing exposes a new decision, conflict, or changed boundary, obtain approval of that delta before implementation. Preserve requirements and rollback/safety decisions; review the document for contradictions and omissions.

Proceed to [writing-plans](../writing-plans/SKILL.md) when a plan is needed. Reuse an existing valid plan rather than restating it.

## Visual Companion

Offer [visual-companion.md](visual-companion.md) only when a visual would materially clarify the design; read it only if accepted.
