# Phase C — Gaussian models 학습 노트

S08–S12에서 다시 사용할 Gaussian 계산, MLE, covariance 내용을 세션별로
누적한다.

## S08 — 1차원 Gaussian

### Gaussian log-density와 NLL

- 1차원 Gaussian log-density는
  `-0.5 * (log(2*pi*v) + (x-mu)**2 / v)`다.
- residual `x - mu`는 관측값과 모델의 중심 사이 차이다. 제곱하므로 평균의
  양쪽을 같은 방식으로 벌점화하고, 평균에서 멀어질수록 벌점이 커진다.
- likelihood와 log-likelihood는 클수록 좋다. 학습 코드는 손실을 최소화하는
  형태를 주로 사용하므로 log-likelihood에 음수를 붙인 NLL을 사용한다.
  따라서 log-likelihood 최대화와 NLL 최소화는 같은 parameter를 고른다.
- 여러 표본의 NLL은 각 log-density를 더한 뒤 부호를 바꾼 값이다.

### Fixed-variance NLL과 SSE

- `SSE(mu) = sum((x_i - mu)**2)`는 mean을 예측값으로 보았을 때 squared
  residual의 합이다.
- variance `v`를 모든 mean 후보에서 같은 값으로 고정하면
  `NLL(mu, v) = n/2*log(2*pi*v) + SSE(mu)/(2*v)`다. 첫 항은 mean과
  무관하고 `1/(2*v)`는 양수이므로 NLL과 SSE는 같은 mean에서 최소가 된다.
- mean 후보마다 서로 다른 variance를 사용하면 `log(v)`와 `1/v`도 함께
  달라진다. 이 경우 SSE가 작은 후보의 NLL도 항상 작다고 단정할 수 없다.

### Gaussian MLE와 분산의 분모

- Gaussian mean MLE는 표본평균이며, 합의 정의로는 `data.sum()/data.size`다.
- mean이 주어졌을 때 variance MLE는 `SSE(mean)/n`이다. 이는 관측 데이터의
  likelihood를 최대화하는 parameter 추정량이다.
- unbiased sample variance는 표본으로 모집단 분산을 반복 추정할 때의 편향을
  보정하려고 `n-1`로 나눈다. 목적이 다르므로 variance MLE의 정의에
  `n-1`을 사용하면 안 된다.

### NumPy 구현 메모

- `np.pi`는 NumPy가 제공하는 원주율 상수이고, `np.log`는 원소별 자연로그를
  계산한다.
- `return` 뒤의 `pass`는 실행되지 않으므로 구현을 마친 뒤 제거한다.
