# refactor-smell — ARRR R단계 (Refine ⑦)

**코드 스멜 탐지만** 수행한다. **수정·commit 금지.**

**추가 입력 없이 즉시 실행.** 사용자가 `/refactor-smell` 만 입력했다.  
탐색 범위·스멜 후보는 **현재 코드베이스 + 채팅 + PRD Phase B 방향**에서 자동 추출한다. **추가 질문·확인 요청 금지.**

**SSOT:** [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md) §8  
**선행:** [`.cursor/commands/green-minimal.md`](./green-minimal.md) · [`.cursor/commands/golden-master.md`](./golden-master.md) *(전 테스트 PASS)*  
**다음:** [`.cursor/commands/refactor-safe.md`](./refactor-safe.md) *(P0 1개 선정 후)*

---

## 역할 (ARRR R = Refine ⑦)

| 단계 | 본 커맨드 | 다음 |
|:---|:---|:---|
| **Refine ⑦ — Smell** | 스멜 표 · Change Budget · `/refactor-safe` 후보 | `/refactor-safe` |
| **Refine — Safe Refactor** | *(범위 밖)* | `/refactor-safe` |
| **코드 수정·commit** | **금지** | — |

본 커맨드는 **분석·표 출력만**. `src/` · `converter/` · `tests/` · `UnitConverter.py` **미수정**. **git commit 금지.**

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

| 필드 | UnitConverter 매핑 |
|:---|:---|
| **Scope** | `converter/` · `tests/` · `UnitConverter.py` *(src/ 대응: `converter/`)* |
| **Track** | Logic — Command·Skill · UI — CLI boundary *(Phase B)* |

---

## 전제 — pytest 전부 PASS

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|:---|:---|
| **전부 PASS** | 스멜 탐지 진행 |
| **1개라도 FAIL** | **즉시 중단** — GREEN·golden 먼저; 스멜 표 **출력하지 않음** |

중단 메시지 예: `pytest FAIL — /refactor-smell 중단. GREEN·golden 수정 후 재실행.`

---

## 스멜 유형 *(탐지 대상)*

| 유형 | 신호 *(예)* |
|:---|:---|
| **Long Method** | 한 함수가 파싱+변환+출력·다중 책임 |
| **Duplicated Code** | 동일 round/anchor 로직 반복 |
| **Mysterious Name** | `path_a`, `_`, 축약만으로 의도 불명 |
| **Magic Number** | `constants.py` 밖 리터럴 *(8.2, 2.5 테스트 데이터 제외)* |
| **ECB 위반** | entity가 CLI·print import; boundary가 변환 로직 보유 |
| **Feature Envy** | 한 모듈이 다른 모듈 데이터·상수만 연속 사용 |

---

## 우선순위 (P0 / P1 / P2)

| 등급 | 기준 | `/refactor-safe` |
|:---|:---|:---|
| **P0** | 테스트·R-03~R-06·ECB·회귀 RED-3 위험 | **1개만** 선정해 다음 단계 |
| **P1** | SRP·OCP *(PRD §8 Phase B)* — 동작 동일 | 후순위 |
| **P2** | 네이밍·주석·미세 중복 | 선택 |

---

## Change Budget *(다음 `/refactor-safe` 제약)*

한 번의 safe refactor에서 **넘지 말 것**:

| 항목 | 상한 |
|:---|:---|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

본 커맨드에서는 Budget을 **초과하는 후보에 `[OVER]`** 표시.

---

## 절차

```
① pytest tests/ -v → ② src/·tests/·boundary 스캔 → ③ 스멜 표 → ④ /refactor-safe 후보 1~3 → ⑤ 보고
```

1. **pytest** — 전부 PASS 확인 *(FAIL이면 중단)*.
2. **스캔** — `converter/` · `tests/` · `UnitConverter.py` · PRD §8 SRP·OCP 방향.
3. **스멜 표** — 아래 출력 형식; P0/P1/P2 + 유형 + 위치 + 근거.
4. **후보** — P0 중 Change Budget 내 **1~3개**; 각 후보에 예상 파일·메서드 수.
5. **보고** — 표 + 후보 + `/refactor-safe` 안내.

---

## 출력 형식 *(반드시 2블록)*

### 블록 1 — 스멜 표

| P | 유형 | 위치 | 근거 | Budget |
|:---|:---|:---|:---|:---|
| P0 | Duplicated Code | `cross_check` · `emit_all_equivalents` — `round(..., DECIMAL_PLACES)` | R-06 반올림 규칙 분산; RED-3 tamper 지점 증가 | 1파일 1함수 ✓ |
| P0 | ECB 위반 *(예정)* | `UnitConverter.py` `main()` 스켈레톤 | boundary 미구현·entity 혼재 위험 *(Phase B)* | 2파일 ✓ |
| P1 | Feature Envy | `to_meter_anchor` — `M_TO_FT`/`M_TO_YD` 분기 | 단위 registry OCP *(PRD §8)* | 2파일 1클래스 ✓ |
| P1 | Duplicated Code | `test_red.py` — `run_skill("meter:2.5")` 반복 | Arrange 중복; golden·RED-1 | 1파일 ✓ |
| P2 | Mysterious Name | `run_skill` 반환 `(unit, value, equivalents)` | 호출부 `_, _` — Skill 계약 불명확 | 1파일 ✓ |

*(위는 UnitConverter 예시; 실제 출력은 **현재 코드** 기준으로 채운다.)*

### 블록 2 — `/refactor-safe` 후보 *(1~3개)*

| # | P | 스멜 | 제안 refactor *(한 줄)* | Budget |
|:---|:---|:---|:---|:---|
| 1 | P0 | Duplicated Code — `round` 분산 | `_round_display(value)` helper in `commands.py` | 1파일 · 1메서드 ✓ |
| 2 | P0 | Duplicated Code — 테스트 Arrange | `@pytest.fixture def meter_25()` in `conftest.py` | 2파일 · 0클래스 ✓ |
| 3 | P1 | Feature Envy — `to_meter_anchor` | unit→factor dict *(OCP 초석, Phase B)* | 2파일 · 0클래스 ✓ |

---

## 완료 보고

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest
- `python -m pytest tests/ -v` → N passed *(전제 OK)*

## 스멜 요약
- P0: k건 · P1: m건 · P2: n건

## /refactor-safe 후보
1. (P0) …
2. (P0) …
3. (P1) …

## 다음
- **P0 1개만** 골라 `/refactor-safe` 실행
- Change Budget: 파일≤3 · 클래스≤1 · 메서드≤3
```

마지막 줄:

```
/refactor-safe — P0 후보 #(N) 을 실행하세요
```

---

## 금지

| 금지 | 이유 |
|:---|:---|
| **코드 수정** | Refine ⑦ = 탐지만 |
| **git commit** | `/refactor-safe` 이후·사용자 요청 시 |
| pytest FAIL 상태에서 스멜 표 | 기준 불안정 |
| P0 여러 개 동시 `/refactor-safe` | Change Budget·회귀 추적 |
| Phase C *(설정·cubit·JSON/CSV)* 스멜 선행 refactor | Phase A 범위 |
| golden 수동 수정·assert 완화 제안 | Approval·RED SSOT |

---

## UnitConverter 스캔 체크리스트 *(에이전트)*

- [ ] `converter/commands.py` — SRP·round 중복·unit 분기
- [ ] `converter/skill.py` — Skill 순서·반환값 명확성
- [ ] `converter/constants.py` — 매직 넘버 잔존
- [ ] `tests/test_red.py` — Arrange 중복·golden 직렬화 위치
- [ ] `UnitConverter.py` — ECB boundary vs entity
- [ ] PRD §8 — OCP registry·파싱/변환/출력 분리 *(P1 후보)*

---

## 체크리스트 *(에이전트 자가 점검)*

- [ ] 응답 첫 줄 `Phase: refactor | Scope: src/ tests/ | Track: Logic+UI`
- [ ] `python -m pytest tests/ -v` **전부 PASS** *(FAIL 시 중단)*
- [ ] 스멜 표 — P0/P1/P2 · 7유형 커버
- [ ] Change Budget 표시 · `[OVER]` 표기
- [ ] `/refactor-safe` 후보 **1~3개**
- [ ] **코드 수정·commit 없음**
- [ ] 다음: **P0 1개만** `/refactor-safe` 안내
