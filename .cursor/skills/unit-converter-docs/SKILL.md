---
name: unit-converter-docs
description: >-
  UnitConverter_18 Report and Transcript Export workflow. Use for Report Export,
  Transcript, /export-session, /export, Phase repeat, ARRR one-cycle completion
  reports, or session N documentation. Loads checklist and templates for
  Report/NN.* and Prompting/NN.Export-Transcript.md.
disable-model-invocation: true
---

# UnitConverter Docs Skill

**SSOT:** `.cursorrules` · `docs/PRD.md`  
**형식 SSOT:** `Report/05.UnitConverter_TDD_RED_Report.md` · `Prompting/05.UnitConverter_TDD_RED_Export-Transcript.md`  
**연동 Command:** `.cursor/commands/export-session.md` · `export.md`

> **Export 요청 시 unit-converter-docs Skill 로드 후 [phase-checklist.md](phase-checklist.md) 수행.**

명시 호출 · `/export-session` · `/export` 시에만 본 Skill을 따른다.

---

## 파일

| 파일 | 용도 |
|:---|:---|
| [SKILL.md](SKILL.md) | 워크플로 Step A~F |
| [phase-checklist.md](phase-checklist.md) | Export 전 점검 |
| [report-template.md](report-template.md) | Report 본문 |
| [transcript-template.md](transcript-template.md) | Transcript 본문 |

---

## 파일명 규칙

| 종류 | 패턴 | 예 |
|:---|:---|:---|
| Report | `Report/NN.{Topic}_Report.md` | `Report/06.UnitConverter_GREEN_Report.md` |
| Transcript | `Prompting/NN.{Topic}_Export-Transcript.md` | `Prompting/06.UnitConverter_GREEN_Export-Transcript.md` |

- `NN` = **2자리** (`01` … `99`)
- `{Topic}` = PascalCase·언더스코어 짧은 주제

---

## 워크플로 Step A → F

```
A 입력 수집 → B NN 결정 → C Report → D Transcript → E README 표 → F 완료 보고
```

### Step A — 입력 수집

**채팅·터미널에서만.** 추측 금지.

| 항목 | 수집 |
|:---|:---|
| **git status** | `git status --short` |
| **pytest** | `python -m pytest tests/ -v` *(실행 후 결과만 기재)* |
| **Phase** | `red` · `green` · `refactor` · `repeat` |
| **Test ID** | RED-1~3 · `red1` golden · 해당 없으면 `-` |
| **Command** | 이번 세션 `/red-test-plan` … `/refactor-safe` · `tdd-red` |

상세: [phase-checklist.md](phase-checklist.md) §A

### Step B — NN = max + 1

```text
Report/NN.*  와  Prompting/NN.*  중 최대 NN → +1
```

| 예 | max | 다음 |
|:---|:---|:---|
| `05` 존재 | 05 | **06** |

**덮어쓰기 금지.**

### Step C — Report

1. [report-template.md](report-template.md) 복사
2. **STEP 블록 1개** — Phase별:

| Phase | STEP | 핵심 |
|:---|:---|:---|
| **red** | RED | C2C · Track B · pytest fail=RED |
| **green** | GREEN | RED 묶음 PASS · constants · golden |
| **refactor** | REFACTOR | 스멜 # · Budget · golden matched |
| **repeat** | repeat | ARRR 1사이클 Command 체인 표 |

3. §1 요약 · §2 산출물 · §3 다음 단계
4. pytest는 **Step A 실측**만

### Step D — Transcript

1. [transcript-template.md](transcript-template.md) 복사
2. `_Exported on {YYYY-MM-DD} from Cursor_`
3. `_Source: {uuid}`* — agent transcript UUID 또는 `session`
4. **User** / **Cursor** 턴 **전문** *(요약 금지)*
5. 생성·변경 파일 표 · Report 링크

### Step E — README 문서 표 갱신

`README.md`에 **문서·Export** 표가 없으면 추가, 있으면 NN 행 1줄 추가:

```markdown
### 문서·Export

| NN | Report | Transcript | 주제 |
|:---:|:---|:---|:---|
| 06 | [Report/06…](Report/06…) | [Prompting/06…](Prompting/06…) | … |
```

README 수정이 세션 범위 밖이면 **생략 가능** *(`.cursorrules` — 명시 요청 없이 docs/Report/Prompting만 Export 시 README는 Skill Step E)*.

### Step F — 완료 보고

```
번호 NN — Export 완료

| 파일 | 경로 |
|:---|:---|
| 세션 보고서 | Report/NN.{Topic}_Report.md |
| Transcript | Prompting/NN.{Topic}_Export-Transcript.md |

세션 주제: (한 줄)
```

---

## Phase: repeat *(ARRR 1사이클)*

**Phase: repeat** — Ask → Respond → Refine **한 사이클** 종료 보고.

| ARRR | TDD | Command | 산출 |
|:---|:---|:---|:---|
| Ask | RED ③④ | red-test-plan · red-skeleton · tdd-red | 플랜 · tests |
| Respond | GREEN | green-minimal · golden-master | converter · golden |
| Refine | REFACTOR | refactor-smell · refactor-safe | 구조 개선 |

Report **STEP — repeat** 표에 Command·pytest·PASS Test ID를 채운다.

---

## Phase 선언 *(Report 메타)*

| 세션 | Phase 필드 |
|:---|:---|
| RED 설계·스켈레톤 | `red` |
| GREEN · golden | `green` |
| refactor smell/safe | `refactor` |
| ARRR 1사이클 | `repeat` |

Layer/Track *(해당 시)*: `entity`/`boundary` · `Logic`/`UI`

---

## pytest 기록 규칙

| 허용 | 금지 |
|:---|:---|
| Step A에서 **실행한** 명령·stdout 요약 | 채팅에 없는 passed/failed **추측** |
| `python -m pytest tests/ -v` | UPDATE_GOLDEN=1 **임의 실행** |

golden 언급 시: matched / mismatch / 미구축 — **실측만**.

---

## ARRR ↔ Export 매핑

| 완료 이벤트 | Phase | Report STEP |
|:---|:---|:---|
| `/red-test-plan` + skeleton + tdd-red | red | RED |
| `/green-minimal` ×3 + golden | green | GREEN |
| `/refactor-safe` | refactor | REFACTOR |
| 위 전체 1회 | repeat | repeat |

---

## Command 체인 *(repeat 표용)*

```
/red-test-plan → /red-skeleton → tdd-red
       → /green-minimal → /golden-master
       → /refactor-smell → /refactor-safe
```

TDD Skill: [.cursor/skills/unit-converter-tdd/SKILL.md](../unit-converter-tdd/SKILL.md)

---

## 금지

| 금지 | 이유 |
|:---|:---|
| **git commit** 임의 | 사용자 요청 시만 |
| **UPDATE_GOLDEN=1** 임의 | `/golden-master` 절차 |
| pytest **추측** 기재 | Report SSOT |
| NN 파일 **덮어쓰기** | Export 이력 |
| Report **또는** Transcript **단독** | 2파일 필수 |
| Transcript **요약** | 전문 Export |
| golden **수동 편집** 언급·권장 | Approval SSOT |

---

## /export-session 연동

`.cursor/commands/export-session.md` 실행 시:

1. **unit-converter-docs** Skill 로드 *(본 문서)*
2. [phase-checklist.md](phase-checklist.md) A→F 순서
3. 템플릿: report · transcript
4. Step F 완료 보고

`/export`는 `/export-session` **별칭**.

---

## 빠른 체크리스트

- [ ] Step A: git · pytest **실행** · Phase · Test ID · Command
- [ ] Step B: NN = max+1 · 덮어쓰기 없음
- [ ] Step C: Report + Phase STEP 1개
- [ ] Step D: Transcript 전문 + `_Source`
- [ ] Step E: README 표 *(해당 시)*
- [ ] Step F: 경로 2개 보고
- [ ] commit · UPDATE_GOLDEN **없음**

---

## 예시 — Report 메타 *(GREEN)*

```markdown
| Phase | green |
| Test ID | RED-1 · red1 golden |
| Command | /green-minimal · /golden-master |
| pytest *(실측)* | `python -m pytest tests/ -v` → 5 passed, 0 failed |
```

---

## 예시 — Transcript 헤더

```markdown
# UnitConverter_18 — GREEN RED 묶음 · Golden Master Export

_Exported on 2026-06-11 from Cursor_
_Source: session_
```

*(UUID 알면 `_Source: a1b2c3d4-e5f6-…`)*

---

*Skill version — UnitConverter_18 Export · SSOT Report/05 · Prompting/05*
