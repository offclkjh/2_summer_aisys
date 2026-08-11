# Phase B — 이산분포와 생성분류 학습 노트

S05–S07에서 다시 사용할 MLAPP 코어, 새 API, 구현 규칙만 누적한다.

## S05 — Bernoulli·Binomial

### MLAPP 코어

- Bernoulli 변수에서 `1`의 확률은 `theta`, `0`의 확률은
  `1 - theta`다.
- 성공 `k`번, 실패 `n - k`번인 특정 ordered sequence의 likelihood는
  `theta**k * (1 - theta)**(n - k)`다.
- Binomial PMF는 성공 횟수가 `k`인 모든 ordered sequence를 하나의
  사건으로 묶으므로 sequence likelihood에 `C(n, k)`를 곱한다.
- `C(n, k)`는 `theta`와 무관한 상수이므로 ordered likelihood와 Binomial
  PMF의 값은 다르지만 `theta`에 대한 MLE는 같다.
- 로그는 곱을 합으로 바꾸고 단조증가하므로 likelihood와 log-likelihood는
  같은 `theta`에서 최대가 된다.
- Bernoulli MLE `theta_hat = k / n`은 관측된 성공 비율이자 binary
  데이터의 표본평균이다. 이는 실제 `theta`의 확정값이 아니라 현재
  데이터를 가장 그럴듯하게 만드는 점 추정값이다.
- likelihood는 데이터를 고정하고 `theta`를 바꾸어 읽는 함수이다. 그 자체는
  `theta`에 대해 정규화된 posterior 분포가 아니다.

### 새 API

- `math.comb(n, k)`: 조합계수 `C(n, k)`를 계산한다.
- `np.log(x)`: 자연로그를 계산한다.

### 재사용할 구현 규칙

- Bernoulli PMF는 `x=0`과 `x=1`의 두 경우를 모두 다루어야 한다.
- 큰 데이터에서는 작은 확률을 먼저 곱한 후 로그를 취하지 말고,
  로그 항을 직접 더해 log-likelihood를 구한다.
- 공개 함수가 Python `float`를 약속하면 NumPy scalar 결과를
  `float(result)`로 변환해 반환한다.
