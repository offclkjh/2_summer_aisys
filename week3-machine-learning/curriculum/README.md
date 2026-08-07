# MLAPP practice curriculum v2

이 디렉터리는 MLAPP의 확률적 관점을 손계산, NumPy 직접 구현, 라이브러리 검산, 신호처리·DNN 연결로 이어가는 40세션 과정이다.

## v2에서 바뀐 점

기존 문서는 40개 제목을 모두 “세션”처럼 표시했지만 실제 문제·입력·계약이 존재한 것은 S01뿐이었다. S01도 서로 다른 세 사례를 한 표에 섞고 NumPy를 숨은 선수지식으로 요구했다.

v2는 다음을 분리한다.

- [curriculum.toml](curriculum.toml): 40개 주제, 선수 세션, 필요 개념의 유일한 기준
- [authoring.toml](authoring.toml): 세션별 중심 질문·교재 주제·중심 사례·핵심/제외 범위
- `concepts/`: 과정 밖 선수지식의 짧은 진단·복습 카드
- `sessions/SXX/`: 실제로 풀 수 있도록 검수된 세션 문제
- [문제 템플릿](templates/PROBLEM_TEMPLATE.md): 상세 문제의 필수 구조
- `tools/`: 선수지식 호출과 구조 검증

`status = "planned"`는 **문제가 아직 출제되지 않았다는 뜻**이다. 제목과 개요만 보고 풀기 시작하지 않는다. `status = "ready"`이고 `PROBLEM.md`가 있는 세션만 실제 학습에 사용한다.

## 문제 생성 원칙

40개 상세 문제를 한 번에 생성하지 않는다. Phase별로 문제를 만들고 실제 튜터 풀이를 거쳐 다음 Phase로 넘어간다. 각 문제는 반드시 다음을 만족해야 한다.

1. 중심 사례를 하나만 사용한다.
2. 답에 필요한 상황·수치·shape·dtype을 문제 안에 공개한다.
3. 필요한 선수개념과 복습 위치를 시작 부분에 명시한다.
4. 손계산과 직접 구현은 같은 수치를 사용한다.
5. 라이브러리와 테스트는 검산 수단이며 문제 명세를 대신하지 않는다.
6. 핵심 120분과 선택 확장을 구분한다.
7. 출력값·허용 오차·완료 기준을 명시한다.
8. 입력·반환 형식·허용 오차 등 필요한 계약은 공개하되, 학습자가 도출할
   구체적인 정답 출력과 완성 코드는 첫 시도 전에 공개하지 않는다.

## 튜터 진행 규칙

튜터는 빠른 정답 전달보다 학습자의 예측, 구현, 검산 순서를 보존한다.

1. 첫 시도 전에는 정답, 완성 코드, 정확한 출력값을 공개하지 않는다.
2. 먼저 학습자의 예측이나 현재 생각을 묻고 `answers.md` 또는 코드에 기록하게 한다.
3. 도움은 **개념 질문 → 작은 힌트 → 의사코드 → 부분 코드 → 정답과 해설** 순서로 제공한다. 학습자가 막힌 지점을 확인하지 않고 단계를 건너뛰지 않는다.
4. 테스트가 실패하면 정답 코드 대신 실패한 입력 계약과 확인할 표현부터 알려준다.
5. 학습자가 정답을 직접 요청해도 먼저 한 번의 시도나 자기 설명을 확인한다. 시도 후에는 요청한 수준의 해설을 제공한다.
6. 실행과 테스트는 예측을 기록한 뒤에 진행하고, 결과가 다르면 수정 전에 차이를 설명하게 한다.
7. 문제문에 정답 수준의 예시가 있더라도 첫 시도 전에는 인용하지 않고 문제 작성 결함으로 기록한다.

학습자가 이미 충분히 시도했거나 명시적으로 해설 단계로 넘어간 뒤에는 정답을
숨기지 않는다. 이 규칙은 도움을 거부하기 위한 것이 아니라 공개 시점을 조절하기
위한 것이다.

### 세션 학습 플로우

세션은 오답을 판정하고 끝내지 않고, 학습자가 정답을 납득하고 다시 사용할 수
있을 때까지 다음 순서로 진행한다.

1. 학습자가 먼저 예측하거나 구현한다.
2. 막힌 지점을 구체화하고 필요한 단계의 힌트를 받는다.
3. 정답뿐 아니라 처음 생각과 달랐던 이유를 설명한다.
4. 도움 없이 핵심을 다시 설명하거나 코드를 정리한다.
5. 다른 입력이나 작은 변형에도 같은 개념을 적용해 본다.
6. 새 API, 재사용할 구현 개선, MLAPP 코어만 Phase별 학습 노트에 남긴다.

완료 기준은 정답을 처음부터 혼자 맞히는 것이 아니다. 튜터의 도움을 사용할 수
있지만, 마지막에는 핵심을 자기 말과 코드로 재구성할 수 있어야 한다.

## 세션을 시작하거나 문제를 생성할 때

먼저 해당 세션의 문맥을 불러온다.

```bash
cd week3-machine-learning/curriculum
python3 tools/session_context.py S01
```

출력에는 다음이 포함된다.

- 직접 선수 세션
- 필요한 개념
- 각 개념을 처음 배운 세션 또는 외부 선수지식 카드
- 이번 세션에서 새로 배울 개념

아직 출제 중인 세션의 문맥은 문제 작성자만 명시적으로 불러온다.

```bash
python3 tools/session_context.py S10 --for-authoring
```

구조 전체는 다음 명령으로 검증한다.

```bash
python3 tools/validate_curriculum.py
```

## Phase와 상태

| Phase | 세션 | 범위 | 상세 문제 상태 |
|---|---|---|---|
| [A](phase_a_ch01_02/README.md) | S01–S04 | 확률 언어와 계산 객체 | S01–S03 ready, S04 planned |
| [B](phase_b_ch03_discrete/README.md) | S05–S07 | 이산분포와 생성분류 | planned |
| [C](phase_c_ch04_gaussian/README.md) | S08–S12 | Gaussian models | planned |
| [D](phase_d_ch05_bayesian/README.md) | S13–S18 | Bayesian inference와 decision | planned |
| [E](phase_e_ch06_evaluation/README.md) | S19–S23 | frequentist evaluation | planned |
| [F](phase_f_ch07_regression/README.md) | S24–S29 | linear regression | planned |
| [G](phase_g_ch08_logistic/README.md) | S30–S36 | logistic regression과 calibration | planned |
| [H](phase_h_ch11_mixture/README.md) | S37–S40 | mixture models와 EM | planned |

현재 학습 가능한 첫 문제: [S01 문제](sessions/S01/PROBLEM.md)

## 주요 재배선

- S07은 conjugate parameter Bayes를 미리 요구하지 않도록 `categorical 생성분류와 zero-count 문제`로 바꿨다.
- conjugate Dirichlet 해석은 S13으로 이동했다.
- S18은 MAP regularization을 분리하고 Bayesian decision과 비대칭 비용에 집중한다.
- gradient/autograd는 S26에서 처음 가르치며 이전 세션은 이를 요구하지 않는다.
- S33은 S06 categorical을, S34는 S23 validation을 명시적 선수로 둔다.
- S35는 확률 품질·calibration·cost threshold에 범위를 제한한다.
- S36은 binary 신호분류 하나만 통합한다.
- S37은 판본 선택 작업을 없애고 MLAPP 2012 Ch.11의 latent mixture factorization을 배운다.

세부 제목과 전체 의존성은 README 표가 아니라 [curriculum.toml](curriculum.toml)을 기준으로 한다.
