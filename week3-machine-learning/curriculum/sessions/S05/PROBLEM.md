# S05 — Bernoulli·Binomial

> 상태: `ready`. 한 과제씩 진행하고, 실행 전 예측을 먼저 기록한다.

## 목표와 비목표

- 목표: binary 관측 하나의 Bernoulli PMF와 여러 독립 관측의
  likelihood를 계산한다.
- 목표: 순서가 있는 관측열의 likelihood와 성공 횟수의 Binomial
  PMF를 조합계수로 연결한다.
- 목표: likelihood와 log-likelihood를 `theta`의 함수로 읽고 MLE를 구한다.
- 목표: 같은 정의식을 NumPy로 직접 구현하고 검산한다.
- 이번 세션에서 하지 않는 것: Beta prior와 posterior, MAP, optimizer,
  MLE의 미분 유도, 대규모 parameter grid sweep.

## 시작 전 선수지식 확인

1. 독립인 사건 여러 개가 모두 발생할 확률은 각 확률을 어떤 연산으로
   결합하는가?
2. `X` Bernoulli 변수에서 `p(X=1)=theta`, `p(X=0)=1-theta`일 때
   `E[X] = sum_x x p(x)`를 계산하면 어떤 값인가?
3. Bayes rule의 `p(D | theta)`에서 데이터 `D`를 고정하고 `theta`를
   바꾸어 읽으면 무엇을 비교하는가?

막히면 [S02의 곱셈법칙과 Bayes rule](../S02/PROBLEM.md#사용할-정의),
[S03의 기대값 정의](../S03/PROBLEM.md#사용할-정의),
[로그 복습 카드](../../concepts/logarithm.md)를 먼저 복습한다.

## 교재 연결

- 판본: Kevin P. Murphy, *Machine Learning: A Probabilistic Perspective* (2012).
- 주제명: Chapter 3의 Bernoulli distribution, Binomial distribution, MLE.
- 확인할 개념: binary outcome PMF, iid sample likelihood, log-likelihood,
  성공 횟수 분포, maximum likelihood estimate.
- 문제에 필요한 정의와 수치는 아래에 모두 제공된다.

## 문제에서 주어진 정보

같은 조건에서 전송한 패킷 다섯 개의 성공 여부를 순서대로 관측했다.
성공은 `1`, 실패는 `0`이다.

```python
data = np.array([1, 0, 1, 1, 0], dtype=np.int64)
theta = 0.4
```

`data`는 shape `(5,)`인 1차원 배열이며 `theta`는 패킷 하나가 성공할 확률이다.
각 관측은 같은 `theta`를 갖고 서로 독립이라고 가정한다. 필수 범위에서
`data`는 비어 있지 않고 `0`과 `1`만 포함하며 `0 < theta < 1`이다.

## 사용할 정의

`x` 하나의 Bernoulli PMF는 다음과 같다.

```text
Bern(x | theta) = theta^x (1 - theta)^(1 - x),  x in {0, 1}
```

`n`개의 독립 Bernoulli 관측열 `D = (x_1, ..., x_n)`의 likelihood는
각 PMF의 곱이다. `k = sum_i x_i`로 두면 다음처럼 정리된다.

```text
L(theta; D) = product_i Bern(x_i | theta)
            = theta^k (1 - theta)^(n - k)
```

여기서는 `D`를 고정하고 `theta`를 바꾸어 가며 어떤 파라미터가 관측을
가장 그럴듯하게 만드는지 읽는다. likelihood는 `theta`에 대해 합이 1인
확률분포일 필요가 없다.

자연로그 log-likelihood는 곱을 합으로 바꾸어 준다.

```text
ell(theta; D) = k log(theta) + (n - k) log(1 - theta)
```

`K`가 `n`번 시행의 성공 횟수일 때 Binomial PMF는 다음과 같다.

```text
P(K = k | n, theta) = C(n, k) theta^k (1 - theta)^(n - k)
```

`C(n, k)`는 성공 `k`개를 배치할 수 있는 서로 다른 관측열의 개수다.
Binomial PMF는 특정 순서 하나가 아니라 성공 횟수가 `k`인 모든 순서의
확률을 합친다.

MLE는 관측된 `D`에 대해 likelihood를 가장 크게 만드는 `theta`다.

```text
theta_hat_MLE = argmax_theta L(theta; D)
              = argmax_theta ell(theta; D)
```

Bernoulli 데이터의 닫힌형 MLE는 다음과 같다. 미분은 이 과정의 S26에서
처음 배우므로 이 세션에서는 이 식을 유도하지 않고 데이터에 적용하고
의미를 설명한다.

```text
theta_hat_MLE = k / n = (1 / n) sum_i x_i
```

## 과제

### T1. 실행 전 예측

코드나 테스트를 실행하기 전 `answers.md`에 답한다.

1. 관측열 `[1, 0, 1, 1, 0]` 하나의 likelihood와 성공 횟수가 `3`인
   Binomial probability 중 어느 것이 더 클지 예측하고 이유를 적는다.
2. 고정된 데이터에서 `theta = 0.4`를 `theta = 0.6`으로 바꾸면 likelihood가
   커질지, 작아질지, 같을지 예측한다.
3. MLE가 `0.5`보다 클지, 같을지, 작을지 먼저 예측한다.

### T2. 같은 수치의 손계산

1. `n`, 성공 횟수 `k`, 실패 횟수 `n - k`를 구한다.
2. 각 관측의 Bernoulli PMF를 순서대로 적고 다섯 항을 곱해
   `L(theta; D)`를 구한다.
3. 정리된 식으로 같은 likelihood를 다시 구한다.
4. 자연로그 log-likelihood를 구하고 `log(L(theta; D))`와 같은지 확인한다.
5. `C(n, k)`를 구한 뒤 Binomial PMF를 구하고, 관측열 likelihood와의
   비율을 확인한다.
6. 제공된 닫힌형 MLE 식을 데이터에 적용하고, 그 값이 성공 비율이자
   binary 데이터의 표본평균인 이유를 적는다.

### T3. NumPy 직접 구현

`starter.py`의 다섯 함수를 완성한다.

- `bernoulli_pmf(x, theta)`: 관측 하나의 Bernoulli PMF를 반환한다.
- `bernoulli_likelihood(data, theta)`: 순서가 있는 관측열 likelihood를 반환한다.
- `bernoulli_log_likelihood(data, theta)`: 자연로그 log-likelihood를 반환한다.
- `binomial_pmf(k, n, theta)`: 성공 횟수의 Binomial PMF를 반환한다.
- `bernoulli_mle(data)`: `theta`의 MLE를 반환한다.

함수 계약은 다음과 같다.

- `data`는 비어 있지 않은 shape `(n,)`, dtype `int64`의 배열이고 `0`, `1`만
  포함한다.
- `x`, `k`, `n`은 Python `int`, `theta`는 Python `float`이다.
- 유효한 입력에서 `x in {0, 1}`, `0 <= k <= n`, `n > 0`,
  `0 < theta < 1`이다.
- 다섯 함수는 모두 Python `float`를 반환한다.
- likelihood와 MLE는 NumPy 배열 연산으로 구현하고, Binomial의
  조합계수는 표준 라이브러리 `math.comb`를 사용해도 된다.

필수 구현은 유효한 입력 계산에 집중하며 validation은 선택 확장으로 둔다.

### T4. 관계 검산

T2와 T3을 마친 뒤 다음을 확인한다.

1. 다섯 함수의 결과가 손계산과 일치하는지 `np.isclose`로 확인한다.
2. log-likelihood가 likelihood의 자연로그와 일치하는지 확인한다.
3. Binomial PMF를 관측열 likelihood로 나눈 값이 어떤 개수와 일치하는지
   확인한다.
4. `theta = 0.4`, `theta = 0.6`, 자신이 구한 MLE에서 likelihood를 계산해
   T1의 예측과 비교한다.

### T5. 잘못된 해석 실패 사례

다음 오류 중 두 개를 골라 왜 틀렸는지, 각 식이 실제로는 어떤 사건을
계산하는지 적는다.

1. 특정 관측열의 likelihood와 Binomial 성공 횟수 PMF를 항상 같다고 둔다.
2. 특정 관측열의 likelihood에도 `C(n, k)`를 곱한다.
3. likelihood를 그 자체로 `theta`에 대한 posterior 분포라고 해석한다.

### T6. 설명 확인

다음을 자기 말로 설명한다.

> 특정 binary 관측열의 Bernoulli likelihood와 성공 횟수의 Binomial
> probability는 어떻게 같고 어떻게 다른가? 데이터를 고정한 뒤 likelihood를
> `theta`의 함수로 읽는 이유는 무엇이며, MLE가 성공 비율이 되는 이유는
> 무엇인가?

## 검산

T1–T4를 작성하고 구현한 뒤 프로젝트 root에서 실행한다.

```bash
cd week3-machine-learning/curriculum/sessions/S05
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```

테스트는 중심 사례의 정답을 대신하지 않으며, 다른 유효한 입력에서도 함수가
공개된 정의와 계약을 따르는지 확인한다.

## 제출물

- `answers.md`: T1–T6의 예측, 손계산, 검산, 설명
- 완성한 `starter.py`
- 통과한 `test_contract.py` 실행 결과

## 완료 기준

- 개별 Bernoulli PMF와 독립 관측열 likelihood를 같은 수치로 계산한다.
- 순서가 있는 특정 관측열과 성공 횟수 사건의 차이를 조합계수로 설명한다.
- likelihood와 log-likelihood의 관계를 수치와 의미 양쪽에서 설명한다.
- MLE를 log-likelihood에서 도출하고 성공 비율과 연결한다.
- 다섯 함수가 다른 유효한 입력에서도 공개된 계약을 만족한다.
- 실행 전 예측과 실제 결과의 차이를 설명한다.
- 제공된 계약 테스트를 통과한다.

## 선택 확장

입력 validation을 추가한다. 배열 차원·dtype·빈 배열·binary 값, `x`, `k`,
`n`의 범위, `theta`의 범위를 나누어 검사하고 각 위반에 대한 자신의 테스트를
작성한다. 추가로 관측 수가 커질 때 probability 곱이 0으로 underflow할 수
있는 이유와 log-likelihood가 이를 어떻게 완화하는지 작은 예로 확인한다.
