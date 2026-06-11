# golden-master — GREEN PASS 후 Approval Test

**Golden Master(Approval Test)** 를 구축·검증한다.  
대상 Test ID가 **pytest PASS** 된 뒤, 출력 스냅샷을 `tests/golden/`에 고정하고 회귀 시 diff로 잡는다.

**추가 입력 없이 즉시 실행.** 사용자가 `/golden-master` 만 입력했다.  
대상 Test ID·golden ID는 **채팅 + GREEN PASS 결과 + `/red-test-plan`** 에서 자동 추출한다. **추가 질문·확인 요청 금지.**

**SSOT:** [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md)  
**선행:** [`.cursor/commands/green-minimal.md`](./green-minimal.md) *(대상 Test ID PASS)*  
**Skill 참조:** `magic-square-tdd` Skill이 있으면 **golden 포맷·1-index 규칙을 자동 따름**.

---

## 역할

| 단계 | 본 커맨드 | 선행 | 다음 |
|:---|:---|:---|:---|
| **GREEN PASS** | *(전제)* | `/green-minimal` · `tdd-red` | `/golden-master` |
| **Golden Master** | `_approval.py` · golden 파일 · matched 검증 | PASS 확인 | REFACTOR·boundary *(별도)* |

**수정 허용:** `tests/_approval.py` · `tests/golden/` · golden 연결 테스트 *( `tests/test_*` )*.  
**수정 금지:** golden 파일 **수동 편집으로 matched 우회** · `converter/`·`entity/` **동작 변경** *(golden 불일치 시 구현 수정)*.

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: green | Layer: entity | Track: Logic
```

이어서 **대상 Test ID / golden ID** 한 줄 *(예: `RED-1 → red1.approved.txt`)*.

---

## 전제

| 조건 | 확인 |
|:---|:---|
| 대상 Test ID **pytest PASS** | `python -m pytest tests/…::test_* -v` |
| GREEN 구현 완료 | `/green-minimal` 또는 Phase A Done |
| golden ID ↔ Test ID 1:1 | 아래 SSOT 표 |

**PASS 전이면** golden 생성·matched 검증 **중단** — GREEN 먼저.

---

## Golden ID SSOT

| 프로젝트 | Test ID | golden 파일 | 직렬화 포맷 |
|:---|:---|:---|:---|
| **UnitConverter Phase A** | RED-1 | `tests/golden/red1.approved.txt` | 등가값 dict 한 줄/키 *(아래 예)* |
| **UnitConverter Phase A** | RED-2 | `tests/golden/red2.approved.txt` | `cross_check=True` |
| **Magic Square** *(Skill)* | D-* | `tests/golden/{id}.approved.txt` | `int[6]` **1-index** 좌표 *(아래 §)* |
| **boundary** | E001~E005 | `tests/golden/e00N.approved.txt` | 에러 코드 **문자열 고정** *(§ 에러 포맷)* |

한 `/golden-master` 실행당 **1 Test ID / 1 golden 파일** 권장. 여러 ID는 순차 실행.

---

## 절차

```
① PASS 재확인 → ② _approval.py → ③ golden 연결 → ④ UPDATE_GOLDEN=1 생성 → ⑤ matched 검증 → ⑥ 보고
```

### ① PASS 재확인

```bash
python -m pytest tests/test_red.py::test_red1 -v
```

FAIL이면 golden 작업 **하지 않음**.

### ② `tests/_approval.py` — `assert_matches_golden`

없으면 **생성**. 있으면 재사용.

```python
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
```

### ③ `tests/golden/{id}.approved.txt` 연결

테스트 Act 결과를 **고정 포맷 문자열**로 직렬화한 뒤 `assert_matches_golden` 호출.

**UnitConverter RED-1 예:**

```python
from tests._approval import assert_matches_golden


def _format_red1_golden(equivalents: dict[str, float]) -> str:
    lines = [
        f"meter={equivalents['meter']}",
        f"feet={equivalents['feet']}",
        f"yard={equivalents['yard']}",
    ]
    return "\n".join(lines) + "\n"


def test_red1_golden():
    _, _, equivalents = run_skill("meter:2.5")
    assert_matches_golden(_format_red1_golden(equivalents), "red1")
```

**Magic Square — `int[6]` 1-index *(Skill SSOT)*:**

```
# 포맷: row-major 1-index 좌표 6개, 공백 구분, trailing newline
1 2 3 4 5 6
```

- 인덱스 **1-based** — `(0,0)` → `1`, `(0,1)` → `2`, … `(1,0)` → `5`.
- **6개 정수**, 공백 1칸, 마지막 `\n` 필수.
- golden ID 예: `d_loc_01` → `tests/golden/d_loc_01.approved.txt`

**에러 코드 문자열 포맷 *(boundary · 고정)*:**

```
E001:Invalid format. Use unit:value (ex: meter:2.5)
E002:Invalid number: abc
E003:Unknown unit: cubit
```

- `{CODE}:{message}` 한 줄, PRD §6.2 **문자열 그대로**.
- golden 수동 수정으로 메시지 맞추기 **금지** — 구현이 포맷에 맞아야 PASS.

### ④ 기준 파일 생성 — `UPDATE_GOLDEN=1`

```bash
# Windows PowerShell
$env:UPDATE_GOLDEN="1"; python -m pytest tests/test_red.py::test_red1_golden -v

# macOS / Linux / Git Bash
UPDATE_GOLDEN=1 python -m pytest tests/test_red.py::test_red1_golden -v
```

- `tests/golden/{id}.approved.txt` **자동 생성·덮어쓰기**.
- 생성 직후 파일 내용을 **눈으로 확인** *(우회 편집 아님 — Act 출력이 맞는지)*.

### ⑤ matched 확인 — `UPDATE_GOLDEN` 없이

```bash
python -m pytest tests/test_red.py::test_red1_golden -v
python -m pytest tests/test_red.py -v
```

| 결과 | 의미 |
|:---|:---|
| **PASSED** | golden **matched** |
| **AssertionError** *(Golden mismatch)* | diff 확인 → **구현** 또는 직렬화 버그 수정; golden 수동 패치 **금지** |

---

## Golden 포맷 규칙 *(공통)*

| 규칙 | 내용 |
|:---|:---|
| **인코딩** | UTF-8 |
| **줄 끝** | POSIX `\n` *(CRLF 혼입 주의)* |
| **직렬화** | 테스트 내 `_format_*_golden()` **단일 SSOT** — 필드 추가 시 함수·golden 동시 갱신 |
| **int[6] 1-index** | Magic Square Skill — 6 integer, 1-based row-major |
| **에러 코드** | `E00N:{message}` — PRD 고정 문자열 |
| **수동 편집** | golden 파일 직접 고쳐 matched 만들기 **금지** |

---

## 금지

| 금지 | 이유 |
|:---|:---|
| golden `.approved.txt` **수동 편집**으로 matched | Approval Test 무력화 |
| PASS 전 golden 생성 | 기준 오염 |
| `UPDATE_GOLDEN=1` 없이 golden 신규 파일만 작성 | Act 출력과 불일치 |
| assert 완화·golden 비교 생략 | 회귀 미탐 |
| `converter/`·`entity/` 무분별 변경 | golden 전체 diff |

---

## 완료 보고

```markdown
Phase: green | Layer: entity | Track: Logic
Golden ID: red1 — RED-1

## golden 경로
- `tests/golden/red1.approved.txt`

## matched
- `UPDATE_GOLDEN` 없이: **matched** ✓
- 명령: `python -m pytest tests/test_red.py::test_red1_golden -v` → 1 passed

## diff 요약
- *(matched — diff 없음)*
- 또는 *(mismatch 시)*:
  - `- feet=8.1` / `+ feet=8.2` *(구현 수정 후 재생성)*

## 변경 파일
- tests/_approval.py *(신규)*
- tests/golden/red1.approved.txt *(UPDATE_GOLDEN=1 생성)*
- tests/test_red.py *(test_red1_golden 추가)*

## pytest
- 생성: `UPDATE_GOLDEN=1 python -m pytest …::test_red1_golden -v`
- 검증: `python -m pytest …::test_red1_golden -v`
- 회귀: `python -m pytest tests/test_red.py -v`
```

**mismatch 시:** diff 요약 → **구현·포맷 함수** 수정 → `UPDATE_GOLDEN=1`로 **재생성** *(golden 손수 수정 금지)*.

마지막 줄:

```
Golden Master 구축 완료 — REFACTOR·boundary는 별도
```

---

## pytest 명령 예시

```bash
# 1) 대상 unit PASS (선행)
python -m pytest tests/test_red.py::test_red1 -v

# 2) golden 기준 생성
$env:UPDATE_GOLDEN="1"; python -m pytest tests/test_red.py::test_red1_golden -v

# 3) matched 검증
python -m pytest tests/test_red.py::test_red1_golden -v

# 4) 전체 회귀
python -m pytest tests/test_red.py -v
```

---

## 체크리스트 *(에이전트 자가 점검)*

- [ ] 응답 첫 줄 `Phase: green | Layer: … | Track: …`
- [ ] 대상 Test ID **PASS** 확인
- [ ] `tests/_approval.py` · `assert_matches_golden` 존재
- [ ] `tests/golden/{id}.approved.txt` 연결 테스트 작성
- [ ] `UPDATE_GOLDEN=1` 로 기준 생성
- [ ] `UPDATE_GOLDEN` 없이 **matched** PASS
- [ ] golden **수동 편집 우회 없음**
- [ ] int[6] 1-index · E00N 문자열 포맷 *(해당 Track)* 준수
- [ ] 보고: golden 경로 · matched · diff 요약
