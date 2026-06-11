"""Command API — Phase A (SSOT: docs/PRD.md §4)."""


def parse_input(s: str):
    ...


def to_meter_anchor(unit: str, value: float):
    ...


def emit_all_equivalents(anchor_m: float):
    ...


def cross_check(path_a, path_b):
    ...
