
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python UnitConverter.py

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점

### SSOT

| 문서 | 용도 |
|:---|:---|
| [`docs/PRD.md`](docs/PRD.md) | 도메인 규칙 · FR |
| [`Report/01.UnitConverter_ProblemDefinition_Report.md`](Report/01.UnitConverter_ProblemDefinition_Report.md) | Mom Test · 문제 정의 |

### 문서·Export *(spec 범위)*

| NN | Report | Transcript | 주제 |
|:---:|:---|:---|:---|
| 01 | [Report/01…](Report/01.UnitConverter_ProblemDefinition_Report.md) | [Prompting/01…](Prompting/01.UnitConverter_STEP1_Mom_Test_Interview_prompt.md) | Mom Test |
| 03 | — | [Prompting/03…](Prompting/03.UnitConverter_Session3_Workbook_prompt.md) | 세션 3 워크북 |
| 04 | — | [Prompting/04…](Prompting/04.UnitConverter_ProblemDefinition_PRD_prompt.md) | PRD 작성 |

### Git 브랜치 (ARRR TDD 파이프라인)

```
spec  →  red  →  green
 문서만      RED      GREEN+Golden
```

| 브랜치 | ARRR 단계 | 포함 | pytest |
|:---|:---|:---|:---|
| **`spec`** *(현재)* | Ask — 문서 | PRD · Report/01 · Prompting/01·03·04 | — |
| **`red`** | RED | converter 스텁 · RED-1~3 · Report/05 | 4 failed |
| **`green`** | GREEN | converter 구현 · golden · Report/06 | 5 passed |

```bash
git fetch origin
git checkout spec   # 문서 단계
git checkout red       # RED 단계
git checkout green     # GREEN 단계
```
