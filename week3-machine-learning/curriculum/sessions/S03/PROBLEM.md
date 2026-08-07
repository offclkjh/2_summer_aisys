# S03 — 기대값·분산·공분산

> 상태: `ready`. 한 과제씩 진행하고, 실행 전 예측을 먼저 기록한다.

## 목표와 비목표

- 목표: 유한 이산분포의 기대값과 분산을 가중합으로 계산한다.
- 목표: 분포의 이론적 moment와 고정된 유한 표본의 통계량을 구분한다.
- 목표: 두 확률변수의 공분산을 계산하고 부호를 해석한다.
- 이번 세션에서 하지 않는 것: Monte Carlo 수렴 실험, 정규분포, 공분산 행렬, normalization layer.

## 시작 전 선수지식 확인

1. `sum_i p_i x_i`에서 `p_i`의 합은 얼마여야 하는가?
2. joint table에서 한 변수를 합으로 제거하면 무엇을 얻는가?
3. shape `(3,)`인 두 배열의 같은 index끼리 곱한 뒤 모두 더하려면 어떤 연산을 쓸 수 있는가?

막히면 [유한합](../../concepts/finite_sum.md)과 [S02의 정의](../S02/PROBLEM.md#사용할-정의),
[배열의 축](../S02/PROBLEM.md#배열의-축)을 복습한다.

## 교재 연결

- 판본: Kevin P. Murphy, *Machine Learning: A Probabilistic Perspective* (2012).
- 주제명: Chapter 2의 expectation, variance, covariance.
- 확인할 기호: `E[X]`, `Var(X)`, `Cov(X,Y)`.
- 필요한 정의와 수치는 아래에 모두 제공된다.

## 문제에서 주어진 정보

한 센서의 상태 `X`는 세 값 중 하나이며, 각 상태에서 보조 특성 `Y`도 함께
정해진다. 세 outcome의 index 순서는 모든 배열에서 같다.

```python
x_values = np.array([-1.0, 1.0, 3.0], dtype=np.float64)
y_values = np.array([2.0, 0.0, 4.0], dtype=np.float64)
probabilities = np.array([0.25, 0.50, 0.25], dtype=np.float64)
samples = np.array([-1.0, 1.0, 3.0, 3.0, 3.0], dtype=np.float64)
```

`probabilities[i]`는 `(X, Y) = (x_values[i], y_values[i])`일 확률이다. `samples`는
이 분포에서 이미 관측한 크기 5의 고정 표본이다. 새 난수를 만들지 않는다.

## 사용할 정의

유한 이산확률변수의 기대값과 분산은 다음과 같다.

```text
mu_X = E[X] = sum_i p_i x_i
Var(X) = sum_i p_i (x_i - mu_X)^2
```

크기 `n`인 고정 표본의 표본평균과 불편 표본분산은 다음과 같다.

```text
x_bar = (1/n) sum_j x_j
s^2 = (1/(n-1)) sum_j (x_j - x_bar)^2
```

여기서는 분포의 `Var(X)`와 표본의 `s^2`를 구분하기 위해 표본분산에
`n-1` 분모를 사용한다. 공분산은 두 변수의 중심에서의 편차를 곱한 값의
기대값이다.

```text
Cov(X,Y) = sum_i p_i (x_i - mu_X)(y_i - mu_Y)
```

## 과제

### T1. 실행 전 예측

코드나 테스트를 실행하기 전 `answers.md`에 답한다.

1. 분포의 기대값과 표본평균은 어떤 대상을 요약하는가?
2. 분산은 어떤 분포에서 0이 되는가?
3. 주어진 `(X,Y)` outcome을 보고 공분산의 부호를 예측하고 이유를 적는다.

### T2. 분포 moment 손계산

1. `probabilities`의 합을 확인한다.
2. `E[X]`를 가중합으로 계산한다.
3. 각 outcome의 편차와 편차제곱을 적고 `Var(X)`를 계산한다.

### T3. 표본 통계량과 NumPy 직접 구현

1. `samples`의 표본평균, 편차제곱, `n-1`로 나눈 표본분산을 손계산한다.
2. `theoretical_moments(values, probabilities)`를 완성한다. 두 입력은 같은 shape의
   1차원 `float64` 배열이고 확률의 합은 1이다. `(expectation, variance)`를
   Python `float` 두 개의 tuple로 반환한다.
3. `sample_moments(samples)`를 완성한다. 입력은 길이 2 이상의 1차원
   `float64` 배열이며 `(sample_mean, unbiased_sample_variance)`를 Python `float`로
   반환한다. 분산 계산은 위 정의식을 직접 구현하고 `np.var`를 쓰지 않는다.
4. 이론값과 표본 통계량이 다른 이유를 적는다.

### T4. 공분산 구현과 라이브러리 검산

1. `E[Y]`와 각 outcome의 `p_i (x_i-mu_X)(y_i-mu_Y)` 항을 손으로 구한다.
2. `theoretical_covariance(x_values, y_values, probabilities)`를 완성한다. 세 입력은
   같은 shape의 1차원 `float64` 배열이고 확률의 합은 1이다. Python `float`를 반환한다.
3. 직접 구현을 완성한 뒤 `np.average(values, weights=probabilities)`,
   `np.var(samples, ddof=1)`과 결과를 검산한다.

### T5. 실패 사례

T3–T4의 입력 계약을 서로 다른 방식으로 위반하는 두 입력을 직접 만든다.
실행 전에 결과나 예외를 예측하고, 실제 결과와 계약 검사가 필요한 이유를
`answers.md`에 기록한다. 이 세션의 필수 구현은 유효한 입력의 계산에 집중하며,
예외 검사 코드는 선택 확장으로 둔다.

### T6. 설명 확인

다음을 자기 말로 설명한다.

> 기대값과 분산은 분포의 무엇을 요약하며, 표본평균·표본분산과는 어떻게 다른가?
> 공분산의 부호는 두 변수의 관계를 어떻게 요약하는가?

## 검산

T1–T4를 작성하고 구현한 뒤 프로젝트 root에서 실행한다.

```bash
cd week3-machine-learning/curriculum/sessions/S03
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```

## 제출물

- `answers.md`: T1–T6의 예측, 계산, 비교, 설명
- 완성한 `starter.py`
- 통과한 `test_contract.py` 실행 결과

## 완료 기준

- 같은 수치로 분포 moment와 표본 통계량을 손계산하고 직접 구현한다.
- 분포 분산과 `n-1` 분모의 불편 표본분산을 구분한다.
- 공분산의 각 가중 항과 총합을 계산하고 결과의 부호를 설명한다.
- 다른 유효한 입력에서도 세 함수가 정의와 일치하는 결과를 반환한다.
- 제공된 계약 테스트를 통과한다.

## 선택 확장

유효성 검사를 추가한다. shape 불일치, 확률의 합, 표본 길이 등 계약을 나누어
적절한 `TypeError` 또는 `ValueError`를 발생시키고 자신의 테스트로 확인한다.
