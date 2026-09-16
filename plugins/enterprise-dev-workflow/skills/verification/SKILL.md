---
name: verification
description: Use before declaring a software change complete. Selects the smallest sufficient evidence for the affected behavior, runs applicable checks, inspects final scope, reports unavailable checks as NOT VERIFIED, and stops when acceptance criteria are proved.
---

# Verification

Completion is a claim backed by current evidence.

## Select checks

Choose checks from the acceptance criteria, changed files, repository instructions, manifests, CI, and affected boundaries. Start narrow, then run broader build, typecheck, lint, unit, integration, API, browser, migration, or security checks only when they materially support the changed behavior.

- Bugs: re-run the original reproduction and regression check.
- UI: exercise the affected behavior in a real browser when available.
- APIs: verify request, response, error, authentication, and consumer/server alignment as applicable.
- Databases: verify migrations and affected queries against disposable data; never use production data without explicit authority.
- Sensitive boundaries: run the focused security review and denied/error paths.

## Evidence rules

- Never claim a test passed unless it ran successfully in the current environment.
- Never claim a build is healthy without running the applicable build.
- Never claim a page works without exercising the relevant behavior.
- Reuse same-run evidence only when code, dependencies, configuration, and environment relevant to that claim are unchanged.
- Report skipped, unavailable, timed-out, flaky, or failing checks as they are.

Use this format for a material missing check:

```text
NOT VERIFIED: <check>
Reason: <exact reason and impact>
```

## Final scope check

Inspect the final diff and status for unintended files, unrelated edits, secrets, debug artifacts, missing tests, missing migrations, and unnecessary complexity. Confirm that `Must Do` is complete and `Must Not Do` is untouched.

When acceptance criteria are satisfied and the required checks pass, stop. Additional cleanup is not part of verification.
