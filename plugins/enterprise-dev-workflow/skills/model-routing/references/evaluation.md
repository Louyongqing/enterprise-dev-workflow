# Workflow Evaluation and Usage Evidence

Read this only for an explicit optimization comparison, regression evaluation, or material routing investigation. It is not a per-task reporting requirement.

## Separate Four Claims

1. Package checks validate structure, policy metadata, links and evaluation schema.
2. Blind forward tests validate the consuming agent's actual decisions, not the presence of phrases in a skill.
3. Executable fixture/project tests validate changed behavior and artifacts; a routing dry-run cannot substitute for them.
4. Resource comparisons need measured, comparable runs. Shorter instructions are not proof of quota or monetary savings.

Use `evals/routing-cases.json` at the plugin root as the evaluator's acceptance contract. Do not show expected answers or prior conclusions to the tested agent. Give only the request, relevant skills and raw artifacts. Keep activation actually observed separate from skills planned for a later lifecycle stage. Score outcomes against evidence, not preferred wording. Test combined risks and approval/evidence boundaries as well as isolated happy paths.

For execution, copy `evals/delivery-fixture/` into an isolated temporary workspace. Its seeded defects are test inputs, not production code. Inspect the resulting diff and run independent acceptance checks. Do not use production data, network services or secrets. A small fixture pass is not enterprise-wide certification.

## Run Records

Only record actual observations. `scripts/summarize_eval_runs.py <records.json>` reads a supplied JSON array and prints a summary; it does not read private session logs, run models, collect telemetry, or upload anything.

Each record contains:

- `case_id`, `variant` (`baseline` or `candidate`), `fixture_id`, `environment`: nonempty strings identifying comparable work and conditions.
- `requested_model`, `actual_model`: string or null; actual means reported by the execution host, not inferred from a request or an agent's assertion.
- `outcome`: `PASS`, `FAIL` or `NOT VERIFIED`, based on reviewed output/artifacts and the applicable quality gate.
- `evidence`: nonempty references to the inspected result/artifact/commands. These are evidence pointers, not executable commands.
- `elapsed_seconds`, `input_tokens`, `output_tokens`, `rework_cycles`: nonnegative numbers/integers as appropriate, or null when unavailable.

Use a unique case ID per paired trial. Match fixture content/revision and environment between baseline/candidate, including tool availability, task constraints and approval state. Both arms must pass the same acceptance criteria. Record requested and actual models even when intentionally comparing different model routes.

The summarizer reports token reduction only for complete, matched, passing pairs with known actual models and token counts. Unknown values remain null and excluded comparisons are explained. A pass label alone is not proof: the caller must inspect the underlying evidence. The summary is a calculation over supplied observations, not a certification of those observations.

Report input/output tokens separately where possible. Cached-input billing and subscription quota rules can differ; token reduction is not money or quota reduction. Do not estimate unavailable quota percentages, hidden reasoning tokens, or actual model identity. For broader conclusions, repeat representative trials; a single small example is not a general savings claim.
