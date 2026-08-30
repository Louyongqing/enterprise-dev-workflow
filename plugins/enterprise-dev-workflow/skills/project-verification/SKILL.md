---
name: project-verification
description: Use as the final evidence-based quality gate after software changes. Selects and runs applicable build, typecheck, lint, test, browser, API, migration, security, and final-diff checks.
---

# Project Verification

Verify the delivered behavior in proportion to its risk. This is the project-level gate; [verification-before-completion](../verification-before-completion/SKILL.md) governs the claims made from the evidence.

## Build the Verification Matrix

Read repository instructions, package scripts, CI configuration, changed paths, the approved acceptance criteria, and the final diff. Use [the verification matrix](references/verification-matrix.md) to select applicable checks.

For every selected check, record:

- the claim it supports;
- the exact command or interaction;
- the expected success condition;
- the actual exit status and result;
- whether the evidence is current after the last relevant change.

Do not run every possible command mechanically. Run every check needed to support the requested outcome and affected risk boundaries.

## One Current Evidence Ledger

Share this ledger with verification-before-completion and review; do not create separate duplicate check runs just to satisfy each skill. Record when a check ran and the relevant workspace/configuration/dependency/environment state it covered. Current successful checks from this run may be reused if those inputs and the complete output remain available and unchanged.

Rerun affected checks when relevant state changes, provenance is uncertain, output is incomplete, or the result is flaky. Recheck broad suites when a shared dependency/configuration change invalidates them. Previous-session reports and unverified agent summaries do not qualify. Refresh the final diff/status inspection after the last edit even when test evidence is reusable.

## Verification Order

Use the fastest useful feedback first, then broader and higher-cost checks:

1. focused regression or changed-module tests;
2. static checks such as format, lint, schema, and typecheck;
3. unit and integration suites for affected components;
4. build or packaging checks;
5. API, database, migration, security, and compatibility checks that apply;
6. browser or end-to-end interactions for user-visible behavior;
7. final diff, status, generated artifact, secret, and debug-artifact inspection.

If a prerequisite fails, record the failure. Continue with independent safe checks when they still provide useful evidence, but do not bury the prerequisite failure.

## Behavior Verification

Verify the requirement at the closest observable boundary:

- Bugs: run the original reproduction or a meaningful regression test.
- UI: exercise the relevant flow in a browser, inspect console output, and check responsive or state behavior that changed.
- API: verify contract, validation, authorization, error behavior, and relevant status or schema outcomes.
- Database: verify migration direction, constraints, transactions, compatibility window, rollback approach, and data integrity.
- Security: load [security-review](../security-review/SKILL.md) for affected trust boundaries and include its evidence.
- Packaging or plugins: run the official validator and installation or load path when the environment permits.

Never claim a page works without exercising it. Never claim a migration is safe from a schema compile alone.

## Final Scope Inspection

Inspect the final diff and workspace status for:

- unrelated user changes or accidental scope expansion;
- secrets, tokens, credentials, private keys, or sensitive fixtures;
- debug logs, disabled checks, temporary files, and placeholders;
- missing tests, migrations, generated files, documentation, or notices;
- dependency or lockfile changes that lack an intentional cause;
- remaining merge markers or formatting damage.

Preserve unrelated dirty-worktree changes and identify them separately from the implementation.

## Evidence Report

Use this table or an equivalent concise ledger:

| Area | Claim | Command or interaction | Result | Status |
|---|---|---|---|---|
| Tests | <claim> | `<command>` | <exit and summary> | VERIFIED / FAILED / NOT VERIFIED |

Then list any residual limitations exactly:

```text
VERIFIED: <claim> - <current evidence>
FAILED: <claim> - <failure and impact>
NOT VERIFIED: <claim> - <exact reason>
```

A failed required gate means the implementation is not ready. An unavailable gate remains `NOT VERIFIED`; it does not become a pass because the code looks correct.
