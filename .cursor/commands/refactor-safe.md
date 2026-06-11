# refactor-safe — ARRR R단계 (Refine — Safe Refactor)

**/refactor-smell** 표에서 **선택한 스멜 1개만** Safe Refactor 실행한다.  
동작·계약·golden **불변** — 구조만 개선.

**추가 입력 없이 즉시 실행.** 사용자가 `/refactor-safe` 만 입력했다.  
대상 스멜은 **직전 `/refactor-smell` 후보 #N + 채팅**에서 자동 추출한다. **추가 질문·확인 요청 금지.**  
*(후보 번호 없으면 P0 **#1** — `round` 분산 — 기본 적용)*

**SSOT:** [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md) §3·§8  
**앞단:** [`.cursor/commands/refactor-smell.md`](./refactor-smell.md) *(스멜 1개 선정)*  
**golden:** [`.cursor/commands/golden-master.md`](./golden-master.md)

---

## 역할

| 단계 | 본 커맨드 | 선행 | 다음 |
|:---|:---|:---|:---|
| **Refine ⑦ — Smell** | *(완료)* | `/refactor-smell` | — |
| **Refine — Safe Refactor** | **스멜 1개** 구조 개선 | P0 후보 선정 | `/refactor-smell` *(잔여)* |
| **GREEN / 버그 수정** | **금지** | — | `/green-minimal` |

**한 실행 = 스멜 1개.** 여러 P0 동시 처리 **금지**.

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: refactor | Layer: entity | Track: Logic
```

이어서 **이번 스멜** 한 줄 *(예: `P0 #1 — Duplicated Code: _round_display 추출`)*.

---

## 전제

```bash
python -m pytest tests/ -v
```

| 조건 | FAIL 시 |
|:---|:---|
| **전 테스트 PASS** | **중단** — refactor 전 GREEN·golden 수정 |
| `/refactor-smell` 후보 **1개** | 번호 없으면 **#1** |
| Change Budget 내 | 초과 시 **[OVER] — `/refactor-smell` 재선정** |

---

## Safe Refactor 원칙

| 원칙 | 내용 |
|:---|:---|
| **입출력 불변** | 함수 시그니처·반환값·RED-1~3 assert 기대 **동일** |
| **예외 불변** | 새 `raise`·E001~E005 emit **금지** |
| **int[6] 1-index** | Magic Square golden 좌표 **1-based row-major 유지** |
| **E001~E005** | entity·refactor 범위 **emit/raise/return 금지** |
| **기능 추가 금지** | cubit·registry·CLI·입력 검증 → **별도 GREEN** |
| **버그 수정 금지** | 동작 버그는 GREEN; refactor는 **구조만** |
| **ECB** | entity ↔ boundary import 추가 **금지** |
| **RED-3** | `monkeypatch` 대상(`M_TO_FT`, `DECIMAL_PLACES`) **동작 유지** |

---

## Change Budget *(필수 준수)*

| 항목 | 상한 | 초과 시 |
|:---|:---|:---|
| **파일** | ≤ 3 | 롤백 · 후보 재선정 |
| **클래스** | ≤ 1 | *(Phase A 함수형 — 0 허용)* |
| **메서드** | ≤ 3 | helper 추출 포함 |

---

## 절차

```
① 스멜·Budget 확인 → ② 최소 diff refactor → ③ pytest → ④ golden matched → ⑤ 보고
```

### ① 대상 스멜 확인

직전 `/refactor-smell` 블록 2에서 **1개**만 실행.

| # | 스멜 *(UnitConverter SSOT)* | 변경 |
|:---|:---|:---|
| **1** *(기본)* | `round` 분산 | `commands.py` — `_round_display(value)` |
| **2** | 테스트 Arrange 중복 | `conftest.py` fixture + `test_red.py` |
| **3** | `to_meter_anchor` Feature Envy | `UNIT_TO_METER` dict *(P1)* |

### ② refactor 실행 *(예: #1)*

```python
# converter/commands.py — Before
round(anchor_m, DECIMAL_PLACES)

# After — 1 helper, 동작 동일
def _round_display(value: float) -> float:
    return round(value, DECIMAL_PLACES)
```

- **Just structure** — 로직·상수·반올림 규칙 변경 없음.
- golden 직렬화 함수(`_format_red1_golden`) **출력 문자열 불변**.

### ③ pytest

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|:---|:---|
| **전부 PASS** | ④ golden |
| **FAIL** | **롤백** — refactor 취소 후 원인 분석 |

### ④ golden matched — `UPDATE_GOLDEN` **없이**

```bash
python -m pytest tests/test_red.py::test_red1_golden -v
python -m pytest tests/ -v
```

| golden 결과 | 조치 |
|:---|:---|
| **matched ✓** | 보고 완료 |
| **mismatch — 비의도** | refactor **롤백** · pytest 재실행 |
| **mismatch — 의도적** | ISS 문서화 *(아래)* → `UPDATE_GOLDEN=1` 재생성 |

#### golden diff 처리

| 유형 | 조건 | 조치 |
|:---|:---|:---|
| **비의도** | refactor 목표 외 출력 변경 | **롤백** · 스멜·구현 재검토 |
| **의도적** | 직렬화·계약 변경이 refactor 목적 *(드묾)* | **ISS 문서** *(채팅·Report 한 줄)* → `$env:UPDATE_GOLDEN="1"; pytest …::test_*_golden` → matched 재확인 |

**금지:** golden `.approved.txt` **수동 편집**으로 matched 우회.

**ISS 문서 예:**

```markdown
ISS-refactor-001: _round_display 추출 — golden 출력 동일 확인 (변경 없음)
```

*(출력 불변이면 ISS·UPDATE_GOLDEN **불필요**.)*

### ⑤ Git *(사용자 요청 시만)*

- 메시지 예: `refactor: extract _round_display (P0 #1)`
- 사용자 미요청 시 **commit 하지 않음**.

---

## 금지

| 금지 | 이유 |
|:---|:---|
| 스멜 **2개 이상** 동시 | Budget·회귀 |
| 기능 추가·버그 수정 | GREEN 전용 |
| E001~E005 구현 | boundary Phase B |
| 입출력·예외·int[6]·E00N 포맷 변경 | Safe Refactor 계약 |
| assert·golden 완화 | RED·Approval SSOT |
| Budget 초과 | `/refactor-smell` 재선정 |
| golden 수동 패치 | Approval 무력화 |
| **사용자 미요청 commit** | `.cursorrules` |

---

## 완료 보고

```markdown
Phase: refactor | Layer: entity | Track: Logic
스멜: P0 #1 — Duplicated Code (_round_display)

## 변경 요약
| 파일 | 변경 |
|:---|:---|
| converter/commands.py | `_round_display` 추출; emit·cross_check에서 사용 |

## Budget
- 파일 1 · 클래스 0 · 메서드 1 ✓

## pytest
- `python -m pytest tests/ -v` → 5 passed

## golden matched
- `tests/golden/red1.approved.txt` — **matched** ✓ *(UPDATE_GOLDEN 없음)*
- `python -m pytest tests/test_red.py::test_red1_golden -v` → 1 passed

## golden diff
- *(없음 — 출력 불변)*

## 다음
- 잔여 스멜: `/refactor-smell` 재실행 또는 P0 #2
```

마지막 줄 *(잔여 P0 있을 때)*:

```
/refactor-smell 로 잔여 스멜 확인 후 /refactor-safe #(N)
```

마지막 줄 *(스멜 소진)*:

```
Refactor Done — boundary·Phase B는 별도 GREEN
```

---

## UnitConverter — #1 실행 체크리스트

- [ ] `_round_display` — `round(v, DECIMAL_PLACES)` 단일 SSOT
- [ ] `emit_all_equivalents` · `cross_check` — helper 사용
- [ ] RED-3 `monkeypatch DECIMAL_PLACES` — 여전히 `_round_display` 경유
- [ ] `tests/golden/red1.approved.txt` — diff 없음
- [ ] pytest **5 passed**

---

## pytest 명령 *(완료 후 필수)*

```bash
python -m pytest tests/ -v
python -m pytest tests/test_red.py::test_red1_golden -v
```

---

## 체크리스트 *(에이전트 자가 점검)*

- [ ] 응답 첫 줄 `Phase: refactor | Layer: entity | Track: Logic`
- [ ] `/refactor-smell` 후보 **1개만** 실행
- [ ] Change Budget 준수
- [ ] 입출력·예외·int[6]·E001~E005 **불변**
- [ ] 기능 추가·버그 수정 **없음**
- [ ] `python -m pytest tests/ -v` **전부 PASS**
- [ ] golden **matched** *(UPDATE_GOLDEN 없음)*
- [ ] golden diff — 비의도 시 **롤백** · 의도 시 **ISS + UPDATE_GOLDEN**
- [ ] 보고: 변경 요약 · pytest · golden matched
- [ ] git commit **사용자 요청 시만**
