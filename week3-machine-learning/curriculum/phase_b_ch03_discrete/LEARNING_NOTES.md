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

## S07 — Categorical 생성분류와 zero-count

### 데이터와 예측 방향

- count table의 행은 class, 열은 관측 가능한 category이며, 각 칸
  `N[c, j]`는 class `c`에서 category `j`를 관측한 표본 수다.
- 학습할 때는 표본의 class와 category를 모두 알고 count table을 만든다.
  예측할 때는 새 표본의 category `x`를 관측하고 class `y`를 예측한다.
- class-conditional table은 `p(x=j | c)`이므로 class별 행합 `N_c`로
  정규화한다. 각 행의 합은 1이어야 하지만 열의 합은 1일 필요가 없다.

### 생성분류 점수

- 관측 `x`가 고정되면 Bayes rule의 분모 `p(x)`는 모든 class에 공통이므로
  `p(c)p(x | c)` 또는 그 log 값의 `argmax`로 class를 예측할 수 있다.
- prior를 같은 count table의 행합으로 추정하고 feature가 category 하나이며
  smoothing하지 않은 특수한 경우에는
  `p(c)p(x=j | c) = (N_c/N)(N_cj/N_c) = N_cj/N`으로 약분된다. 이때만
  category 열의 raw count `argmax`와 생성분류 결과가 같다.

### Zero-count와 additive smoothing

- 어떤 class에서 category count가 0이면 해당 conditional과 joint가 0이
  되고 log-joint는 `-inf`가 된다. 모든 score가 `-inf`일 때 `np.argmax`는
  오류를 내지 않고 첫 인덱스를 반환하지만, 이는 증거에 따른 의미 있는
  분류가 아니다.
- additive smoothing은 `(N_cj + alpha) / (N_c + alpha*K)`로 계산한다.
  분자에만 `alpha`를 더하면 행합이 1보다 커져 확률분포의 의미가 깨진다.
- smoothing은 `alpha > 0`일 때 zero probability를 없애지만, 적절한
  `alpha`, 올바른 class 예측, 모형의 타당성을 보장하지 않는다.
- 모든 class에서 같은 category가 zero-count여도 smoothed likelihood는
  `alpha / (N_c + alpha*K)`이므로 일반적으로 class마다 같지 않다. 다만
  S07처럼 empirical prior `N_c/N`을 쓰면 최종 점수는 `N_c`에 따라
  증가하므로 prior의 순서를 따른다.

### NumPy 축과 shape

- `(C, K)` count table에서 `sum(axis=0)`은 class 축을 없애 category별 합
  shape `(K,)`를 남기고, `sum(axis=1)`은 category 축을 없애 class별 합
  shape `(C,)`를 남긴다.
- 행 정규화에서는 `sum(axis=1, keepdims=True)`로 shape `(C, 1)`을
  유지하면 `(C, K) / (C, 1)` broadcasting의 방향이 명확해진다.
  `sum(axis=1)[:, None]`도 같은 shape을 만든다.
- 특정 category에 대한 모든 class의 확률은 `conditionals[:, category]`로
  선택한다.

### 새 API

- `np.sum(a, axis=axis, keepdims=True)`: reduction한 축을 크기 1로 유지한다.
- `np.log(a)`: 배열 원소별 자연로그를 계산하며 `np.log(0)`은 `-inf`다.
- `np.errstate(divide="ignore")`: 의도된 `log(0)`의 divide warning만 지정한
  범위에서 숨긴다.
- `np.argmax(scores)`: 최댓값의 위치를 반환한다. Python `int` 계약에는
  `int(np.argmax(scores))`처럼 명시적으로 변환한다.
- `np.isfinite(scores)`: score가 유한한지 검사해 all-`-inf` 예측을 거른다.
