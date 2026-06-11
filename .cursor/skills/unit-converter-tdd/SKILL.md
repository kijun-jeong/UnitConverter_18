---
name: unit-converter-tdd
description: >-
  UnitConverter_18 Dual-Track TDD workflow (ARRR, C2C, RED/GREEN/REFACTOR).
  Use when Phase is red, green, or refactor; when running Commands
  /red-test-plan, /red-skeleton, /green-minimal, /golden-master,
  /refactor-smell, /refactor-safe, or tdd-red; or when the user mentions
  TDD, RED, GREEN, REFACTOR, Dual-Track, C2C, or pytest.fail for
  UnitConverter meter-anchor Skill tests.
disable-model-invocation: true
---

# UnitConverter TDD Skill

**SSOT:** `.cursorrules` · `docs/PRD.md`  
**구현:** `converter/` *(src/ 대응)* · `tests/` · `UnitConverter.py`  
**Phase A:** R-01~R-06 · Command 4개 · Skill · RED-1~3 · cubit/JSON/CSV **금지**

명시 호출·Command 실행 시에만 본 Skill을 따른다.

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | Command | 산출 |
|:---|:---|:---|:---|
| **Ask** | RED ③ | `/red-test-plan` | C2C 표 · Track B · 테스트 플랜 · ECB 점검 *(코드 없음)* |
| **Ask** | RED ④ | `/red-skeleton` · `tdd-red` | 스켈레톤 `pytest.fail` → assert RED *(tests/만)* |
| **Respond** | GREEN | `/green-minimal` | 1 RED 묶음 최소 구현 · PASS |
| **Respond** | Approval | `/golden-master` | `tests/golden/{id}.approved.txt` |
| **Refine** | Smell ⑦ | `/refactor-smell` | 스멜 표 *(수정 금지)* |
| **Refine** | Safe | `/refactor-safe` | 스멜 1개 · Budget 내 refactor |

---

## 2. Phase 선언 — 응답 첫 줄

| 단계 | 형식 |
|:---|:---|
| RED 설계 | `Phase: red \| Layer: entity \| Track: Logic` |
| RED 스켈레톤 | 동일 |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| Golden | `Phase: green \| Layer: entity \| Track: Logic` |
| Refactor smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| Refactor safe | `Phase: refactor \| Layer: entity \| Track: Logic` |

**Track A 재사용:** boundary 테스트는 `Layer: boundary` · `Track: UI`만 변경.

---

## 3. C2C Rule 1~3 *(PRD §5·§7)*

| Rule | FR | To-Do | Test ID |
|:---|:---|:---|:---|
| **Rule1** | FR-IN-01, FR-CV-01 (R-01, R-03, R-04) | `meter:2.5` 파싱 → anchor 2.5 | **RED-1** |
| **Rule2** | FR-CV-02 (R-05, R-06) | 3단위 등가값 소수 1자리 | **RED-1** |
| **Rule3** | FR-CV-03 (R-03) | 교차 경로 `cross_check` True | **RED-2** |

**RED-3:** Rule1~2 회귀 — `M_TO_FT`·`DECIMAL_PLACES` tamper → RED-1 assert `AssertionError`.

---

## 4. RED 절대 금지

| 금지 | 이유 |
|:---|:---|
| `converter/`·`src/`·`UnitConverter.py` 수정 *(RED ③④·tdd-red)* | 테스트만 |
| `@pytest.mark.skip` · `xfail` | RED 회피 |
| assert 완화 (`pytest.approx`, truthy만) | R-06 SSOT |
| Logic Track **Domain Mock** | ECB; RED-3만 `monkeypatch` tamper |
| E001~E005 시나리오 (Logic RED) | boundary Phase B |
| cubit · JSON/CSV · 설정 로드 | Phase A 범위 밖 |
| golden 수동 편집 | Approval 무력화 |

**RED-1 Then:** `feet==8.2`, `yard==2.7` — `==` 엄격.

---

## 5. GREEN

### RED 묶음 SSOT

| 묶음 | Test ID | 구현 | 테스트 |
|:---|:---|:---|:---|
| 1 | RED-1 | `constants` · `parse_input` · `to_meter_anchor` · `emit_all_equivalents` · `run_skill` | `test_red1` |
| 2 | RED-2 | `cross_check` | `test_red2` |
| 3 | RED-3 | *(구현 추가 없음)* · tdd-red tamper | `test_red3_*` |

### 원칙

- **1커밋 = 1 RED 묶음** *(git commit은 사용자 요청 시만)*
- **매직 넘버 금지** — `converter/constants.py` SSOT:

```python
M_TO_FT = 3.28084
M_TO_YD = 1.09361
DECIMAL_PLACES = 1
```

- E001~E005 entity **raise/emit 금지**
- ECB: entity → boundary/control import **금지**
- Skill 순서: `PARSE_INPUT` → `TO_METER_ANCHOR` → `EMIT_ALL_EQUIVALENTS`

---

## 6. REFACTOR

### 전제

```bash
python -m pytest tests/ -v   # 전부 PASS
```

### Change Budget *(1회 `/refactor-safe`)*

| 항목 | ≤ |
|:---|:---|
| 파일 | 3 |
| 클래스 | 1 |
| 메서드 | 3 |

### Safe Refactor 원칙

- 입출력·예외·RED assert **불변**
- 기능 추가·버그 수정 **금지** *(별도 GREEN)*
- **golden 유지** — `UPDATE_GOLDEN` 없이 matched 확인
- golden diff **비의도** → 롤백 · **의도** → ISS + `UPDATE_GOLDEN=1`

### `/refactor-smell` 후보 *(UnitConverter)*

| # | 스멜 | refactor |
|:---|:---|:---|
| 1 | `round` 분산 | `_round_display()` in `commands.py` |
| 2 | Arrange 중복 | `conftest.py` fixture |
| 3 | `to_meter_anchor` 분기 | unit dict *(P1, Phase B)* |

**한 실행 = 스멜 1개.**

---

## 7. Dual-Track — Track A vs Track B

| | **Track B (Logic)** | **Track A (UI / boundary)** |
|:---|:---|:---|
| **Layer** | `entity` | `boundary` |
| **Track** | `Logic` | `UI` |
| **대상** | `run_skill` · Command API | CLI · stdout/stderr |
| **테스트** | RED-1~3 · assert·tamper | E001~E005 · 프롬프트·출력 라인 |
| **Mock** | Domain Mock **금지** | Entity Mock **금지** |
| **E001~E005** | Logic RED/GREEN **제외** | boundary 전용 |

**ECB:** Entity(변환) · Controller(`run_skill`) · Boundary(`UnitConverter.py` I/O).

**E001~E005 포맷 *(boundary)*:** `E00N:{message}` — PRD §6.2 문자열 고정.

---

## 8. Command 체인

```
/red-test-plan          → C2C·플랜 (코드 없음)
       ↓
/red-skeleton           → pytest.fail 스켈레톤 (tests/)
       ↓
tdd-red                 → assert RED (tests/)
       ↓
/green-minimal          → 1 RED 묶음씩 PASS (converter/)
       ↓
/golden-master          → tests/golden/{id}.approved.txt
       ↓
/refactor-smell         → 스멜 표 (수정 없음)
       ↓
/refactor-safe          → 스멜 1개 (Budget 내)
```

Command 본문: `.cursor/commands/{name}.md` — 충돌 시 Command + PRD + `.cursorrules`.

---

## 9. pytest 명령 패턴

```bash
# 전체 (선행·회귀)
python -m pytest tests/ -v

# 단일 RED / GREEN 묶음
python -m pytest tests/test_red.py::test_red1 -v
python -m pytest tests/test_red.py::test_red2 -v

# RED-3 회귀
python -m pytest tests/test_red.py::test_red3_tampered_ratio_would_fail_red1 -v

# Golden 생성 (1회)
$env:UPDATE_GOLDEN="1"; python -m pytest tests/test_red.py::test_red1_golden -v

# Golden matched (평상)
python -m pytest tests/test_red.py::test_red1_golden -v
```

**기대:** RED 스켈레톤 → FAILED(`pytest.fail`) · GREEN 후 → PASS · refactor 후 → PASS + golden matched.

---

## 10. 완료 보고 형식

### RED ③ `/red-test-plan`

4블록: C2C · Track B · 테스트 플랜 · ECB·Mock  
마지막: `/red-skeleton 으로 넘길 준비됐다`

### RED ④ `/red-skeleton`

| Test ID | FAIL 한 줄 |  
변경: `tests/`만 · `python -m pytest tests/test_red.py -v`

### GREEN `/green-minimal`

| PASS Test ID | pytest |  
변경 파일 · 단일+전체 pytest · 회귀 · 다음 묶음

### Golden `/golden-master`

golden 경로 · matched · diff 요약 · `Golden Master 구축 완료`

### Refactor smell

스멜 표 P0/P1/P2 · 후보 1~3 · `/refactor-safe — P0 후보 #(N)`

### Refactor safe

변경 요약 · Budget · pytest · golden matched · diff

---

## 파일 SSOT

| 파일 | 역할 |
|:---|:---|
| `converter/constants.py` | R-04, R-06 상수 |
| `converter/commands.py` | 4 Command + helpers |
| `converter/skill.py` | `run_skill` |
| `tests/test_red.py` | RED-1~3 + golden test |
| `tests/_approval.py` | `assert_matches_golden` |
| `tests/golden/red1.approved.txt` | RED-1 Approval |

---

## RED-3 monkeypatch *(회귀 SSOT)*

```python
monkeypatch.setattr("converter.commands.M_TO_FT", 99.0)
monkeypatch.setattr("converter.commands.DECIMAL_PLACES", 4)
# tamper 후 _assert_red1 → pytest.raises(AssertionError)
```

상수는 `converter.commands`에 import되어 있어야 tamper 유효.

---

## Git

- commit / push: **사용자 요청 시만**
- GREEN: `green: RED-N — …`
- Refactor: `refactor: … (P0 #N)`

---

## Phase A 금지 *(명시 요청 전)*

cubit · JSON/YAML 설정 · JSON/CSV 출력 · OCP 대규모 리팩터 · `docs/`·`Report/`·`Prompting/` 수정
