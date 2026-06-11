# Transcript Template — UnitConverter_18

**파일명:** `Prompting/NN.{Topic}_Export-Transcript.md`  
**예:** `Prompting/06.UnitConverter_ARRR_Cycle_Export-Transcript.md`

---

```markdown
# UnitConverter_18 — {세션 주제} Export

_Exported on {YYYY-MM-DD} from Cursor_  
_Source: {agent-transcript-uuid 또는 `session`}_

---

**User**

{User 메시지 전문}

---

**Cursor**

{Cursor 응답 전문}

---

*(User / Cursor 턴 반복 — 요약 금지)*

---

## 세션 메타

| 항목 | 값 |
|:---|:---|
| Phase | {red \| green \| refactor \| repeat} |
| Command | {목록} |
| Test ID | {RED-N · golden id} |
| pytest *(실측)* | `{명령}` → {결과} |

---

## 생성·변경 파일

| 파일 | 설명 |
|:---|:---|
| | |

---

## 관련 문서

| 문서 | 설명 |
|:---|:---|
| [Report/NN.{Topic}_Report.md](../Report/NN.{Topic}_Report.md) | 본 세션 보고서 |
| [docs/PRD.md](../docs/PRD.md) | PRD SSOT |
| [.cursorrules](../.cursorrules) | 프로젝트 규칙 |

---

*본 문서는 Prompting/NN.{Topic}_Export-Transcript.md — {세션 주제} 세션 대화 Export입니다.*
```

---

## _Source uuid

| 소스 | 값 |
|:---|:---|
| Agent transcript 있음 | 채팅 메타·transcript JSONL의 UUID *(예: `a1b2c3d4-…`)* |
| 없음 | `_Source: session`* |

Transcript 링크 *(선택)*: Cursor agent transcript `[제목](uuid)` 형식.
