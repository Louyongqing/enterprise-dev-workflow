---
name: security-review
description: Use after changes involving trust boundaries such as authentication, authorization, payments, uploads, user input, APIs, databases, secrets, sessions, admin features, external URLs, file paths, or commands. Produces scoped findings and minimal remediations.
---

# Security Review

Review the affected trust boundaries after implementation and before completion. Focus on exploitable behavior and the requested change; do not use security review as permission for an unrelated rewrite.

## Define the Review Surface

Start from the approved requirements and actual diff. Identify:

- protected assets and sensitive operations;
- actors, roles, tenants, and privilege levels;
- untrusted inputs and external systems;
- data stores, files, commands, URLs, and network boundaries;
- authentication, authorization, session, and secret boundaries;
- destructive or irreversible operations.

Draw or describe the shortest useful data flow from input to sensitive effect. Mark where identity, authorization, validation, encoding, and integrity checks occur.

Use Sol for security architecture, authentication or authorization design, payment or data-loss risk, cross-tenant access, unsafe command or file handling, and Critical findings. Terra may perform ordinary scoped review. Luna may collect mechanical evidence but does not own high-risk judgments.

## Review the Boundary

Read [the security checklist](references/security-checklist.md) and select only applicable sections. At minimum, check:

1. authentication and session establishment;
2. authorization at the server-side resource or action boundary;
3. input validation, canonicalization, and output encoding;
4. injection paths into queries, commands, templates, logs, and headers;
5. file paths, uploads, archive extraction, and content handling;
6. external URL handling, redirects, callbacks, and server-side requests;
7. secrets, tokens, cookies, error messages, and logs;
8. database constraints, transactions, ownership, and migration safety;
9. replay, race, idempotency, rate-limit, and abuse cases where relevant;
10. secure failure behavior and auditability.

Do not infer protection from UI behavior. Verify enforcement at the trusted boundary. Do not rely on validation performed only by clients or upstream callers.

## Validate Findings

For each suspected issue:

1. identify the attacker-controlled input or missing control;
2. trace it to a protected asset or sensitive effect;
3. verify whether an existing control blocks the path;
4. create a safe reproduction or focused test when practical;
5. separate confirmed findings from assumptions requiring more evidence.

Never run destructive exploit steps against production or external systems. Use local fixtures, isolated environments, or non-mutating evidence unless explicitly authorized with a safety plan.

## Severity

- `Critical`: practical compromise, privilege escalation, cross-tenant access, secret exposure, destructive data impact, or equivalent release blocker.
- `Important`: meaningful defense gap with plausible impact or an incomplete required control.
- `Minor`: localized hardening or clarity improvement with limited direct exploitability.
- `Observation`: relevant context without a confirmed defect.

Severity reflects impact and exploitability, not how easy the code change is.

## Remediate Minimally

Fix the control at the authoritative boundary. Add defense in depth only when it protects a distinct layer. Preserve architecture and compatibility unless they prevent a safe fix.

Add focused positive and negative tests when practical, including unauthorized, cross-tenant, malformed, replayed, or boundary-value cases that match the threat. Re-run affected functional and security checks after the last change.

## Required Report

```text
Security scope: <assets, actors, and trust boundaries>
Threats checked: <applicable checklist sections>
Critical: <count>
Important: <count>
Minor: <count>
Finding: <severity, evidence, impact, location, remediation>
VERIFIED: <control or remediation> - <command or safe interaction> - <result>
NOT VERIFIED: <control> - <exact reason>
Residual risk: <accepted or unresolved risk and owner>
```

Do not describe the change as security-reviewed without stating the reviewed boundary and the checks that were actually performed.
