# Recipe-app evaluation scenario

| Path | Role |
|---|---|
| `sources/*.md` | Controlling product and technical sources |
| `EVALUATION-BRIEF.md` | Authority classes, constraints, alternatives, and conflicts |
| `results/*.md` | Candidate plans |
| `results/calibration-legacy/raw/*.v1.{GRADE,SCORE}.json` | Immutable v1 artifacts |
| `results/calibration-v2/raw/*.v2.{GRADE,SCORE}.json` | Immutable v2 artifacts |
| `results/calibration-v3/raw/*.v3.*` | Active machine-readable evaluator artifacts |
| `results/calibration-v3/CALIBRATION*.v3.json` | Human-readable calibration reports |

From `evals/plan-slices`:

```bash
make validate PLAN=<candidate.md>
make grade PLANS='<candidate.md>' PROVIDER=both DRY_RUN=1
make compare BEFORE=<before.md> AFTER=<after.md> PROVIDER=both DRY_RUN=1
make calibrate-critical DRY_RUN=1
make calibrate-critical DRY_RUN=1 SHARD_COUNT=4 SHARD_INDEX=1
make calibrate-critical-report
make calibrate DRY_RUN=1
```

Use `CONFIRM_SEND=1` only after reviewing a dry run. Use `RESUME=1` to validate and reuse compatible
artifacts. A material grader disagreement exits `pending-review`; place the requested immutable
resolution file beside the blind request, then resume.

`calibrate-critical` plans the slice 7 absolute matrix only: 36 absolute provider calls and no paired or
adjudication units. It does not send without explicit confirmation. Shards are deterministic,
disjoint, and report-free; `calibrate-critical-report` joins only a complete resumable raw matrix
and never probes or invokes providers.
