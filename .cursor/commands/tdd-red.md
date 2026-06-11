# TDD RED — UnitConverter Skill

`run_skill` / Command API의 **RED 단계 전용** 커맨드.  
`tests/`만 수정한다. `converter/`·`src/`·`UnitConverter.py`는 건드리지 않는다.

**SSOT:** [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md) §7

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: RED | Scope: Phase A (세션 3)
```

이어서 이번 RED가 다루는 시나리오를 한 줄로 적는다 (예: `RED-1: meter:2.5 → feet 8.2, yard 2.7`).

| Phase A 범위 | 제외 |
|:---|:---|
| R-01~R-06, Command 4개, Skill, RED-1~3 | 설정 파일, cubit, JSON/CSV, OCP 리팩터 |

---

## 대상

| 항목 | 내용 |
|:---|:---|
| **Skill** | `run_skill(s)` — `PARSE_INPUT` → `TO_METER_ANCHOR` → `EMIT_ALL_EQUIVALENTS` |
| **Command** | `parse_input`, `to_meter_anchor`, `emit_all_equivalents`, `cross_check` |
| **파일** | `tests/test_red.py` *(필요 시 `tests/` 보조 모듈)* |
| **상수** | `M_TO_FT = 3.28084`, `M_TO_YD = 1.09361`, `DECIMAL_PLACES = 1` (`converter/constants.py`) |
| **앵커** | meter = 앵커; feet/yard는 `anchor_m`에서만 파생 (R-03) |

---

## AAA 절차

각 테스트는 **Arrange → Act → Assert** 순으로 작성한다.

1. **Arrange** — 입력 문자열(`unit:value`) 또는 `cross_check`용 `(unit, value)` 튜플을 준비한다. 시나리오 의도를 주석으로 남긴다.
2. **Act** — `run_skill(...)` 또는 `cross_check(...)` **한 번만** 호출한다.
3. **Assert** — 등가값·bool 결과를 **엄격히** 검증한다 (`==`, 정확한 소수 1자리). `pytest.approx`·범위 허용은 RED-1 기대값에 쓰지 않는다.

RED가 끝나면 `pytest`가 **실패**해야 한다. 통과하면 테스트가 약하거나 구현이 이미 들어간 것이다.

---

## RED 시나리오 (SSOT: PRD §7)

| ID | Given | When | Then |
|:---|:---|:---|:---|
| **RED-1** | `meter:2.5` | `run_skill` | `feet == 8.2`, `yard == 2.7` (R-06, 1자리) |
| **RED-2** | `feet:8.2` 와 `meter:2.5` | `cross_check` | `True` (교차 경로 일치) |
| **RED-3** | RED-1 fixture | `M_TO_FT`·`DECIMAL_PLACES` tamper (`monkeypatch`) | RED-1 assert **AssertionError** *(회귀)* |

한 번에 **하나의 행동**만 검증한다. RED-3은 tamper 후 RED-1 기대가 깨지는지 확인하는 **회귀 가드**다.

---

## pytest 예시

```python
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
```

실행:

```bash
pytest tests/test_red.py -v
```

기대 결과: **FAILED** (구현이 스켈레톤이거나 없으므로).  
구현 완료 후에는 RED-1·RED-2 **통과**, RED-3 tamper 시 **AssertionError** 확인.

---

## 금지

| 금지 | 이유 |
|:---|:---|
| `src/` 수정 | RED는 테스트만 *(본 프로젝트 구현은 `converter/`)* |
| `converter/` 수정 (`commands.py`, `constants.py`, `skill.py` 등) | RED는 테스트만 |
| `UnitConverter.py` 수정 | GREEN 단계에서 |
| assert 완화 (`== 8.2` → `pytest.approx`, `in`, `>=`, truthy만 검사) | R-06·요구사항 흐림 |
| `@pytest.mark.skip`, `xfail` | RED 회피 |
| 실패 테스트 삭제·이름 변경으로 우회 | 회귀 보호 무력화 |
| RED-3에서 tamper 없이 RED-1만 통과 확인 | 회귀 가드 누락 |
| cubit·JSON/CSV·설정 로드 테스트 추가 | Phase A 범위 밖 |

---

## 보고 형식

RED 작업 완료 후 아래 형식으로 보고한다.

```markdown
Phase: RED | Scope: Phase A (세션 3)

## 요약
- 시나리오: RED-N — (한 줄 설명)
- 수정 파일: tests/test_red.py

## 추가·수정한 테스트
| 테스트 함수 | Arrange 요지 | Assert 기대 |
|:---|:---|:---|
| test_red1 | meter:2.5 | feet==8.2, yard==2.7 |
| test_red2 | feet:8.2 vs meter:2.5 | cross_check is True |
| test_red3_... | M_TO_FT tamper | AssertionError on _assert_red1 |

## pytest 결과
- 명령: `pytest tests/test_red.py -v`
- 결과: N failed, M passed *(스켈레톤 단계면 failed가 RED 성공)*

## 다음 단계
- GREEN: `converter/commands.py` · `converter/skill.py` 최소 구현
```

---

## 체크리스트

- [ ] 응답 첫 줄 `Phase: RED | Scope: Phase A (세션 3)`
- [ ] `tests/`만 변경
- [ ] AAA 주석 또는 빈 줄로 구역 구분
- [ ] `pytest tests/test_red.py -v` 실행 결과 확인
- [ ] assert 완화·skip·xfail 없음
- [ ] `converter/`·`src/`·`UnitConverter.py` 미수정
