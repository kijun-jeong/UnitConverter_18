"""Skill — PARSE_INPUT → TO_METER_ANCHOR → EMIT_ALL_EQUIVALENTS (SSOT: docs/PRD.md §4.1)."""

from converter.commands import emit_all_equivalents, parse_input, to_meter_anchor


def run_skill(s: str):
    unit, value = parse_input(s)
    anchor_m = to_meter_anchor(unit, value)
    equivalents = emit_all_equivalents(anchor_m)
    return unit, value, equivalents
