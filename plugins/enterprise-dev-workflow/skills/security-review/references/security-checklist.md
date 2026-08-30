# Scoped Security Checklist

Select checks that intersect the requested change and actual data flow. Record non-applicable sections rather than pretending they were tested.

## Identity and Session

- Authentication is enforced at the trusted boundary.
- Account recovery, enrollment, and identity linking cannot bypass the primary control.
- Sessions and tokens use appropriate expiry, rotation, revocation, audience, and issuer checks.
- Cookies use secure attributes appropriate to the deployment.
- Sensitive changes require the intended level of re-authentication.

## Authorization and Tenancy

- Every protected action verifies the actor, action, resource, and tenant server-side.
- Object identifiers do not grant access by possession.
- List, read, create, update, delete, export, and bulk paths enforce consistent policy.
- Admin and service capabilities are least-privileged and auditable.
- Default behavior denies access when policy data is missing or ambiguous.

## Input, Output, and Injection

- Inputs are validated against an explicit schema and size limits.
- Canonicalization occurs before allowlist, ownership, or path decisions.
- Queries and commands use parameterized or structured APIs.
- Untrusted content is encoded for its output context.
- Logs, headers, templates, and error messages cannot be injected or split.

## Files and Uploads

- Paths are resolved and constrained beneath an intended root.
- Filenames are not trusted as storage paths.
- File type, size, count, and content checks match the threat model.
- Archive extraction prevents traversal, links, bombs, and overwrite.
- Uploaded content is served with safe disposition and content-type behavior.
- Temporary and generated files have safe permissions and lifecycle.

## External URLs and Network Calls

- URL schemes and destinations follow an allowlist or equivalent policy.
- Redirects and DNS resolution cannot bypass destination restrictions.
- Callback state, signatures, timestamps, and replay controls are verified.
- Timeouts, response-size limits, and failure handling prevent resource abuse.
- Credentials are not forwarded to untrusted destinations.

## Data and Persistence

- Constraints enforce ownership, uniqueness, and integrity assumptions.
- Transactions protect multi-step invariants.
- Queries are scoped by tenant or owner at the data boundary.
- Migrations have forward, rollback, compatibility, and backup considerations.
- Sensitive data has appropriate retention, redaction, and deletion behavior.

## Secrets and Observability

- Secrets are not committed, logged, returned in errors, or exposed to clients.
- Tokens and credentials are stored and compared using appropriate mechanisms.
- Audit events identify actor, action, target, outcome, and correlation context without leaking secrets.
- Security failures are observable without revealing exploitable details.

## Abuse, Concurrency, and Failure

- Rate limits and quotas cover the meaningful identity or resource.
- Idempotency and replay controls protect repeated sensitive requests.
- Concurrent operations cannot bypass limits or corrupt invariants.
- Partial failures are safe and recoverable.
- Destructive actions require appropriate confirmation, authorization, and scope validation.
