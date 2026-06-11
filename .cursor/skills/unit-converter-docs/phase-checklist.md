# Phase Checklist — Export 전 점검

`/export-session` · `/export` 실행 전 **Step A** 수집·검증용.

---

## A. 입력 수집 *(실행·채팅에서만)*

| # | 항목 | 수집 방법 | 기록 위치 |
|:---:|:---|:---|:---|
| A1 | **git status** | `git status --short` | Report §2 · Transcript 메타 |
| A2 | **pytest** | `python -m pytest tests/ -v` | Report 메타 · §2.3 · Transcript 메타 |
| A3 | **Phase** | `red` · `green` · `refactor` · `repeat` | Report STEP 블록 |
| A4 | **Test ID** | RED-1~3 · golden id | Report 메타 |
| A5 | **Command** | `/red-test-plan` … `/refactor-safe` | Report · Transcript |

**금지:** 채팅·터미널에 **없는** pytest 결과 기재.

---

## B. 번호 (NN)

```
NN = max( Report/NN.* , Prompting/NN.* ) + 1  → 2자리 (06, 07, …)
```

| 현재 max *(예)* | 다음 |
|:---|:---|
| `05` | `06` |

- 기존 NN **덮어쓰기 금지**
- `REPORT.md` 단독명 **금지**

---

## C. Report — Phase STEP *(1개만)*

| Phase | STEP 섹션 | 필수 내용 |
|:---|:---|:---|
| **red** | RED | C2C · Track B · pytest fail/pass 해석 |
| **green** | GREEN | RED 묶음 · constants · golden matched |
| **refactor** | REFACTOR | 스멜 # · Budget · golden |
| **repeat** | repeat | ARRR 1사이클 표 · Command 체인 |

템플릿: [report-template.md](report-template.md)

---

## D. Transcript

- [ ] `_Exported on {날짜} from Cursor_`
- [ ] `_Source: {uuid}`*
- [ ] User / Cursor **전문** *(요약 금지)*
- [ ] 생성·변경 파일 표
- [ ] Report 링크

템플릿: [transcript-template.md](transcript-template.md)

---

## E. README 문서 표 갱신

`README.md` 하단 **문서·Export** 표 *(없으면 섹션 추가)*:

```markdown
### 문서·Export

| NN | Report | Transcript | 주제 |
|:---:|:---|:---|:---|
| 06 | [Report/06….md](Report/06….md) | [Prompting/06….md](Prompting/06….md) | {한 줄} |
```

- 새 NN 행 **1줄 추가** · 기존 행 수정 최소화
- 사용자가 README 갱신 금지 요청 시 **생략**

---

## F. 완료 보고 *(채팅)*

```
번호 NN — Export 완료

| 파일 | 경로 |
|:---|:---|
| 세션 보고서 | Report/NN.{Topic}_Report.md |
| Transcript | Prompting/NN.{Topic}_Export-Transcript.md |

세션 주제: (한 줄)
```

---

## 금지

| 금지 | 이유 |
|:---|:---|
| git commit 임의 | 사용자 요청 시만 |
| UPDATE_GOLDEN=1 임의 | golden-master 절차만 |
| pytest 추측 기재 | SSOT 오염 |
| Report만 / Transcript만 | Export는 **2파일 필수**

---

## /export-session 연동

> Export 요청 시 **unit-converter-docs** Skill 로드 후 본 checklist 수행.

Command: `.cursor/commands/export-session.md` · `.cursor/commands/export.md`
