---
name: systematic-debugging
description: Use for bugs, test failures, crashes, regressions, and unexpected behavior. Requires evidence and root-cause analysis before implementation changes.
---

# Systematic Debugging

Treat a fix as a causal claim. Establish what failed, why it failed, and why the proposed change addresses that cause before editing production code.

## Entry Conditions

Use this skill for every observed defect, flaky test, unexpected output, performance regression, integration failure, or unexplained environment difference.

If the report cannot yet be reproduced, collect the smallest useful evidence set: exact inputs, expected and actual results, timestamps, versions, relevant logs, and recent changes. Do not convert uncertainty into a guessed fix.

## Phase 1 - Establish the Failure

1. Read repository instructions and inspect workspace state.
2. Capture the exact failing command or interaction.
3. Reproduce consistently when safe, or document why reproduction is unavailable.
4. Reduce the failure to the narrowest reliable case.
5. Record environment, configuration, and dependency differences that may matter.

Luna may collect bounded evidence, search logs, or run a known reproduction. Terra normally owns cross-file diagnosis. Escalate to Sol for architecture, concurrency, security, data integrity, conflicting evidence, or repeated failed hypotheses.

## Phase 2 - Trace the Root Cause

Trace data and control flow backward from the visible failure. At every boundary, compare the value or state that entered with the value or state that left.

Form one falsifiable hypothesis at a time:

```text
Hypothesis: <specific cause>
Evidence supporting it: <observations>
Evidence that would disprove it: <check>
Next experiment: <smallest differentiating test>
```

Prefer evidence that distinguishes competing causes. Do not make several speculative changes and infer causality from a passing result.

Use the bundled references when useful:

- [Root cause tracing](root-cause-tracing.md)
- [Defense in depth](defense-in-depth.md)
- [Condition-based waiting](condition-based-waiting.md)

## Phase 3 - Specify the Fix

Before editing, state:

- the root cause;
- the invariant that was violated;
- the smallest change that restores it;
- the observable behavior that proves the correction;
- the regression risk and affected boundaries.

Add a failing regression test first when the behavior is observable, runnable test infrastructure exists, and the test cost is proportionate. If automated regression coverage is not practical, record the exact reason and choose a concrete alternative check.

## Phase 4 - Implement and Verify

1. Apply one focused root-cause change.
2. Run the narrow reproduction or regression test.
3. Run affected project checks.
4. Inspect nearby paths for the same invalid assumption.
5. Inspect the final diff for speculative edits and debug artifacts.

If the first fix fails, return to evidence and revise the hypothesis. After two failed fix attempts, reassess the model, assumptions, and architecture with Sol rather than stacking another patch.

## Required Report

Report diagnosis separately from verification:

```text
Root cause: <cause and evidence>
Fix: <focused change>
VERIFIED: <claim> - <command or interaction> - <result>
NOT VERIFIED: <claim> - <exact reason>
Residual risk: <none or remaining risk>
```

Never claim a root cause when only a symptom was observed.
