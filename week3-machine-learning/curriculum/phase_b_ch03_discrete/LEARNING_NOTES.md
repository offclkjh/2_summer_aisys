# Phase B — 이산분포와 생성분류 학습 노트

S05–S07에서 다시 사용할 API, MLE의 의미, likelihood 내용만 누적한다.

## S05 — Bernoulli·Binomial

### Likelihood

- 성공 `k`번, 실패 `n - k`번인 특정 ordered sequence의 likelihood는
  `theta**k * (1 - theta)**(n - k)`다.
- Binomial PMF는 성공 횟수가 `k`인 모든 ordered sequence를 하나의
  사건으로 묶으므로 sequence likelihood에 `C(n, k)`를 곱한다.
- `C(n, k)`는 `theta`와 무관한 상수이므로 ordered likelihood와 Binomial
  PMF의 값은 다르지만 `theta`에 대한 MLE는 같다.
- likelihood는 데이터를 고정하고 `theta`를 바꾸어 읽는 함수이며,
  `theta`에 대해 정규화된 posterior 분포가 아니다.

### MLE의 의미

- Bernoulli MLE `theta_hat = k / n`은 관측된 성공 비율이자 binary
  데이터의 표본평균이다. 이는 실제 `theta`의 확정값이 아니라 현재
  데이터를 가장 그럴듯하게 만드는 점 추정값이다.

### 새 API

- `math.comb(n, k)`: 조합계수 `C(n, k)`를 계산한다.
- `np.log(x)`: 자연로그를 계산한다.

## S06 — Categorical·Multinomial

### Likelihood

- ordered Categorical sequence likelihood는 `np.prod(theta[labels])`로 표현한다.
- Multinomial count PMF는 관측 순서를 제거하고 category별 count만 남긴
  사건의 확률이다. 표준 분포 API는
  `scipy.stats.multinomial.pmf(counts, n=n, p=theta)`다.
- count PMF와 ordered sequence likelihood의 비율은 Multinomial 계수이고,
  이 계수는 `theta`와 무관하다.

### MLE의 의미

- Categorical MLE는 `counts / counts.sum()`이며 각 category의 관측 비율이다.
- 결과 vector의 합은 1이고, 각 성분은 실제 parameter의 확정값이 아니라
  현재 데이터에서의 추정값이다.

### 새 API

- `np.eye(K, dtype=np.float64)[labels]`: integer label를 one-hot row로 변환한다.
- `np.bincount(labels, minlength=K)`: category count vector를 만든다.
- `np.prod(theta[labels])`: 선택된 Categorical PMF 항을 곱한다.
- `scipy.stats.multinomial.pmf(counts, n=n, p=theta)`: Multinomial count PMF를 계산한다.
