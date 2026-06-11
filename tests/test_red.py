"""Test Loop RED-1~3 + Golden (SSOT: docs/PRD.md §7).

| SC   | Test              | 검증 |
|------|-------------------|------|
| SC-1 | RED-1             | meter 앵커 → feet==8.2, yard==2.7 |
| SC-2 | RED-2             | cross_check True |
| SC-3 | RED-3 (×2 tamper) | 비율·반올림 tamper 시 RED-1 실패 |
"""

import pytest

from converter.commands import cross_check
from converter.skill import run_skill
from tests._approval import assert_matches_golden


def _format_red1_golden(equivalents: dict[str, float]) -> str:
    lines = [
        f"meter={equivalents['meter']}",
        f"feet={equivalents['feet']}",
        f"yard={equivalents['yard']}",
    ]
    return "\n".join(lines) + "\n"


def _assert_red1(equivalents: dict[str, float]) -> None:
    """SC-1 / RED-1 — R-06 엄격 ==."""
    assert equivalents["feet"] == 8.2
    assert equivalents["yard"] == 2.7


def test_red1(raw_red1):
    # Given — SC-1: meter 앵커 입력
    # When — PARSE_INPUT → TO_METER_ANCHOR → EMIT_ALL_EQUIVALENTS
    _, _, equivalents = run_skill(raw_red1)

    # Assert — R-05 전 단위, R-06 소수 1자리
    _assert_red1(equivalents)


def test_red1_golden(raw_red1):
    """§7.2 Golden — RED-1 CLI 출력이 red1.approved.txt와 일치."""
    _, _, equivalents = run_skill(raw_red1)
    assert_matches_golden(_format_red1_golden(equivalents), "red1")


def test_red2(cross_paths_red2):
    # Given — SC-2: 서로 다른 입력 경로, 동일 물리량
    path_a, path_b = cross_paths_red2

    # When
    result = cross_check(path_a, path_b)

    # Assert — 교차 맥락 일치
    assert result is True


def test_red3_tampered_ratio_would_fail_red1(monkeypatch, raw_red1):
    # Given — SC-3: R-04 비율 tamper
    monkeypatch.setattr("converter.commands.M_TO_FT", 99.0)

    # When
    _, _, equivalents = run_skill(raw_red1)

    # Assert — RED-1 기대가 깨져야 함
    with pytest.raises(AssertionError):
        _assert_red1(equivalents)


def test_red3_tampered_rounding_would_fail_red1(monkeypatch, raw_red1):
    # Given — SC-3: R-06 반올림 tamper
    monkeypatch.setattr("converter.commands.DECIMAL_PLACES", 4)

    # When
    _, _, equivalents = run_skill(raw_red1)

    # Assert — RED-1 기대가 깨져야 함
    with pytest.raises(AssertionError):
        _assert_red1(equivalents)
