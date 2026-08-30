---
name: verification-before-completion
description: Use before claiming software work complete, fixed, healthy, or ready. Match each claim to current evidence and disclose missing checks.
---

# Verification Before Completion

Validate claims against the current ledger maintained by [project-verification](../project-verification/SKILL.md). This is a claim gate, not a second test runner.

## Evidence Reuse

A check already executed successfully in this run can support multiple claims when its command/interaction, relevant code/configuration/dependencies/environment, and complete result are unchanged. Read the result and verify that it covers the claim; do not rerun it solely because this skill loaded.

Rerun affected checks after a relevant change, an uncertain state comparison, missing/incomplete output, or a reproducibility-sensitive/flaky result. Previous-session reports and unverified child summaries are not current evidence. A dependency or shared configuration change may invalidate many checks.

Use evidence only at its demonstrated scope: lint is not a build, a build is not UI behavior, and a routing dry-run is not delivered implementation. The original failure path needs a reproduction/regression check. Final diff/status inspection remains required.

## Claims and Stop Conditions

Report concisely, reusing the ledger instead of duplicating a second table:
```text
VERIFIED: <claim> - <command/interaction and current result>
FAILED: <claim> - <failure and impact>
NOT VERIFIED: <claim> - <exact reason>
```

Do not declare completion/readiness when a required check failed or was not run, evidence is stale, the original failure is untested, or final scope is uninspected. Continue fixing only when authorized and safe; otherwise hand off the remaining condition. Confidence and plausible code never replace evidence.
