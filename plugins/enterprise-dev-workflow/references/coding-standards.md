# Coding Standards

## Smallest sufficient implementation

Implement only what the current goal and acceptance criteria require. Do not add caches, queues, frameworks, providers, factories, permission layers, or extension points because they may be useful later.

Prefer local implementation first. Observe real repetition before generalizing: implement the business need once, watch for real repetition the next time, and consider abstraction only after the pattern is proven. This is a judgment aid, not a mandatory occurrence count. Existing project abstractions remain valid when they already fit the task.

## SOLID without ceremony

- Single responsibility: group code that changes for the same business reason; do not split a simple flow into many tiny classes.
- Open/closed: preserve a stable extension point when one already exists; do not create one for a hypothetical future implementation.
- Liskov substitution: honor existing inheritance and polymorphism; do not introduce inheritance merely to demonstrate the principle.
- Interface segregation: keep real interfaces focused; one implementation does not automatically require an interface.
- Dependency inversion: use it at meaningful domain, infrastructure, or external-system boundaries; ordinary local CRUD does not always need another layer.

## Cohesion and coupling

Keep code for one business capability close to its module. Avoid dumping domain rules into generic `common`, `helper`, `manager`, `processor`, `executor`, `utils`, or `misc` locations.

Do not bypass layers, create service cycles, expose repository details to unrelated modules, make UI depend on backend internals, or put specific business rules in a generic shared module.

## Naming and methods

Use business verbs and nouns such as `createOrder`, `uploadAvatar`, `activeUsers`, or `paymentResult`. Avoid vague names such as `handle`, `process`, `execute`, `data`, `info`, `obj`, and `temp` when context does not make them precise.

Prefer cohesive methods and readable control flow. Extract a method for a meaningful operation, real duplication, difficult logic, testability, or boundary clarity, not to satisfy an arbitrary line limit.

## Directories and packages

Inspect the existing structure first. Put new code in an appropriate existing location. Create a directory only for a demonstrated business or architectural boundary, and mirror the project's test layout.

## Errors and refactoring

Reuse the project's exception, result, error code, and global handling conventions. Add distinct error types only when a caller must react differently.

Do not refactor unrelated code. Refactor when the requested task is a refactor, current code directly blocks safe implementation, or relevant duplication materially harms this change.

## Specialized surfaces

- Frontend: reuse the design system, components, state management, and API wrapper; verify real page behavior after UI changes.
- API: keep names, schemas, auth, validation, status/error format, and versioning consistent with the existing contract.
- Database: inspect the schema and real queries first; use tracked migrations, evidence-based indexes, compatible changes, and no unrelated table edits.
- Security: follow existing controls and route a focused review only when a real trust boundary is affected.
