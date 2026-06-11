# green-minimal — ARRR R단계 (Respond = GREEN)

**RED 1묶음당 최소 구현**으로 해당 Test ID를 **PASS**시킨다.  
1커밋 = 1 RED 묶음 원칙 *(git commit은 사용자 요청 시만)*.

**추가 입력 없이 즉시 실행.** 사용자가 `/green-minimal` 만 입력했다.  
대상 RED 묶음·Test ID는 **채팅 + `/red-test-plan` + `tdd-red` assert 테스트**에서 자동 추출한다. **추가 질문·확인 요청 금지.**

**SSOT:** [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md) §3·§4·§7  
**앞단:** [`.cursor/commands/tdd-red.md`](./tdd-red.md) *(assert RED)* · [`.cursor/commands/red-skeleton.md`](./red-skeleton.md)  
**다음:** REFACTOR *(별도 커맨드·명시 요청 전 금지)*

---

## 역할 (ARRR R = Respond)

| 단계 | 본 커맨드 | 이전 | 다음 |
|:---|:---|:---|:---|
| **A — RED ③④** | *(범위 밖)* | `/red-test-plan` · `/red-skeleton` | — |
| **A — RED assert** | *(선행)* | `tdd-red` | `/green-minimal` |
| **R — GREEN** | **1 RED 묶음** 최소 구현 + PASS | `tdd-red` | 다음 RED 묶음 또는 Done |
| **REFACTOR** | *(금지)* | — | 명시 요청 시 |

**수정 허용:** 이번 RED 묶음에 필요한 **구현** + 해당 **테스트** *(pytest.fail → assert 교체)*.  
**수정 금지:** 이번 RED 묶음 **외** Test ID 선행 해결 · REFACTOR · boundary E001~E005.

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 기본 | boundary 재사용 |
|:---|:---|:---|
| **Layer** | `entity` | `boundary` — CLI·stderr만; Entity는 위임 |
| **Track** | `Logic` | `UI` — E001~E005는 boundary Track 전용 |

이어서 **이번 GREEN 묶음** 한 줄: `RED-N — (Test ID·한 줄 요약)`.

---

## RED 묶음 SSOT *(UnitConverter Phase A)*

| RED 묶음 | Test ID | 최소 구현 범위 | 테스트 함수 |
|:---|:---|:---|:---|
| **묶음 1** | RED-1 | `constants.py` · `parse_input` · `to_meter_anchor` · `emit_all_equivalents` · `run_skill` | `test_red1` |
| **묶음 2** | RED-2 | `cross_check` *(묶음 1 의존)* | `test_red2` |
| **묶음 3** | RED-3 | *(구현 추가 없음 — 회귀)* · `tdd-red` assert·tamper | `test_red3_*` |

**한 번에 1묶음만.** 묶음 2는 묶음 1 PASS 후; 묶음 3는 묶음 1·2 PASS 후.

---

## 절차

```
① RED 재확인 → ② src/ 최소 구현 → ③ pytest.fail 제거·assert 교체 → ④ PASS 확인 → ⑤ 보고
```

### ① RED 재확인

- `/red-test-plan` Track B에서 **이번 묶음 Test ID** Given/When/Then·Invariant를 읽는다.
- `tdd-red` assert 테스트가 이미 있으면 그대로 사용; **스켈레톤만** 있으면 assert로 교체 *(Then `pytest.fail` 제거)*.
- **다른 묶음 Test ID**는 여전히 FAIL이어도 된다.

### ② src/ 최소 구현

| 프로젝트 | 구현 경로 *(src/ 대응)* |
|:---|:---|
| **UnitConverter** | `converter/constants.py` · `converter/commands.py` · `converter/skill.py` |
| **Magic Square** | `entity/` · `src/` *(Skill SSOT)* |

- **Just enough** — 이번 Then을 PASS시키는 최소 코드만.
- **매직 넘버·하드코딩 금지** — 비율·반올림·그리드 크기는 **`constants.py` SSOT**만.

```python
# converter/constants.py (UnitConverter 예)
M_TO_FT = 3.28084
M_TO_YD = 1.09361
DECIMAL_PLACES = 1
```

- **E001~E005** `raise` / 오류 `return` / stderr emit **금지** *(Phase B·boundary)*.
- **ECB:** entity·commands·skill은 **boundary·control import 금지** *(예: `UnitConverter.py`, `sys.stdout`)*.

### ③ pytest.fail 제거 · assert 교체

스켈레톤 Then을 `tdd-red` assert로 교체:

```python
# Before (RED ④)
pytest.fail("RED: RED-1 — feet==8.2, yard==2.7")

# After (GREEN)
_, _, equivalents = run_skill(raw)
assert equivalents["feet"] == 8.2
assert equivalents["yard"] == 2.7
```

- AAA 주석 Given / When / Then 유지.
- `pytest.approx`·범위 assert **금지** *(R-06)*.

### ④ PASS 확인

```bash
# 단일 테스트 — 이번 RED 묶음만
python -m pytest tests/test_red.py::test_red1 -v

# 파일 전체 — 회귀·다른 묶음 FAIL 허용 여부 확인
python -m pytest tests/test_red.py -v
```

| 결과 | 조치 |
|:---|:---|
| **이번 묶음 PASS** | 보고 후 다음 묶음 또는 Done |
| **이번 묶음 FAIL** | 구현·assert 수정 후 재실행 |
| **이전 묶음 FAIL** *(회귀)* | **즉시 수정** — GREEN 완료 전제 |

### ⑤ Git *(사용자 요청 시만)*

- **1커밋 = 1 RED 묶음** 메시지 예: `green: RED-1 — meter anchor emit feet/yard`
- 사용자가 commit을 요청하지 않으면 **commit 하지 않음**.

---

## ECB · E001~E005 *(Logic Track GREEN)*

| 계층 | GREEN 허용 | 금지 |
|:---|:---|:---|
| **Entity** | 순수 변환·파싱·dict 반환 | `UnitConverter` import, print, E001~E005 |
| **Controller** | `run_skill` 순서: PARSE → ANCHOR → EMIT | CLI I/O |
| **Boundary** | *(본 Track 범위 밖)* | entity에서 boundary 호출 |

| Code | GREEN entity에서 |
|:---|:---|
| E001~E005 | **raise / return / emit 금지** — Phase B boundary |

---

## 금지

| 금지 | 이유 |
|:---|:---|
| **이번 RED 묶음 외** Test ID 동시 PASS 시도 | 1묶음=1GREEN, 회귀 추적 |
| REFACTOR *(리네임·추상화·OCP 구조)* | 별도 Phase |
| assert 완화 (`==` → `approx`, truthy만) | R-06·RED SSOT |
| 매직 넘버·하드코딩 | `constants.py` SSOT |
| E001~E005 entity 구현 | boundary Phase B |
| entity → boundary/control import | ECB |
| cubit·JSON/CSV·설정 로드 | Phase A 범위 밖 |
| `@pytest.mark.skip`, `xfail` | GREEN 회피 |
| **사용자 미요청 git commit** | `.cursorrules` |

---

## 완료 보고

```markdown
Phase: green | Layer: entity | Track: Logic
RED 묶음: RED-N — (한 줄)

## PASS Test ID
| Test ID | pytest |
|:---|:---|
| RED-1 | tests/test_red.py::test_red1 PASSED |

## 변경 파일
| 파일 | 변경 요지 |
|:---|:---|
| converter/constants.py | M_TO_FT, M_TO_YD, DECIMAL_PLACES |
| converter/commands.py | parse_input, to_meter_anchor, emit_all_equivalents |
| converter/skill.py | run_skill |
| tests/test_red.py | pytest.fail → assert (RED-1) |

## pytest
- 단일: `python -m pytest tests/test_red.py::test_red1 -v` → 1 passed
- 전체: `python -m pytest tests/test_red.py -v` → N passed, M failed *(다른 묶음 FAIL OK)*

## 회귀
- *(없음)* 또는 *(수정함: …)*

## 다음
- GREEN 묶음 2: RED-2 — cross_check
```

**회귀 실패 시:** 보고 전 **반드시 수정·재실행** 후 PASS 확인.

마지막 줄 *(다음 묶음 있을 때)*:

```
/green-minimal 로 RED-(N+1) 묶음을 진행할 준비됐다
```

마지막 줄 *(Phase A Done)*:

```
Phase A GREEN Done — REFACTOR는 명시 요청 전 보류
```

---

## UnitConverter 예시 — 묶음 1 (RED-1)

### 최소 구현 체크

- [ ] `converter/constants.py` — R-04, R-06 상수
- [ ] `parse_input("meter:2.5")` → `("meter", 2.5)`
- [ ] `to_meter_anchor("meter", 2.5)` → `2.5`
- [ ] `emit_all_equivalents(2.5)` → `{meter, feet, yard}` *(R-05, R-06)*
- [ ] `run_skill` — Skill 순서 준수

### pytest

```bash
python -m pytest tests/test_red.py::test_red1 -v
python -m pytest tests/test_red.py -v
```

---

## 체크리스트 *(에이전트 자가 점검)*

- [ ] 응답 첫 줄 `Phase: green | Layer: … | Track: …` + 이번 RED 묶음
- [ ] **1 RED 묶음만** 구현·assert 교체
- [ ] `constants.py` SSOT — 매직 넘버 없음
- [ ] E001~E005 entity **미구현**
- [ ] entity **boundary/control import 없음**
- [ ] 이번 Test ID **PASS** 확인 *(단일 pytest)*
- [ ] 전체 pytest 실행 — **회귀 시 즉시 수정**
- [ ] git commit **사용자 요청 시만**
- [ ] 보고: PASS Test ID · 변경 파일 · pytest 결과
