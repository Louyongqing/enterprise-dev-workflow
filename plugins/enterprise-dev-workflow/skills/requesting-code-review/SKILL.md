---
name: requesting-code-review
description: Use after a meaningful implementation increment or before delivery to obtain an independent, evidence-based review of requirements, correctness, risk, tests, and scope.
---

# Requesting Code Review

Review the actual change against its requirements and risk. The reviewer is independent of the implementer whenever agent capability is available.

## Prepare the Review Package

Provide the reviewer with:

- the approved requirement or task brief;
- repository instructions and relevant constraints;
- the exact diff range or review package;
- changed-file summary;
- implementation report and verification evidence;
- known risks, migrations, security boundaries, and intentional exclusions.

Do not ask for a general opinion without a concrete diff and acceptance criteria. The bundled [reviewer prompt](code-reviewer.md) may be used as a starting point, but project requirements remain authoritative.

## Select the Reviewer

Use Terra for ordinary independent review. Luna is acceptable for a tiny, mechanical, low-risk diff with complete acceptance criteria. Use Sol for architecture, concurrency, security, migrations, data integrity, Critical findings, unclear intent, or low reviewer confidence.

The reviewer must not be the agent that authored the change. If subagents are unavailable or not authorized, perform a structured main-agent self-review and report:

```text
NOT VERIFIED: independent code review
Reason: <capability or authorization limitation>
```

Self-review is still required; it is not described as independent.

## Review Order

1. Check requirement and acceptance-criteria compliance.
2. Check correctness, error paths, edge cases, and regressions.
3. Check tests for meaningful behavior and missing negative cases.
4. Check security, data, API, migration, concurrency, and compatibility risks that apply.
5. Check maintainability, dependency boundaries, and unnecessary complexity.
6. Check final scope for unrelated changes, secrets, debug artifacts, and generated noise.

Classify findings:

- `Critical`: unsafe to deliver; security, data loss, corruption, or fundamental incorrectness.
- `Important`: material requirement, correctness, regression, or maintainability gap.
- `Minor`: localized improvement that does not block the requested outcome.

Every finding includes file and location when possible, evidence, impact, and a specific remediation direction. Do not inflate stylistic preferences into blockers.

## Resolve and Re-review

Fix all confirmed Critical and Important findings before completion. Re-review the fix diff, not just the original implementation report. Escalate to Sol when a finding is disputed on architecture or safety grounds, or when two review/fix cycles fail to converge.

Report the final state:

```text
Review: independent | self-review only
Reviewer model: Luna | Terra | Sol
Critical: <count>
Important: <count>
Minor: <count>
Resolved: <summary>
Open: <finding and disposition>
```
