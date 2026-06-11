# Report Template — UnitConverter_18

**파일명:** `Report/NN.{Topic}_Report.md`  
**예:** `Report/06.UnitConverter_ARRR_Cycle_Report.md`

---

```markdown
# UnitConverter_18 — {세션 주제}

| 항목 | 내용 |
|:---|:---|
| 프로젝트 | `UnitConverter_18` |
| Phase | {Phase: red \| green \| refactor \| repeat} |
| Layer / Track | {entity \| boundary} / {Logic \| UI} |
| Test ID | {RED-1~3 · golden id · 없음} |
| Command | {/red-test-plan · /green-minimal · …} |
| 보고서 생성일 | {YYYY-MM-DD} |
| 목적 | {한 줄} |
| pytest *(실측)* | `{명령}` → {N passed, M failed} |
| 관련 Transcript | [`Prompting/NN.{Topic}_Export-Transcript.md`](../Prompting/NN.{Topic}_Export-Transcript.md) |

---

## STEP — {RED | GREEN | REFACTOR | repeat}

<!-- Phase별 블록 1개만 사용. 아래에서 해당 Phase 섹션 복사 -->

### RED *(Phase: red)*

| 항목 | 내용 |
|:---|:---|
| C2C | Rule1~3 · Track B Test ID |
| 산출 | 플랜 / 스켈레톤 / assert RED |
| pytest | failed = RED 성공 *(스켈레톤)* · passed = 구현 선행 주의 |
| 금지 준수 | src/·converter/ 미수정(Ask) · skip/xfail 없음 |

### GREEN *(Phase: green)*

| RED 묶음 | Test ID | PASS |
|:---|:---|:---|
| 1 | RED-1 | ✓/✗ |
| 2 | RED-2 | ✓/✗ |
| 3 | RED-3 | ✓/✗ |

| 항목 | 내용 |
|:---|:---|
| constants SSOT | `M_TO_FT` · `M_TO_YD` · `DECIMAL_PLACES` |
| golden | `{id}.approved.txt` matched *(해당 시)* |

### REFACTOR *(Phase: refactor)*

| 항목 | 내용 |
|:---|:---|
| 스멜 | P0 #N — {유형} |
| Budget | 파일≤3 · 클래스≤1 · 메서드≤3 |
| golden | matched / diff / ISS |

### repeat *(Phase: repeat — ARRR 1사이클)*

| ARRR | Command | 결과 |
|:---|:---|:---|
| Ask | red-test-plan → red-skeleton → tdd-red | |
| Respond | green-minimal → golden-master | |
| Refine | refactor-smell → refactor-safe | |

---

## 1. 요약

{3~5문장 — 세션 한 줄 + pytest 실측 + 판정}

---

## 2. 핵심 결정·산출물

### 2.1 Command / Skill

| 항목 | 내용 |
|:---|:---|
| | |

### 2.2 코드·테스트

| 파일 | 변경 |
|:---|:---|
| | |

### 2.3 pytest *(채팅·실행 로그 기준 — 추측 금지)*

```bash
python -m pytest tests/ -v
```

| 결과 | |
|:---|:---|
| passed | |
| failed | |

---

## 3. 다음 단계

| 순서 | 작업 |
|:---:|:---|
| 1 | |

---

*본 문서는 Report/NN.{Topic}_Report.md — {세션 주제} 세션 보고서입니다.*
```
