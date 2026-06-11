"""Test Loop RED-1, RED-2, RED-3 (SSOT: docs/PRD.md §7)."""

import pytest

from converter.commands import cross_check
from converter.skill import run_skill


def _assert_red1(equivalents: dict[str, float]) -> None:
    assert equivalents["feet"] == 8.2
    assert equivalents["yard"] == 2.7


def test_red1():
    # Arrange — meter 앵커 입력
    raw = "meter:2.5"

    # Act
    _, _, equivalents = run_skill(raw)

    # Assert — R-05 전 단위, R-06 소수 1자리
    _assert_red1(equivalents)


def test_red2():
    # Arrange — 서로 다른 입력 경로, 동일 물리량
    path_a = ("feet", 8.2)
    path_b = ("meter", 2.5)

    # Act
    result = cross_check(path_a, path_b)

    # Assert
    assert result is True


def test_red3_tampered_ratio_would_fail_red1(monkeypatch):
    # Arrange — 비율 tamper (R-04 회귀 가드)
    monkeypatch.setattr("converter.commands.M_TO_FT", 99.0)

    # Act
    _, _, equivalents = run_skill("meter:2.5")

    # Assert — RED-1 기대가 깨져야 함
    with pytest.raises(AssertionError):
        _assert_red1(equivalents)


def test_red3_tampered_rounding_would_fail_red1(monkeypatch):
    # Arrange — 반올림 tamper (R-06 회귀 가드)
    monkeypatch.setattr("converter.commands.DECIMAL_PLACES", 4)

    # Act
    _, _, equivalents = run_skill("meter:2.5")

    # Assert — RED-1 기대가 깨져야 함
    with pytest.raises(AssertionError):
        _assert_red1(equivalents)
