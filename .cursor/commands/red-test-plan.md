# red-test-plan — ARRR A단계 (Ask = RED ③)

**C2C 설계표·테스트 플랜만 작성**한다. 코드·테스트 파일은 만들지 않는다.

**추가 입력 없이 즉시 실행.** 사용자가 `/red-test-plan` 만 입력했다.  
세션 주제·Test ID·FR 매핑은 **현재 채팅 + PRD**에서 자동 추출한다. **추가 질문·확인 요청 금지.**

**SSOT:** [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md) §5·§7  
**형식 참고:** [`.cursor/commands/tdd-red.md`](./tdd-red.md) *(다음 단계 RED 구현용)*

---

## 역할 (ARRR A = Ask)

| 단계 | 본 커맨드 | 다음 커맨드 |
|:---|:---|:---|
| **A — Ask (RED ③)** | C2C 표 + Track B 표 + 테스트 플랜 + ECB·Mock 점검 | `/red-skeleton` |
| R — RED 구현 | *(본 커맨드 범위 밖)* | `tdd-red` / `/red-skeleton` |
| R — REFACTOR / GREEN | *(금지)* | — |

본 커맨드는 **설계·플랜 문서만** 출력한다. `tests/`·`converter/`·`src/`·`UnitConverter.py`에 **파일을 생성·수정하지 않는다.**

---

## Phase 선언

응답 **첫 줄**에 반드시 쓴다. Track·Layer는 채팅·PRD에서 추론하고, UnitConverter Phase A 기본값은 아래와 같다.

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | UnitConverter Phase A 기본 | Track A (boundary) 재사용 |
|:---|:---|:---|
| **Layer** | `entity` — Command·Skill·도메인 규칙 | `boundary` — CLI 입출력·오류 emit만 바꿔 동일 절차 재사용 |
| **Track** | `Logic` — `run_skill`·Command API | `UI` — 프롬프트·stdout·stderr *(Phase B+)* |

> **Track A 재사용:** boundary 레이어 테스트(예: CLI 프롬프트, 오류 메시지 E001~E005)가 필요할 때 **Layer만 `boundary`로 바꾸면** C2C·Track B·플랜·ECB 점검 블록 구조를 그대로 쓴다. Test ID·대상 함수·금지 규칙만 boundary 계약에 맞게 갱신한다.

---

## 자동 추출 (사용자에게 묻지 말 것)

| 항목 | 추출 소스 |
|:---|:---|
| **세션 주제** | 채팅 맥락 (예: Phase A 세션 3 — meter 앵커 Skill RED) |
| **Test ID** | PRD §7 RED-1~3 *(채팅에 다른 ID가 있으면 병합)* |
| **FR·Rule** | PRD §3 R-01~R-06, §5 FR-IN-01·FR-CV-01~03 |
| **대상 Command** | PRD §4 — `PARSE_INPUT`, `TO_METER_ANCHOR`, `EMIT_ALL_EQUIVALENTS`, `CROSS_CHECK`, Skill |
| **구현 파일 경로** | `.cursorrules` — `converter/commands.py`, `skill.py`, `tests/test_red.py` |

Phase A 범위 밖(cubit, JSON/CSV, 설정 로드)은 플랜에 **넣지 않는다.**

---

## 출력 (반드시 4블록, 표 형식)

아래 4개 섹션을 **순서대로** 출력한다. UnitConverter 기본값 예시는 괄호 안에 적었다; 채팅·PRD와 다르면 자동 추출 값으로 **덮어쓴다.**

---

### 블록 1 — C2C (Rule1~3)

PRD FR 인용 → **To-Do 1개** → Test ID Given/When/Then. Rule은 C2C 계약 3줄(핵심 도메인 규칙 3개)로 압축한다.

| Rule | PRD FR 인용 | To-Do (1개) | Test ID · Given / When / Then |
|:---|:---|:---|:---|
| **Rule1** | FR-IN-01 (R-01), FR-CV-01 (R-03, R-04) | `meter:2.5` 입력을 파싱하고 meter 앵커 2.5를 확정한다 | **RED-1** · Given `meter:2.5` / When `run_skill` / Then `feet==8.2`, `yard==2.7` |
| **Rule2** | FR-CV-02 (R-05, R-06) | 앵커에서 3단위 등가값을 소수 1자리로 일괄 산출한다 | **RED-1** · *(Rule1과 동일 Act·Assert — emit·반올림 검증)* |
| **Rule3** | FR-CV-03 (R-03) | 서로 다른 입력 경로가 동일 물리량이면 `CROSS_CHECK`가 true다 | **RED-2** · Given `feet:8.2` vs `meter:2.5` / When `cross_check` / Then `True` |

RED-3(회귀)는 Rule1~2의 **Invariant 가드**이므로 블록 2 Track B 표에 둔다.

---

### 블록 2 — Track B 표

Logic Track: Command·Skill 단위 RED. boundary Track일 때는 CLI·stderr 대상으로 행을 교체한다.

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|:---|:---|:---|:---|:---|
| **RED-1** | `run_skill` → `emit_all_equivalents` | `meter:2.5` → feet 8.2, yard 2.7 | R-03 앵커 순서, R-04 `M_TO_FT`/`M_TO_YD`, R-06 1자리 | `AssertionError` 또는 스켈레톤 미구현으로 assert 실패 |
| **RED-2** | `cross_check` | `(feet,8.2)` vs `(meter,2.5)` → `True` | 두 경로 모두 `anchor_m` 경유 | `False` 또는 미구현 |
| **RED-3** | `run_skill` + `monkeypatch` | RED-1 fixture 후 `M_TO_FT`·`DECIMAL_PLACES` tamper | R-04·R-06 변경 시 RED-1 기대 깨짐 | tamper 없이 RED-1 통과 *(가드 누락)* |

한 Test ID당 **한 행동**만 검증. RED-3은 tamper 후 `_assert_red1`이 **AssertionError**를 내야 성공.

---

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|:---|:---|
| **파일 경로** | `tests/test_red.py` *(Phase A SSOT)* |
| **테스트 함수명** | `test_red1`, `test_red2`, `test_red3_tampered_ratio_would_fail_red1`, `test_red3_tampered_rounding_would_fail_red1` |
| **헬퍼** | `_assert_red1(equivalents)` — RED-1 assert 공유 *(RED-3 회귀용)* |
| **conftest 픽스처** | `monkeypatch` *(pytest 내장)* — RED-3 tamper 전용; 별도 `conftest.py` 불필요 *(필요 시만 `tests/conftest.py`에 RED-1 equivalents fixture)* |
| **import 계약** | `from converter.skill import run_skill` · `from converter.commands import cross_check` |
| **pytest 명령** | `pytest tests/test_red.py -v` |
| **RED 묶음 범위** | **RED-1~3** — PRD §7 전체; Phase A Done 전까지 한 파일에 유지 |
| **AAA** | Arrange → Act → Assert; assert는 `==` 엄격 비교 *(RED-1)* |

**기대 상태 (플랜 시점):** 구현 스켈레톤이면 **FAILED**가 정상. `/red-skeleton` 이후 테스트 코드 작성.

---

### 블록 4 — ECB·Mock 점검

| 점검 항목 | Logic Track (entity) | boundary Track *(Layer=boundary)* |
|:---|:---|:---|
| **Entity** | `parse_input`, `to_meter_anchor`, `emit_all_equivalents`, `cross_check` — **실구현 또는 스텁 호출, Domain Mock 금지** | CLI handler가 Entity를 **위임만** — Entity Mock 금지 |
| **Controller** | `run_skill` 오케스트레이션 순서: PARSE → ANCHOR → EMIT | `UnitConverter.py` `main()` — 입출력만 |
| **Boundary** | Logic Track RED에서 **CLI·stdout/stderr 검증 없음** | 프롬프트·출력 라인·오류 메시지 검증 |
| **Domain Mock** | **금지** — `M_TO_FT` 등은 tamper(`monkeypatch`)만 RED-3 회귀용 | Entity 대체 Mock **금지** |
| **E001~E005 emit** | Logic Track RED에서 **오류 emit 시나리오 포함 금지** *(Phase B FR-IN-04)* | boundary 전용 Test ID로 분리 |

**E001~E005** *(boundary 오류 계약, Logic RED 제외)*

| Code | 조건 | 메시지 *(PRD §6.2)* |
|:---|:---|:---|
| E001 | `:` 없음 | `Invalid format. Use unit:value (ex: meter:2.5)` |
| E002 | 숫자 아님 | `Invalid number: {value_str}` |
| E003 | unknown unit | `Unknown unit: {unit}` |
| E004~E005 | *(Phase B 예약)* | 입력 검증 확장 시 boundary Track에만 추가 |

Logic Track RED-1~3 플랜에 E001~E005 **Given/When/Then 행을 넣지 않는다.**

---

## 금지

| 금지 | 이유 |
|:---|:---|
| `src/`·`converter/`·`UnitConverter.py` **수정** | Ask 단계 — 설계만 |
| `tests/` **파일 생성·수정** | `/red-skeleton` · `tdd-red` 단계 |
| GREEN / REFACTOR 구현·제안 | RED ③은 플랜만 |
| `@pytest.mark.skip`, `xfail` | RED 회피 |
| assert 완화·삭제로 RED 우회 | R-06·회귀 가드 흐림 |
| Domain Mock으로 Entity 대체 | ECB 위반 |
| Logic Track에 E001~E005 시나리오 | boundary 관심사 |
| cubit·JSON/CSV·설정 로드 테스트 | Phase A 범위 밖 |

---

## 완료

4블록 출력 후 **마지막 줄**에 반드시 한 줄만 쓴다:

```
/red-skeleton 으로 넘길 준비됐다
```

---

## 체크리스트 *(에이전트 자가 점검)*

- [ ] 응답 첫 줄 `Phase: red | Layer: … | Track: …`
- [ ] 블록 1 C2C Rule1~3 표 *(FR → To-Do → G/W/T)*
- [ ] 블록 2 Track B 표 *(Invariant · Expected RED Failure)*
- [ ] 블록 3 테스트 플랜 *(경로·함수·conftest·pytest·RED 범위)*
- [ ] 블록 4 ECB·Mock · E001~E005 Logic 금지
- [ ] `tests/`·`src/`·`converter/` **미생성·미수정**
- [ ] 마지막 줄 `/red-skeleton 으로 넘길 준비됐다`
- [ ] Track A 안내: Layer=`boundary`로 재사용 가능 명시
