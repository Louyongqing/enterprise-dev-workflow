---
name: task-decomposition
description: Use when a software requirement is too broad for one independently understandable and verifiable unit. Splits work by business capability, dependencies, scope, acceptance criteria, and verification without fragmenting it into line-level chores.
---

# Task Decomposition

Split a large requirement before implementation. A task is the smallest business or technical unit that one agent can independently understand, implement, and verify.

## When to split

Split when the request contains multiple user-visible capabilities, crosses independent module boundaries, has ordered dependencies, or cannot be verified with one coherent outcome. Do not split a cohesive small change merely to create ceremony.

## Task shape

Use [the task template](../../references/task-template.md). Each task records:

- one clear goal;
- direct inputs and dependencies;
- expected files or areas, when known;
- acceptance criteria that can be observed;
- explicit out-of-scope work;
- proportionate verification.

Decompose by business capability, independently verifiable behavior, a specific bug, or a necessary technical step. Do not create tasks such as "change line 23," "add an if," or "declare a variable."

Order tasks only when a real dependency exists. Identify integration verification separately when several tasks must work together. Once the tasks cover the requested result, stop decomposing.
