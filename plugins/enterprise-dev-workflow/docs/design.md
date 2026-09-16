# Enterprise Dev Workflow 2.0 Design

## Purpose

Enterprise Dev Workflow is a task decomposer, scope controller, skill router, engineering-standards guide, and verification guard. It is not a task rating system, an execution-model chooser, or an architecture generator.

The plugin optimizes for correct, maintainable, sufficient work rather than maximum process or code volume.

## Fixed lifecycle

```text
Understand -> Recon -> Decompose -> Scope Lock -> Skill Route
-> Implement -> Quality Check -> Verify -> STOP
```

`enterprise-delivery` is the only implicitly invoked skill. It owns the lifecycle and routes to five explicit bundled skills:

```text
enterprise-delivery
|-- task-decomposition
|-- scope-control
|-- code-quality
|-- systematic-debugging
`-- verification
```

Specialist capabilities such as UI design, browser testing, API design, database engineering, architecture, security review, codebase reconnaissance, and project verification remain external routes. They are selected only when the task actually contains that concern.

## Boundary model

Each implementation task records:

```text
Must Do
May Do
Must Not Do
```

The final diff is checked against the same boundary. Adjacent discoveries are reported and left unchanged unless they block safe completion or the user expands scope.

## Implementation model

The default is local, cohesive implementation using existing project structure. Abstraction requires demonstrated reuse, a real boundary, or an existing convention. SOLID principles guide decisions without requiring extra interfaces or layers.

Large requirements are split by business capability or independently verifiable behavior. Small cohesive requirements remain one task. Bugs use reproduction and root-cause evidence before a patch.

## Completion model

Verification is proportionate to the behavior and risk that changed. Evidence may include targeted tests, build, typecheck, lint, integration checks, browser behavior, API probes, migration checks, and focused security checks. Unavailable material evidence is reported as `NOT VERIFIED` with its exact reason.

Once acceptance criteria are satisfied and required verification passes, the workflow stops. No speculative feature, abstraction, refactor, test, or cleanup is added after that point.

## Package invariants

- Exactly six bundled skills.
- Only `enterprise-delivery` allows implicit invocation.
- No task-level classification contract.
- No responsibility for choosing the host's execution model.
- All local Markdown links resolve inside the plugin.
- Evaluation cases express required routes and outcomes without introducing a hidden rating system.
