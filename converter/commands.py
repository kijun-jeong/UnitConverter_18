"""Command API — Phase A (SSOT: docs/PRD.md §4)."""

from converter.constants import DECIMAL_PLACES, M_TO_FT, M_TO_YD, UNIT_TO_METER


def _round_display(value: float) -> float:
    return round(value, DECIMAL_PLACES)


def parse_input(s: str):
    unit, value_str = s.strip().split(":", 1)
    return unit.strip(), float(value_str.strip())


def to_meter_anchor(unit: str, value: float):
    factor = UNIT_TO_METER.get(unit)
    if factor is None:
        return None
    return value * factor


def emit_all_equivalents(anchor_m: float):
    return {
        "meter": _round_display(anchor_m),
        "feet": _round_display(anchor_m * M_TO_FT),
        "yard": _round_display(anchor_m * M_TO_YD),
    }


def cross_check(path_a, path_b):
    """CROSS_CHECK — SC-2 / FR-CV-03: 교차 입력 경로 일치."""
    unit_a, value_a = path_a
    unit_b, value_b = path_b
    anchor_a = to_meter_anchor(unit_a, value_a)
    anchor_b = to_meter_anchor(unit_b, value_b)
    return _round_display(anchor_a) == _round_display(anchor_b)
