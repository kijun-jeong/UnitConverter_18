"""Golden Master approval helpers (SSOT: /golden-master)."""

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def golden_path(golden_id: str) -> Path:
    return GOLDEN_DIR / f"{golden_id}.approved.txt"


def assert_matches_golden(actual: str, golden_id: str) -> None:
    path = golden_path(golden_id)
    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return
    expected = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"Golden mismatch: {path}\n--- expected ---\n{expected}--- actual ---\n{actual}"
        )
