---
name: test-driven-development
description: Use when enterprise-delivery determines automated test-first development is practical for a feature, bug fix, or behavior change. Skip fake coverage when no meaningful runnable test is available.
---

# Test-Driven Development

Use test-first development when it provides real evidence. This skill is explicit-only and follows the risk decision made by `enterprise-delivery`.

When writing or changing tests, read [writing-good-tests.md](writing-good-tests.md).

## TDD Required

Use Red-Green-Regression-Verification when all are true:

- runnable test infrastructure exists;
- changed behavior can be observed meaningfully through automation;
- the test represents the actual requirement or regression;
- test cost is proportionate to the change risk.

### Red

Write one minimal test that demonstrates desired observable behavior. Before writing it, name the production mistake that should make it fail. Derive expected values independently from the implementation.

### Confirm Red

Run the narrow test and observe the expected failure. It must fail because behavior is missing or wrong, not because of syntax, setup, or environment errors.

If it passes immediately, the test does not establish the new behavior. Correct the test or confirm the behavior already exists.

### Green

Write the smallest implementation that makes the test pass. Do not add unrelated features or refactors.

### Regression and Refactor

Run the narrow test, then the relevant broader suite. Refactor only while tests stay green. Keep test-only helpers out of production code.

### Verification

Run the applicable project verification after the TDD loop. Passing one new test is not proof that the build, integration, UI, migration, or security behavior is healthy.

## TDD Not Practical

Automated TDD is not required when any applies:

- the project has no suitable test infrastructure;
- the current environment cannot run it;
- the change is generated code or purely declarative configuration;
- the only possible test would assert source wording or manufacture fake coverage instead of validating behavior.

Do not introduce a testing framework solely to satisfy ceremony unless the user authorizes that scope. Continue with the best safe verification and report:

```text
NOT VERIFIED: automated regression test
Reason: <exact reason>
```

Absence of a runnable test environment must never be reported as tests passing.

## Good-Test Gate

A test earns its place only when:

- it names a real break it would catch;
- it exercises the real component rather than asserting on a mock;
- expected values are hand-derived;
- it tests public behavior or meaningful side effects, not exact prose or private structure;
- a realistic mutation would make it fail.

If none of these are possible, use the `TDD Not Practical` path and document the limitation.
