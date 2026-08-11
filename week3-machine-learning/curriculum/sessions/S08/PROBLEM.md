# S08 — 1차원 Gaussian
> 상태: `ready`. 실행 전 예측을 먼저 기록한다.

## 목표와 비목표
- 목표: Gaussian log-density/NLL, mean·variance MLE, fixed-variance NLL과 SSE의 관계를 계산한다.
- 비목표: autograd, optimizer, 미분 유도, multivariate Gaussian.

## 시작 전 선수지식 확인
1. 자연로그가 곱을 어떤 연산으로 바꾸는가?
2. 표본평균과 편차 `x-mean`의 의미는 무엇인가?
3. MLE에서 데이터와 parameter 중 무엇을 고정하는가?

막히면 [로그 복습](../../concepts/logarithm.md),
[S03 expectation/variance](../S03/PROBLEM.md#사용할-정의),
[S05 MLE](../S05/PROBLEM.md#사용할-정의)를 복습한다.

## 교재 연결
- Kevin P. Murphy, *MLAPP* (2012), Ch.4 univariate Gaussian and Gaussian MLE.

## 문제에서 주어진 정보
```python
data = np.array([1.0, 2.0, 3.0], dtype=np.float64)
candidate_mean = 1.5
variance = 2.0
```

## 사용할 정의
```text
log N(x|mu,v) = -0.5[log(2*pi*v) + (x-mu)^2/v]
NLL(mu,v) = -sum_i log N(x_i|mu,v)
SSE(mu) = sum_i (x_i-mu)^2
mu_hat = mean(data)
v_hat_MLE = SSE(mu_hat)/n
```
`v`는 표준편차가 아니라 variance다. fixed positive `v`에서 NLL은
`n/2 log(2*pi*v) + SSE/(2v)`이므로 NLL와 SSE는 같은 mean에서 최소다.
variance MLE의 분모는 `n`이며 unbiased sample variance의 `n-1`과 목적이 다르다.

## 구현 도구 구분

- **직접 구현:** Gaussian log-density, NLL, SSE, mean MLE, variance MLE.
  `gaussian_mean_mle`는 `np.mean`, `gaussian_variance_mle`는 `np.var`로 바로
  대체하지 않고 공개된 합·분모 정의를 쓴다.
- **사용 권장 API:** vectorized `-`, `**`, `/`, `np.sum`, `np.log`,
  `data.size`. 이 기본 배열 연산은 직접 재구현하지 않는다.
- **검산 전용 API:** `np.mean`, `np.var(ddof=0)`, `np.var(ddof=1)`.
  T1–T3 완료 후 직접 구현 결과와만 비교한다.
- **표준 검산 선택:** mean은 `np.mean(data)`, variance MLE는
  `np.var(data, ddof=0)`, unbiased sample variance는 `np.var(data, ddof=1)`다.
  `ddof`가 분모를 `N-ddof`로 바꾸므로 반드시 명시한다.

## 과제
### T1. 실행 전 예측
1. **T1-1** candidate mean이 data mean보다 큰지/작은지 예측한다.
2. **T1-2** candidate와 MLE mean 중 SSE/NLL이 작은 쪽을 예측한다.
3. **T1-3** variance MLE와 `n-1` sample variance가 같은지 예측한다.
### T2. 손계산
1. **T2-1** candidate mean의 residual, squared residual, SSE를 구한다.
2. **T2-2** 세 log-density와 합 NLL을 구한다.
3. **T2-3** mean MLE와 그 위치의 SSE를 구한다.
4. **T2-4** variance MLE와 `n-1` sample variance를 구해 비교한다.
### T3. 직접 구현
1. **T3-1** `gaussian_logpdf(x, mean, variance) -> x.shape float64`를 완성한다.
2. **T3-2** `gaussian_nll(data, mean, variance) -> float`를 완성한다.
3. **T3-3** `squared_error_sum(data, mean) -> float`를 완성한다.
4. **T3-4** `gaussian_mean_mle(data) -> float`를 완성한다.
5. **T3-5** `gaussian_variance_mle(data, mean) -> float`를 완성한다.
계약: data/x는 nonempty 1D `float64`, `variance>0`, scalar 반환은 Python `float`.
부동소수 비교 허용오차는 `rtol=1e-7`, `atol=1e-12`다.
### T4. 검산
1. **T4-1** `-sum(logpdf)`와 NLL을 비교한다.
2. **T4-2** 손계산과 다섯 함수 결과를 비교한다.
3. **T4-3** 두 mean의 NLL 차이와 `SSE/(2v)` 차이를 비교한다.
4. **T4-4** MLE를 `np.mean`, `np.var(ddof=0)`와 비교한다.
### T5. 잘못된 해석
1. **T5-1** variance 자리에 표준편차를 넣는 오류를 설명한다.
2. **T5-2** variance MLE에 `n-1`을 쓰는 오류를 설명한다.
3. **T5-3** mean마다 variance도 바꾸면서 NLL/SSE 순서가 항상 같다고 하는 오류를 설명한다.
### T6. 설명 확인
1. **T6-1** Gaussian log-density의 residual penalty를 설명한다.
2. **T6-2** fixed variance에서 NLL과 SSE가 같은 minimizer를 갖는 이유를 설명한다.
3. **T6-3** variance MLE와 unbiased sample variance의 목적을 구분한다.

## 검산
```bash
cd week3-machine-learning/curriculum/sessions/S08
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```
## 제출물
`answers.md`, 완성한 `starter.py`, 통과한 계약 테스트.
## 완료 기준
T1–T6을 설명하고 NLL/SSE/MLE 관계와 분모 `n`·`n-1`을 구분한다.
## 선택 확장
세 mean 후보를 추가해 NLL과 SSE 순서를 비교한다.
