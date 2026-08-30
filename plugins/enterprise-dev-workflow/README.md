# Enterprise Dev Workflow

Enterprise Dev Workflow is a self-contained Codex plugin for risk-aware software delivery. It applies the lightest workflow that matches the work while requiring current evidence before completion claims.

## Routing levels

- **L1 - Routine change:** clear, isolated, low-risk work. No brainstorming, implementation plan, review loop, or subagent by default.
- **L2 - Complex feature:** non-trivial, cross-module, interface, or architectural work. Reuses applicable design approval and plans; otherwise requires the missing design/plan decision. Bounded work can use a concise plan. Independent review and final verification remain required.
- **L3 - High-risk change:** authentication, authorization enforcement, payments, uploads, external URLs, files, commands, secrets, admin capabilities, migrations, production data, concurrency, destructive operations, or material integrity risk. Permission-settings UI or configuration plumbing remains L2 when it does not change server-side authorization decisions or enforcement. L3 adds Strong-model risk decisions and scoped security review.

Hidden complexity upgrades the level. It never silently downgrades discovered risk.

Risk and scheduling are separate: overlapping writers have an L2 floor, but authorization, migrations and other L3 boundaries remain L3. Mere mentions of a URL, file or permission label do not automatically make a documentation/display change high-risk.

## Approval and evidence reuse

Reuse explicit user approvals when scope, interfaces, acceptance criteria, risk and allowed actions remain unchanged. Reapprove material deltas; do not treat a prior approval as permission for new external/destructive actions. Architectural and L3 work retains durable safety/rollback plans.

Verification skills share one current evidence ledger. Reuse complete checks from the same run only when relevant inputs/environment are unchanged; rerun invalidated or uncertain checks. Final diff/status inspection is always required.

## Model policy

- **Strong - `gpt-5.6-sol`:** requirements, architecture, decomposition, security decisions, concurrency, migrations, critical findings, and high-risk integration.
- **Standard - `gpt-5.6-terra`:** routine engineering judgment, bounded multi-file implementation, test design, integration analysis, and default independent review.
- **Economy - `gpt-5.6-luna`:** search, extraction, mechanical edits, repetitive work, and executing established tests.

When a preferred model is unavailable, the workflow selects the closest available tier and records the substitution instead of retrying a nonexistent model.

Model preferences are not automatic host controls. The current main model does not change because a skill names another model. Report actual model/usage only from host evidence, and never invent token or quota savings. The optional comparison procedure is in `skills/model-routing/references/evaluation.md`.

## Agent safety

The plugin defaults to one writer. Read-only analysis may run in parallel. Parallel writes require provably disjoint file ownership or existing isolated workspaces, no shared interface changes, and no dependency on shared uncommitted state.

Multi-agent support is optional. When unavailable or unauthorized, work continues serially through the main agent.

## Optional visual companion

The brainstorming skill can offer a local browser companion when a visual comparison would materially help. It starts only after user approval, binds to loopback by default, and creates a new key, port, and unpredictable owner-only OS runtime/temp directory for every launch. If project persistence is selected, visual content is written to a symlink-checked session under `.enterprise-dev-workflow/brainstorm/`; each generated session has a self-ignoring `.gitignore`, while authenticated state stays outside the project. A restart requires opening the newly returned complete URL. Remove or revise the generated `.gitignore` only when those mockups are intentionally versioned.

The companion does not automatically load third-party brand images. Its upstream attribution link is contacted only if the user chooses to open it.

## Verification

Completion claims require current-environment evidence. Applicable checks may include build, typecheck, lint, unit/integration/E2E tests, browser behavior, API compatibility, migrations, security-sensitive paths, and final diff/status review.

Unavailable checks are reported explicitly:

```text
NOT VERIFIED: <check>
Reason: <exact reason>
```

## Installation

This package is distributed through the `enterprise-dev-workflow` GitHub marketplace:

```powershell
codex plugin marketplace add https://github.com/Louyongqing/enterprise-dev-workflow
codex plugin add enterprise-dev-workflow@enterprise-dev-workflow
```

Restart Codex or start a new task after installation so skill discovery uses the installed package.

Runtime routing is not considered validated until the representative cases in `evals/routing-cases.json` have been exercised in a fresh task.

## Development checks

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/validate_routing_contract.py .
python -B scripts/summarize_eval_runs.py <reviewed-run-records.json>
```

Package/schema tests do not certify agent behavior. The evaluation set includes composite risks, approval/evidence reuse, Chinese prompts and missing telemetry. `evals/delivery-fixture/` contains deliberately defective, isolated test inputs; copy them to a temporary workspace before evaluation and never deploy them. Use `evals/check_delivery_fixture.py` to independently check trusted resulting artifacts.

See `docs/verification.md` for package evidence, behavioral-evaluation boundaries, and limitations.

## License

Original plugin content is MIT licensed. Vendored and adapted Superpowers content retains its upstream MIT terms; see `THIRD_PARTY_NOTICES.md`.
