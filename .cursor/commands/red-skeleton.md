# red-skeleton — ARRR A단계 (RED ④)

**/red-test-plan** 설계표 기준으로 **`pytest.fail` 스켈레톤만** 작성한다.  
실제 assert·회귀 tamper·GREEN 구현은 **다음 단계** (`tdd-red`)에서 한다.

**추가 입력 없이 즉시 실행.** 사용자가 `/red-skeleton` 만 입력했다.  
Test ID·함수명·픽스처는 **직전 `/red-test-plan` 출력 + 채팅 + PRD**에서 자동 추출한다. **추가 질문·확인 요청 금지.**

**SSOT:** [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md) §7  
**앞단 설계:** [`.cursor/commands/red-test-plan.md`](./red-test-plan.md)  
**다음 단계:** [`.cursor/commands/tdd-red.md`](./tdd-red.md) *(실 assert RED)*

**Skill 참조:** `magic-square-tdd` Skill이 있으면 **자동 따름** *(스켈레톤·픽스처·상수 import 규칙)*. 없으면 본 커맨드 본문을 SSOT로 한다.

---

## 역할 (ARRR A = RED ④)

| 단계 | 본 커맨드 | 이전 | 다음 |
|:---|:---|:---|:---|
| **A — RED ③** | *(범위 밖)* | — | `/red-test-plan` |
| **A — RED ④** | `pytest.fail` 스켈레톤 + conftest 픽스처 | `/red-test-plan` | `tdd-red` |
| **R — RED assert** | *(금지)* | — | `tdd-red` |
| **GREEN / REFACTOR** | *(금지)* | — | — |

**수정 허용:** `tests/` 만.  
**수정 금지:** `src/` · `converter/` · `UnitConverter.py` · `entity/` *(구현)*.

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 기본 | boundary 재사용 |
|:---|:---|:---|
| **Layer** | `entity` | `boundary` — Layer만 바꾸면 동일 스켈레톤 절차 |
| **Track** | `Logic` | `UI` — CLI·stderr Test ID |

---

## 자동 추출 (사용자에게 묻지 말 것)

| 항목 | 소스 |
|:---|:---|
| **Test ID** | `/red-test-plan` 블록 2 Track B 표 |
| **테스트 파일·함수명** | `/red-test-plan` 블록 3 |
| **Given/When/Then** | `/red-test-plan` C2C·Track B |
| **conftest 픽스처** | 블록 3 + 프로젝트 SSOT *(아래 표)* |

### 프로젝트별 conftest·상수 SSOT

| 프로젝트 | conftest 픽스처 | 상수 import *(픽스처·Given 데이터만)* |
|:---|:---|:---|
| **Magic Square** *(Skill 템플릿)* | `tests/conftest.py` → `grid_g1` *(0 두 개, row-major)* | `from entity.constants import MAGIC_SUM, GRID_SIZE, GRID_DIM` *(34 / 16 / 4)* |
| **UnitConverter Phase A** | `monkeypatch` *(pytest 내장, RED-3는 tdd-red)* · 필요 시 `raw_red1 = "meter:2.5"` | `from converter.constants import M_TO_FT, M_TO_YD, DECIMAL_PLACES` *(Given 주석·데이터만, tamper 금지)* |

---

## 스켈레톤 규칙

### AAA 주석 *(Given / When / Then)*

각 테스트 함수는 **3구역 주석**으로 나눈다:

```python
def test_...():
    # Given — …
    ...

    # When — …
    ...

    # Then — …
    pytest.fail("RED: {Test ID} — …")
```

| 구역 | 허용 | 금지 |
|:---|:---|:---|
| **Given** | 입력·픽스처·상수 참조 *(import한 상수는 Arrange 데이터만)* | Domain Mock, tamper |
| **When** | 대상 함수 **1회** 호출 *(스켈레톤에서 Act 생략 가능 — Then이 fail이면 RED 유지)* | 여러 Act, side-effect 검증 |
| **Then** | **`pytest.fail("RED: {Test ID} — …")` 한 줄만** | `assert`, `pytest.raises`, `pass`, 더미 `True` |

### Then 메시지 형식

```
pytest.fail("RED: {Test ID} — {Then 한 줄 요약}")
```

예: `pytest.fail("RED: RED-1 — feet==8.2, yard==2.7")`  
예: `pytest.fail("RED: D-LOC-01 — blank coords row-major at (0,0) and (3,1)")`

### 금지

| 금지 | 이유 |
|:---|:---|
| `assert` 본문 | RED ④는 fail 스켈레톤; assert는 `tdd-red` |
| `@pytest.mark.skip`, `xfail` | RED 회피 |
| 통과 더미 (`pass`, `assert True`) | RED 무효 |
| `src/` · `converter/` · `entity/` **구현** 수정 | 스켈레톤은 `tests/`만 |
| GREEN / REFACTOR 코드 | 다음 Phase |
| `monkeypatch` tamper *(UnitConverter RED-3)* | `tdd-red` 단계 |

---

## 절차

1. 직전 `/red-test-plan` *(또는 채팅)* 에서 Test ID·함수명·경로를 읽는다.
2. `magic-square-tdd` Skill이 있으면 **Skill 규칙을 우선** 적용한다.
3. `tests/conftest.py` — 플랜에 명시된 픽스처만 추가·갱신 *(없으면 생성)*.
4. 테스트 파일 — Track B **모든 Test ID**에 대해 `pytest.fail` 스켈레톤 함수 작성.
5. **`pytest {플랜의 경로} -v`** 실행.
6. 아래 **완료 보고** 형식으로 결과 출력.

---

## 템플릿 예시 — Magic Square *(Skill 기본)*

### `tests/conftest.py`

```python
import pytest


@pytest.fixture
def grid_g1():
    """Given grid: 0 두 개, row-major (4×4)."""
    return [
        [0, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
```

### `tests/test_d_loc.py` *(발췌)*

```python
"""RED ④ skeleton — D-LOC Track (SSOT: /red-test-plan)."""

import pytest

from entity.constants import GRID_DIM, GRID_SIZE, MAGIC_SUM


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given — 4×4 grid, blank(0) 두 칸, row-major; MAGIC_SUM=34, GRID_SIZE=16, GRID_DIM=4
    grid = grid_g1
    _ = MAGIC_SUM, GRID_SIZE, GRID_DIM

    # When — locate_blank_coords(grid)
    # coords = locate_blank_coords(grid)

    # Then
    pytest.fail("RED: D-LOC-01 — blank coords row-major at indices for two zeros")


def test_d_loc_02_magic_sum_invariant(grid_g1):
    # Given — MAGIC_SUM=34, GRID_DIM=4
    _ = MAGIC_SUM, GRID_DIM, grid_g1

    # When — validate_row_sum(grid, row=0)

    # Then
    pytest.fail("RED: D-LOC-02 — row 0 sum equals MAGIC_SUM 34")
```

---

## 템플릿 예시 — UnitConverter Phase A

### `tests/test_red.py` *(RED ④ 스켈레톤 — tdd-red 전)*

```python
"""RED ④ skeleton — RED-1~3 (SSOT: docs/PRD.md §7, /red-test-plan)."""

import pytest

from converter.constants import DECIMAL_PLACES, M_TO_FT, M_TO_YD


def test_red1():
    # Given — meter:2.5, R-04 ratios available for reference
    raw = "meter:2.5"
    _ = M_TO_FT, M_TO_YD, DECIMAL_PLACES

    # When — run_skill(raw)

    # Then
    pytest.fail("RED: RED-1 — feet==8.2, yard==2.7")


def test_red2():
    # Given — cross paths, same physical quantity
    path_a = ("feet", 8.2)
    path_b = ("meter", 2.5)

    # When — cross_check(path_a, path_b)

    # Then
    pytest.fail("RED: RED-2 — cross_check is True")


def test_red3_tampered_ratio_would_fail_red1():
    # Given — RED-1 fixture; tamper deferred to tdd-red

    # When — run_skill after M_TO_FT tamper

    # Then
    pytest.fail("RED: RED-3 — tampered M_TO_FT breaks RED-1 assert")


def test_red3_tampered_rounding_would_fail_red1():
    # Given — RED-1 fixture; tamper deferred to tdd-red

    # When — run_skill after DECIMAL_PLACES tamper

    # Then
    pytest.fail("RED: RED-3 — tampered DECIMAL_PLACES breaks RED-1 assert")
```

실행:

```bash
pytest tests/test_red.py -v
```

기대: **전 테스트 FAILED** *(pytest.fail)* — 스켈레톤 RED 성공.

---

## 완료 보고

스켈레톤 작성·pytest 실행 후 아래 형식으로 보고한다.

```markdown
Phase: red | Layer: entity | Track: Logic

## 변경 파일 *(tests/ 만)*
- tests/conftest.py *(픽스처 추가 시)*
- tests/test_….py

## pytest 결과
| Test ID | FAIL 한 줄 |
|:---|:---|
| RED-1 | RED: RED-1 — feet==8.2, yard==2.7 |
| RED-2 | RED: RED-2 — cross_check is True |
| … | … |

- 명령: `pytest tests/test_red.py -v`
- 결과: N failed, 0 passed *(전부 pytest.fail = RED ④ 성공)*

## 다음 단계
- `tdd-red`: Then을 실 assert·monkeypatch 회귀로 교체
```

마지막 줄:

```
tdd-red 로 assert RED를 작성할 준비됐다
```

---

## 체크리스트 *(에이전트 자가 점검)*

- [ ] 응답 첫 줄 `Phase: red | Layer: … | Track: …`
- [ ] `/red-test-plan` Track B **전 Test ID** 스켈레톤 함수 존재
- [ ] AAA 주석 Given / When / Then
- [ ] Then = `pytest.fail("RED: …")` **한 줄만**
- [ ] assert 본문·skip·xfail·통과 더미 **없음**
- [ ] `src/` · `converter/` · `entity/` 구현 **미수정**
- [ ] conftest 픽스처 *(grid_g1 또는 플랜 명시)* 반영
- [ ] 상수는 import만 *(픽스처·Given 데이터)* — tamper 없음
- [ ] `pytest … -v` 실행 + Test ID · FAIL 표 보고
- [ ] `magic-square-tdd` Skill 있으면 Skill 규칙 적용 명시
