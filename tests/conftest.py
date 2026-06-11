"""RED test fixtures — Given SSOT (SSOT: /refactor-safe P0 #1)."""

import pytest


@pytest.fixture
def raw_red1() -> str:
    return "meter:2.5"


@pytest.fixture
def cross_paths_red2():
    return ("feet", 8.2), ("meter", 2.5)
