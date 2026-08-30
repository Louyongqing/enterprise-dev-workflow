"""Calculate usage summaries from supplied evidence; never collect telemetry."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

VARIANTS = ("baseline", "candidate")
COUNTERS = ("input_tokens", "output_tokens", "rework_cycles")


def validate_record(record):
    if not isinstance(record, dict):
        raise ValueError("each run must be an object")
    for field in ("case_id", "variant", "fixture_id", "environment"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"{field} must be a nonempty string")
    if record["variant"] not in VARIANTS:
        raise ValueError("variant must be baseline or candidate")
    if record.get("outcome") not in ("PASS", "FAIL", "NOT VERIFIED"):
        raise ValueError("outcome must be PASS, FAIL or NOT VERIFIED")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or any(
        not isinstance(item, str) or not item.strip() for item in evidence
    ):
        raise ValueError("evidence must contain nonempty evidence references")
    for field in ("requested_model", "actual_model"):
        value = record.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{field} must be a nonempty string or null")
    for field in COUNTERS + ("elapsed_seconds",):
        value = record.get(field)
        if value is None:
            continue
        valid_type = type(value) in ((int, float) if field == "elapsed_seconds" else (int,))
        if not valid_type or value < 0 or (isinstance(value, float) and not math.isfinite(value)):
            raise ValueError(f"{field} must be finite, nonnegative and {'numeric' if field == 'elapsed_seconds' else 'integer'}, or null")


def known_sum(records, field):
    values = [record.get(field) for record in records]
    if not values or any(value is None for value in values):
        return None
    total = sum(values)
    if isinstance(total, float) and not math.isfinite(total):
        raise ValueError(f"{field} aggregate must be finite")
    return total


def summarize_runs(records):
    if not isinstance(records, list) or not records:
        raise ValueError("expected a nonempty run array")
    arms = {variant: {} for variant in VARIANTS}
    for record in records:
        validate_record(record)
        arm = arms[record["variant"]]
        if record["case_id"] in arm:
            raise ValueError("duplicate case/variant; use a unique case ID for each trial")
        arm[record["case_id"]] = record

    variants = {}
    for variant, arm in arms.items():
        runs = list(arm.values())
        metrics = {field: known_sum(runs, field) for field in COUNTERS + ("elapsed_seconds",)}
        metrics["total_tokens"] = (
            metrics["input_tokens"] + metrics["output_tokens"]
            if metrics["input_tokens"] is not None and metrics["output_tokens"] is not None else None
        )
        variants[variant] = dict(
            runs=len(runs), passed=sum(r["outcome"] == "PASS" for r in runs),
            failed=sum(r["outcome"] == "FAIL" for r in runs),
            not_verified=sum(r["outcome"] == "NOT VERIFIED" for r in runs),
            actual_models=sorted({r["actual_model"] for r in runs if r.get("actual_model")}),
            **metrics,
        )

    reasons = []
    comparable = 0
    for case_id in sorted(set(arms["baseline"]) | set(arms["candidate"])):
        before, after = (arms[variant].get(case_id) for variant in VARIANTS)
        if before is None or after is None:
            reasons.append(f"{case_id}: missing comparison arm")
            continue
        if any(before[field] != after[field] for field in ("fixture_id", "environment")):
            reasons.append(f"{case_id}: different fixture or environment")
            continue
        if before["outcome"] != "PASS" or after["outcome"] != "PASS":
            reasons.append(f"{case_id}: both arms must pass reviewed quality gates")
            continue
        if any(not run.get("actual_model") for run in (before, after)):
            reasons.append(f"{case_id}: actual model NOT VERIFIED")
            continue
        if any(run.get(field) is None for run in (before, after) for field in ("input_tokens", "output_tokens")):
            reasons.append(f"{case_id}: token counts NOT VERIFIED")
            continue
        comparable += 1

    reduction = None
    before_tokens = variants["baseline"]["total_tokens"]
    after_tokens = variants["candidate"]["total_tokens"]
    if not reasons and comparable and before_tokens is not None and after_tokens is not None:
        if before_tokens > 0:
            try:
                reduction = round((before_tokens - after_tokens) / before_tokens * 100, 4)
            except OverflowError as exc:
                raise ValueError("token comparison is outside finite numeric range") from exc
            if not math.isfinite(reduction):
                raise ValueError("token comparison must be finite")
        else:
            reasons.append("baseline tokens are zero; percentage is undefined")
    return dict(
        variants=variants, comparable_pairs=comparable,
        token_reduction_percent=reduction, not_verified=reasons,
        limitation="Calculation over supplied records only. Inspect evidence independently; token reduction is not subscription quota or monetary savings.",
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path)
    args = parser.parse_args(argv)
    try:
        records = json.loads(args.records.read_text(encoding="utf-8"))
        result = summarize_runs(records)
        serialized = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)
    except (OSError, UnicodeError, ValueError, OverflowError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
