#!/usr/bin/env python3
"""Prove `scripts/ingest_terralith.py` still reads a choudoufu scale record —
and a chant one — the way it says it does.

Nothing else in this repository runs the ingest at all — `just check` and
`.github/workflows/docs.yml` validate and render whatever is already sitting
in `results/`, so a schema drift between this repo and choudoufu's own
`ScaleRecord` (see `tools/gauntlet/scalerecord.go` there), or chant's own
record (`test/scale-estate.sh` there), would only be noticed the day a
published number went wrong. This test ingests small, committed scale
records — one choudoufu-shaped invocation, one chant-shaped invocation — and
diffs each result against a committed expectation, so that drift is a red
test here instead.

Fixtures live under `tests/fixtures/ingest_terralith/` — this repository has
no other tests and so no established convention; `tests/fixtures/<script
name>/` was chosen so a second script gaining a test does not have to
invent a new layout or collide with this one's file names. It holds:

  gauntlet-scale.json   a two-record ScaleArtifact, laid out the way
                        choudoufu#1053 actually shipped it (after its own
                        correction): one floci record WITH both `plan_calls`
                        — an ordinary plan's cold/warm call count for
                        choudoufu, cold carrying the stock oracle's own count
                        beside it — AND `audit_calls` — the account-inventory
                        audit's separate sweep/read_pass split, its own
                        stock oracle on the read_pass leg — exercising the
                        populated branch of `independence_block()` (which
                        reads only `plan_calls`) and `measurement_block()`'s
                        `plan_calls_cold`/`plan_calls_warm`/`plan_calls_note`/
                        `stock_read_pass_calls` (from `plan_calls`) alongside
                        `adoption_sweep_calls`/`adoption_read_pass_calls`/
                        `adoption_stock_read_pass_calls` (from `audit_calls`)
                        — and one aws record with NEITHER `plan_calls` NOR
                        `audit_calls` and a failing `test_apply` stage,
                        exercising the null/reason branch, the throttle/retry
                        summing, and a mixed pass/fail score. That pairing
                        (floci measured, aws not yet) matches every real
                        record in `live/gauntlet-scale.json` today. The floci
                        record's `cold` and `warm` plan legs are deliberately
                        equal (5 calls each), the same equality the real
                        79-resource row shows (186 each) — see
                        `plan_calls_note` in `expected/`.
  gauntlet.json         a minimal companion carrying `duration_s` for only
                        the floci record's commit — so one expected result
                        gets `effort.wall_seconds` and the other proves the
                        "commit not found" path leaves it out
  chant-scale-record-1.json   a schema-3 chant record with every optional
                        field present — `stages.cold_deploy.stacks[]`,
                        `median_seconds`, `anomaly_detected`, and `seconds`/
                        `detail`/`by_action` on all three reads — exercising
                        the populated branch of `chant_measurement_block()`
                        and `chant_effort_block()`.
  chant-scale-record-2.json   a schema-2 chant record with none of those —
                        no `emulator`, no `seconds` anywhere, no `per_stack`,
                        no schema-3 deploy fields — exercising the
                        absent-optional-field branch of the same two
                        functions, the same way `gauntlet-scale.json`'s
                        second record does for choudoufu's `plan_calls`.
  expected/*.json       the exact result set `ingest_terralith.py` must
                        produce from the fixtures above, one file per
                        record's own `run.id`

    python3 tests/test_ingest_terralith.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "ingest_terralith"
INGEST = ROOT / "scripts" / "ingest_terralith.py"


def diff(expected: dict, actual: dict, path: str = "") -> list[str]:
    """Every disagreement between `expected` and `actual`, so a failure names
    every field that moved rather than the first one found.
    """
    problems: list[str] = []
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in sorted(set(expected) | set(actual)):
            here = f"{path}.{key}" if path else key
            if key not in expected:
                problems.append(f"{here}: unexpected in actual (got {actual[key]!r})")
            elif key not in actual:
                problems.append(f"{here}: expected {expected[key]!r}, missing from actual")
            else:
                problems.extend(diff(expected[key], actual[key], here))
    elif expected != actual:
        problems.append(f"{path}: expected {expected!r}, got {actual!r}")
    return problems


def main() -> int:
    expected_dir = FIXTURES / "expected"
    expected_files = sorted(expected_dir.glob("*.json"))
    if not expected_files:
        print(f"no expected fixtures under {expected_dir} — nothing to test")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        result = subprocess.run(
            [
                sys.executable,
                str(INGEST),
                "--scale-records", str(FIXTURES / "gauntlet-scale.json"),
                "--gauntlet", str(FIXTURES / "gauntlet.json"),
                "--out", str(out),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("ingest_terralith.py exited non-zero against the choudoufu fixture:")
            print(result.stdout)
            print(result.stderr)
            return 1

        # Same output directory, a second invocation — the two ingest shapes
        # are mutually exclusive per call (see ingest_terralith.py's own
        # docstring) but their outputs are not, and the two fixture sets
        # write disjoint run ids, so nothing here overwrites the choudoufu
        # results just written above.
        chant_result = subprocess.run(
            [
                sys.executable,
                str(INGEST),
                "--chant-record", str(FIXTURES / "chant-scale-record-1.json"),
                "--chant-record", str(FIXTURES / "chant-scale-record-2.json"),
                "--out", str(out),
            ],
            capture_output=True,
            text=True,
        )
        if chant_result.returncode != 0:
            print("ingest_terralith.py exited non-zero against the chant fixtures:")
            print(chant_result.stdout)
            print(chant_result.stderr)
            return 1

        actual_files = sorted(out.glob("*.json"))
        actual_names = {p.name for p in actual_files}
        expected_names = {p.name for p in expected_files}

        failed = False

        for name in sorted(expected_names - actual_names):
            print(f"FAIL  {name}: expected but the ingest did not write it")
            failed = True
        for name in sorted(actual_names - expected_names):
            print(f"FAIL  {name}: the ingest wrote it but no expectation names it")
            failed = True

        for name in sorted(expected_names & actual_names):
            expected = json.loads((expected_dir / name).read_text())
            actual = json.loads((out / name).read_text())
            problems = diff(expected, actual)
            if problems:
                failed = True
                print(f"FAIL  {name}")
                for p in problems:
                    print(f"        {p}")
            else:
                print(f"ok    {name}")

    if failed:
        print("\ningest_terralith.py disagrees with tests/fixtures/ingest_terralith/expected/")
        return 1

    print(f"\n{len(expected_files)}/{len(expected_files)} fixture result(s) match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
