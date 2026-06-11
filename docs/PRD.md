# UnitConverter_18 — Product Requirements Document (PRD)

**버전**: 0.1 (Draft)  
**작성일**: 2026-06-11  
**SSOT**: 본 문서 + `Report/01.UnitConverter_ProblemDefinition_Report.md`  
**실행 진입점**: `UnitConverter.py`

> Mom Test 근거는 **[시뮬레이션]** 이며, `Report/01`의 진짜 문제·증거를 따른다.

---

## 1. 개요

### 1.1 제품 한 줄

`unit:value` 한 줄 입력으로 **meter 앵커**를 확정하고, 등록된 길이 단위(meter, feet, yard)의 **등가값을 한 번에** 출력하는 CLI 단위 변환기.

### 1.2 Mom Test → PRD 연결

| Mom Test | PRD 대응 |
|:---|:---|
| 출처마다 다른 숫자 (4.1016 / 4.10 / 4.1) | R-03 meter 앵커, R-04 고정 비율, R-06 반올림 |
| 3회 반복 변환 + 엑셀 재확인 | `EMIT_ALL_EQUIVALENTS`, `CROSS_CHECK`, RED-2 |
| 7~8분 교차 검증 | RED-1~3 회귀, Skill 1회 절차 |

### 1.3 범위 단계

| 단계 | 포함 | 제외 |
|:---|:---|:---|
| **Phase A (세션 3)** | Rule R-01~R-06, Command 4개, Skill, RED-1~3 | 설정 파일, cubit, JSON/CSV, OCP 리팩터 |
| **Phase B** | OCP·SRP, 입력 검증 TC, 기본 요구 완성 | — |
| **Phase C** | 설정 외부화, 동적 단위, 출력 포맷 | — |

---

## 2. 사용자·목표

### 2.1 Primary Persona *(시뮬레이션)*

스타트업 1인 개발자. 동일 물리량을 펌웨어·슬랙·문서에 다른 단위로 쓰며, **숫자 불일치 불안**으로 검색·엑셀 교차 확인에 시간을 쓴다.

### 2.2 Product Goal

1. **단일 meter 앵커**로 모든 등가값을 계산한다.
2. **한 입력 → 전 단위 출력**으로 반복 변환을 없앤다.
3. **테스트**로 비율·순서·반올림 변경 시 실패하게 한다.

### 2.3 Non-Goals (Phase A)

- mm 및 IoT 파이프라인 통합
- 웹 UI / 구글 검색 연동
- cubit 동적 등록, JSON/CSV 출력
- “만들면 쓸 거냐” 가설 검증

---

## 3. 도메인 규칙 (Rule SSOT)

| ID | 규칙 | 검증 |
|:---|:---|:---|
| **R-01** | 입력: `unit:value`, 공백 trim 후 파싱 | RED + 형식 FR |
| **R-02** | 허용 단위: `meter`, `feet`, `yard` (소문자) | unknown unit FR |
| **R-03** | **meter = 앵커**; feet/yard는 `anchor_m`에서만 파생 | RED-1, RED-2 |
| **R-04** | `M_TO_FT = 3.28084`, `M_TO_YD = 1.09361` | RED-1, RED-3 |
| **R-05** | 유효 입력 시 **3단위 모두** 출력 | RED-1 |
| **R-06** | 출력 소수 **1자리** 반올림 *(README 예시 기준)* | RED-1 |

### 3.1 변환 공식

```
anchor_m = value                    if unit == meter
anchor_m = value / M_TO_FT          if unit == feet
anchor_m = value / M_TO_YD          if unit == yard

out_meter = anchor_m
out_feet  = anchor_m * M_TO_FT
out_yard  = anchor_m * M_TO_YD
```

---

## 4. Command API (논리 계약)

Phase A에서는 함수명·모듈 배치는 구현자 선택; **행위**는 아래와 일치해야 한다.

| Command | 입력 | 출력 | 오류 |
|:---|:---|:---|:---|
| `PARSE_INPUT(s)` | 문자열 | `(unit: str, value: float)` | 형식 오류, 비숫자 |
| `TO_METER_ANCHOR(unit, value)` | 단위, 값 | `anchor_m: float` | unknown unit |
| `EMIT_ALL_EQUIVALENTS(anchor_m)` | meter 앵커 | `{meter, feet, yard}` 표시용 튜플/ dict | — |
| `CROSS_CHECK(path_a, path_b)` | 두 `(unit, value)` | `bool` 일치 | 파싱/단위 오류 |

### 4.1 Skill (적용 순서)

```
PARSE_INPUT → TO_METER_ANCHOR → EMIT_ALL_EQUIVALENTS
[optional] CROSS_CHECK(alt_input, primary_input)
```

---

## 5. 기능 요구 (FR)

### 5.1 Phase A — Must (세션 3)

| FR ID | 요약 | Rule | Test |
|:---|:---|:---|:---|
| **FR-IN-01** | `unit:value` 파싱 | R-01 | RED-1 |
| **FR-IN-02** | 등록 단위 외 거부 | R-02 | *(Phase B)* |
| **FR-CV-01** | meter 앵커 변환 | R-03, R-04 | RED-1, RED-2 |
| **FR-CV-02** | 전 단위 일괄 출력 | R-05, R-06 | RED-1 |
| **FR-CV-03** | 교차 입력 경로 일치 | R-03 | RED-2 |

### 5.2 Phase B — Should (README 기본·품질)

| FR ID | 요약 |
|:---|:---|
| **FR-IN-03** | 음수 거부 |
| **FR-IN-04** | 잘못된 형식 메시지 |
| **FR-AR-01** | OCP: 단위 추가 시 기존 코드 최소 변경 |
| **FR-AR-02** | SRP: 파싱 / 변환 / 출력 분리 |
| **FR-QA-01** | 단위 변환 TC |
| **FR-QA-02** | 입력 검증 TC |

### 5.3 Phase C — Could (README 추가)

| FR ID | 요약 |
|:---|:---|
| **FR-CFG-01** | JSON/YAML에서 비율 로드 |
| **FR-REG-01** | `1 cubit = 0.4572 meter` 동적 등록 |
| **FR-OUT-01** | JSON / CSV / 표 출력 선택 |

---

## 6. 입·출력 명세

### 6.1 CLI (현재)

**프롬프트**

```
Insert value for converting (ex: meter:2.5):
```

**입력 예**

```
meter:2.5
```

**출력 예** *(R-06: 소수 1자리)*

```
2.5 meter = 2.5 meter
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

### 6.2 오류 메시지 *(Phase B, 현재 코드와 정렬)*

| 조건 | 메시지 |
|:---|:---|
| `:` 없음 | `Invalid format. Use unit:value (ex: meter:2.5)` |
| 숫자 아님 | `Invalid number: {value_str}` |
| unknown unit | `Unknown unit: {unit}` |

---

## 7. Test Loop (RED SSOT)

| Test ID | Given | When | Then |
|:---|:---|:---|:---|
| **RED-1** | `meter:2.5` | 변환 실행 | feet ≈ **8.2**, yard ≈ **2.7** (1자리) |
| **RED-2** | `feet:8.2` 와 `meter:2.5` | 각각 앵커·등가 계산 | `CROSS_CHECK` **true** |
| **RED-3** | RED-1 fixture | `M_TO_FT`·앵커 순서·R-06 반올림 규칙 변경 | RED-1 **fail** *(회귀)* |

**성공 기준 매핑**

- SC-1 ← RED-1 (단일 앵커·전 단위)
- SC-2 ← RED-2 (교차 경로)
- SC-3 ← RED-3 (규칙 변경 시 깨짐)

---

## 8. 아키텍처 방향 *(Phase B+)*

README 품질 요구와 정렬; Phase A에서는 **동작 계약**만 우선.

| 관심사 | 방향 |
|:---|:---|
| 변환 비율 | 상수 또는 설정 로더 *(Phase C)* |
| 단위 registry | OCP — 새 단위는 등록만 *(Phase B)* |
| 파싱 / 변환 / 출력 | SRP 클래스 분리 *(Phase B)* |

**현재 스켈레톤** (`UnitConverter.py`): `main()` 단일 함수, `elif` 단위 분기, meter 앵커 암묵적 사용.

---

## 9. 수용 기준 체크리스트 (Phase A)

- [ ] R-01~R-06 문서·코드·테스트 일치
- [ ] RED-1, RED-2 통과
- [ ] RED-3: 비율·앵커 순서·반올림(R-06) tamper 시 RED-1 실패 확인
- [ ] Skill 순서로 수동 1회 재현 가능
- [ ] Phase B/C FR은 본 PRD에만 존재, Phase A Done에 포함 안 함

---

## 10. 참조

| 문서 | 내용 |
|:---|:---|
| `Report/01.UnitConverter_ProblemDefinition_Report.md` | Mom Test, R-G-I-O, 표면 문제 |
| `README.md` | 실습 일정, 실행, 전체 요구 목록 |

---

*PRD v0.1 — Mom Test **[시뮬레이션]** 및 세션 3 워크북 초안 기반. 구현 상세·파일 트리는 후속 세션에서 갱신.*
