"""Rule R-02, R-04, R-06 — Phase A constants (SSOT: docs/PRD.md §3)."""

M_TO_FT = 3.28084
M_TO_YD = 1.09361
DECIMAL_PLACES = 1

UNIT_TO_METER = {
    "meter": 1.0,
    "feet": 1.0 / M_TO_FT,
    "yard": 1.0 / M_TO_YD,
}
