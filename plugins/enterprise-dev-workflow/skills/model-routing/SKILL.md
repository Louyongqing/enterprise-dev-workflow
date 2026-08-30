---
name: model-routing
description: Use for model selection, justified delegation, review escalation, or unavailable-model fallback in software work.
---

# Model Routing

Choose the least expensive available model that can reliably handle the role. A skill is guidance, not a model-switching mechanism.

## Capability Tiers

| Tier | Preferred model | Responsibility |
|---|---|---|
| Strong | gpt-5.6-sol | Ambiguous requirements, architecture, security, concurrency, migrations/rollback, data-loss risk, Critical findings and high-risk integration |
| Standard | gpt-5.6-terra | Ordinary engineering implementation, evidence analysis, test design, compatibility checks and first independent review |
| Economy | gpt-5.6-luna | Bounded search/extraction, exact mechanical work, established command execution and tiny mechanical reviews |

Consider complexity, ambiguity, coupling, and actual risk. Strong decides consequential uncertainty; return bounded execution to Standard/Economy afterward. Do not require a Sol coordinator for every routine task.

## Host and Authorization Boundary

Inspect the host's allowed roster and permitted model controls before dispatch. Select the model only through an available authorized control; do not modify global settings, create a new user task, or spawn an agent solely to simulate switching the current main model.

The main task's model remains whatever the host actually uses. Distinguish a recommendation/request from observed execution. If a preferred model is unavailable, choose the nearest permitted capable tier without repeated retries. If capability is insufficient for a mandatory high-risk decision, continue safe evidence collection but report the decision as NOT VERIFIED and block unsafe implementation/delivery.

Report an actual substitution:
```text
MODEL SUBSTITUTION
Requested: <preferred model>
Used: <host-reported actual model or NOT VERIFIED>
Reason: <availability, authorization, or capability limit>
```

Never claim that naming a model in prose changed it.

## Delegation Cost Gate

Delegate only when the bounded deliverable is worth dispatch, context, review, and integration overhead. Give the child the exact task, relevant files/contracts, permissions, stop condition, and required evidence—not the entire conversation by default.

Prefer one writer and useful read-only parallel work. Parallel writers need disjoint file/interface ownership and verified isolation; no shared unfinished dependencies. Usually two or three bounded assignments are sufficient. Respect the host's limits and delegation authorization.

## Review and Escalation

Start independent review with Terra; Luna is sufficient only for a tiny mechanical low-risk diff. Sol owns high-risk/security/concurrency/migration review and Critical adjudication.

Escalate for material uncertainty, conflicting requirements/evidence, unexpected architecture/public-contract changes, security/data-loss/concurrency risk, or two failed meaningful attempts/review-fix cycles. One ordinary test failure is evidence to investigate, not an automatic upgrade. Do not repeat failed cheap attempts indefinitely or add a Sol review after every successful Terra review.

The main agent inspects important changes and reconciles evidence; an agent's success report is not proof.

## Measuring Optimization

Only when a comparison is requested or useful, read [evaluation.md](references/evaluation.md). Record host-reported actual models, elapsed time, tokens and rework when available; unknown metrics stay null/NOT VERIFIED. Do not add a metrics ceremony to every L1 task or infer subscription-quota savings from prompt size or model names.
