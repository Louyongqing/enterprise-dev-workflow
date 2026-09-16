# Testing Standards

Tests prevent regressions and prove required behavior. Their goal is not to maximize test count.

Prioritize:

- core business rules;
- bug regressions;
- boundary and error cases;
- important APIs and state transitions;
- data transformations;
- behavior that is easy to break.

Do not add tests by default for accessors, framework behavior, logic-free DTOs, pure configuration mapping, or implementation details that do not affect behavior.

Follow the existing test framework and directory structure. Mirror source packages where the project does so. Do not introduce a new test stack for one small change.

For a bug:

```text
Reproduce -> Root cause -> Valuable regression check -> Smallest fix -> Verify
```

When automated infrastructure is absent or unusable, perform the safest available observable check and report the missing regression coverage as `NOT VERIFIED` with the exact reason.
