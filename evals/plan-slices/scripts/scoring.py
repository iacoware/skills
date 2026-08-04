#!/usr/bin/env python3
"""Pure scoring strategies for plan-slices grades."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


VERDICT_SCORES = {"pass": 4, "minor": 3, "material": 2, "severe": 1, "absent": 0}
SCORING_VERSION = 3
SCORING_STRATEGIES = frozenset({"axis_worst", "criterion_mean"})


def _round(value: float) -> float:
    return round(value + 1e-12, 2)


def score_components(
    axes: Sequence[Mapping[str, object]], strategy: str
) -> tuple[list[dict[str, object]], float]:
    if strategy not in SCORING_STRATEGIES:
        raise ValueError(f"unknown scoring strategy: {strategy}")
    components: list[dict[str, object]] = []
    raw_total = 0.0
    for axis in axes:
        axis_id = str(axis["id"])
        weight = int(axis["weight"])
        verdicts = {
            str(criterion["id"]): str(criterion["verdict"])
            for criterion in axis["criteria"]  # type: ignore[union-attr]
        }
        numeric = [VERDICT_SCORES[verdict] for verdict in verdicts.values()]
        axis_score = min(numeric) if strategy == "axis_worst" else sum(numeric) / len(numeric)
        weighted_score = axis_score / 4 * weight
        raw_total += weighted_score
        components.append(
            {
                "id": axis_id,
                "weight": weight,
                "criterion_verdicts": verdicts,
                "criterion_scores": {
                    criterion_id: VERDICT_SCORES[verdict]
                    for criterion_id, verdict in verdicts.items()
                },
                "axis_score": _round(axis_score),
                "weighted_score": _round(weighted_score),
            }
        )
    return components, _round(raw_total)


def apply_caps(raw_total: float, caps: Sequence[tuple[str, int]]) -> tuple[float, list[dict[str, object]]]:
    ordered = sorted(({"id": failure_id, "cap": cap} for failure_id, cap in caps), key=lambda item: (item["cap"], item["id"]))
    return min([raw_total, *(float(item["cap"]) for item in ordered)]), ordered


def score_strategies(
    axes: Sequence[Mapping[str, object]], caps: Sequence[tuple[str, int]]
) -> dict[str, dict[str, object]]:
    results: dict[str, dict[str, object]] = {}
    for strategy in sorted(SCORING_STRATEGIES):
        components, raw_total = score_components(axes, strategy)
        effective_total, applied_caps = apply_caps(raw_total, caps)
        results[strategy] = {
            "components": components,
            "raw_total": raw_total,
            "effective_total": effective_total,
            "applied_caps": applied_caps,
        }
    return results
