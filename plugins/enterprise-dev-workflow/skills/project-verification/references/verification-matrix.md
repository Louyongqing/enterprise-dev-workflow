# Verification Matrix

Select rows affected by the change. Add project-specific checks from repository instructions and CI configuration.

| Change surface | Minimum evidence | Additional risk-scaled evidence |
|---|---|---|
| Pure documentation | Link and reference checks; final diff | Render or example validation when formatting matters |
| Library or module | Focused tests; typecheck or compile | Broader unit suite; compatibility matrix |
| Backend behavior | Unit or integration test; typecheck; lint | API contract, authorization, failure path, load or concurrency check |
| Public API contract | Schema or contract test; positive and negative requests | Version compatibility, idempotency, pagination, rate-limit behavior |
| Database schema | Migration validation; model compile; integrity checks | Forward and rollback rehearsal, backfill, lock and performance analysis |
| Authentication or authorization | Positive and denied-path tests | Cross-role, cross-tenant, session, replay, and audit checks |
| File or upload flow | Boundary tests; path and size validation | Content-type, archive, malware, storage, and cleanup checks |
| User interface | Component or state tests; browser interaction | Responsive states, accessibility, console, network, and visual comparison |
| Build or packaging | Production build or package validator | Clean install, artifact inspection, supported-platform check |
| Dependency change | Install or lockfile consistency; build | Vulnerability, license, size, and compatibility review |
| Concurrency or jobs | Deterministic tests for ordering and retry | Race, duplicate delivery, cancellation, timeout, and recovery checks |
| Performance change | Representative measurement and baseline | Load profile, resource use, regression threshold |

## Always Inspect

- Repository and nested instructions were followed.
- Exact acceptance criteria are covered by evidence.
- Final diff and status match intended scope.
- Secrets, debug artifacts, placeholders, and merge markers are absent.
- Skipped or unavailable checks are reported as `NOT VERIFIED` with exact reasons.
