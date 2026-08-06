# Plan-slices evaluator v3 workflow

> **Abandoned on 2026-08-06.** Unmaintained document, kept for history. The active tool is
> `CONSENSUS-WORKFLOW.md`.

## Active contracts

- `grader-rubric.v3.json`: verdict semantics, criteria, critical-failure triggers, and selected current scoring strategy.
- `recipe-app/EVALUATION-BRIEF.md`: authority classes, hard constraints, accepted alternatives, and known conflicts.
- `fixtures/manifest.v3.json`: labeled fixtures, repetitions, pairs, and human-review provenance.
- `scripts/grading_contract.py`: rubric, absolute-grade, and paired-grade validation.
- `scripts/scoring.py`: pure selected and shadow scoring formulas.
- `scripts/adjudication_contract.py`: absolute and paired disagreement resolution.

Historical v2 and v1 artifacts remain immutable under `recipe-app/results/calibration-v2/raw/`
and `recipe-app/results/calibration-legacy/raw/`. Active machine-readable artifacts and atomic
staging files live under `recipe-app/results/calibration-v3/raw/`; reports live one level above in
`recipe-app/results/calibration-v3/`.

## Offline checks

```bash
make test
make validate PLAN=<candidate.md>
```

The validator checks only published structure. It does not inspect product wording, scenario
expectations, source decisions, or semantic equivalence.

## Dry runs

```bash
make grade PLANS='<candidate.md>' PROVIDER=both DRY_RUN=1
make compare BEFORE=<before.md> AFTER=<after.md> PROVIDER=both DRY_RUN=1
make calibrate-critical DRY_RUN=1
make calibrate-critical DRY_RUN=1 SHARD_COUNT=4 SHARD_INDEX=1
make calibrate DRY_RUN=1
```

Dry runs show every file sent and artifact target without invoking providers. Review this output
before adding `CONFIRM_SEND=1`.

`calibrate-critical` is the slice 7 absolute-calibration workload: six `critical_subset` fixtures, three runs
per provider, 36 absolute calls, no paired calls, and no adjudication. Its diagnostic report is
`CALIBRATION-CRITICAL.v3.json`; the grade/score names remain reusable by full calibration.

For parallel collection, run one disjoint shard per worker using the same `SHARD_COUNT` and unique
one-based `SHARD_INDEX`. Shards never generate the shared report. Dry-run every shard first and
verify their union is 36 calls. After all 72 raw grade/score artifacts exist, one coordinator runs
`make calibrate-critical-report`; this performs no provider probe or send, requires every artifact
to pass resume validation, and then publishes the report atomically.

## Blind payloads and metadata

Provider prompts expose only `Source 1`, `Evaluation brief`, and `Candidate A`/`Candidate B`.
Generator identity, provider, local paths, and alias mappings exist only in artifact metadata.
Resume validates source, brief, rubric, prompt, candidate, manifest, label-set, model, effort,
configuration, CLI, and alias hashes.

## Adjudication

Two absolute grades are adjudicated before paired grading. `pass`↔`minor` differences resolve
automatically; any criterion involving `material`, `severe`, or `absent`, and every critical-failure
disagreement, creates a blind request.

The workflow exits `3` with `pending-review` and names the expected
`*.v3.ADJUDICATION.RESOLUTION.json`. The human resolution may contain only discordant criteria and
failures and must repeat input hashes. Resume then derives `RESOLVED.GRADE`, `RESOLVED.SCORE`, or
`RESOLVED.PAIRED` artifacts in code.

## Calibration status

`CALIBRATION.v3.json` is diagnostic while `thresholds_enforced` is `false`. Missing samples use a
zero denominator and `null` value. Provider-backed calibration and final scoring selection remain a
future checkpoint; until then the active formula remains `axis_worst`, with alternatives reported
only in shadow mode.
