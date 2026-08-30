---
name: dispatching-parallel-agents
description: Use when two or more independent tasks can run concurrently without shared mutable state. Defaults to read-only parallelism and one writer.
---

# Dispatching Parallel Agents

Parallelism is a scheduling tool, not a default. Use it only when independent work will finish sooner than coordination overhead and the user or applicable instructions authorize multi-agent execution.

## Independence Test

Before dispatching, create a task matrix:

| Task | Inputs | Outputs | Files or state | Dependencies | Model |
|---|---|---|---|---|---|

Tasks are parallel-safe only when they can complete without consuming another task's unfinished output, modifying the same files or interfaces, or depending on shared uncommitted state.

Good parallel assignments include repository research, log analysis, test-failure triage, documentation review, independent code review, and unrelated read-only investigations.

Do not parallelize tightly coupled implementation, sequential migrations, overlapping fixes, or tasks that can invalidate each other's assumptions.

## Writer Policy

Default to one writer. Parallel agents return analysis, evidence, patches, or recommendations to the main integrator.

Parallel writes require both:

1. provably disjoint file and interface ownership; and
2. isolated workspaces or another verified mechanism that prevents shared-state collisions.

The main agent owns integration, conflict resolution, cross-task verification, and the final completion claim. Agents must not merge, push, publish, delete shared state, or widen scope unless separately authorized.

## Dispatch Size and Models

Use two or three agents for normal work. More agents require clear evidence that the tasks remain independent and that review and integration capacity exists.

- Luna: bounded search, evidence gathering, mechanical inspection.
- Terra: ordinary implementation analysis, debugging, and review.
- Sol: architecture, security, concurrency, data integrity, conflict resolution, and critical review.

Specify the model and expected output explicitly. Use [model-routing](../model-routing/SKILL.md) when the assignment is not obviously mechanical.

## Bounded Brief Contract

Each brief includes:

- objective and acceptance criteria;
- exact scope and prohibited scope;
- files or systems the agent may read or modify;
- relevant repository instructions;
- evidence commands to run;
- required result format;
- prohibition on creating additional subagents unless explicitly authorized.

Agents return concise findings, evidence, changed paths if any, verification results, and blockers. Do not paste broad conversation history when a task-specific brief is sufficient.

## Reconcile Results

1. Check every result against its brief.
2. Resolve contradictions before adopting conclusions.
3. Integrate through the designated writer.
4. Run combined verification after integration.
5. Report unavailable agents or reduced independence explicitly.

If multi-agent capability is missing, continue serially with the main agent and note the loss of concurrency or independent review. Do not treat missing agents as proof that work was verified.
