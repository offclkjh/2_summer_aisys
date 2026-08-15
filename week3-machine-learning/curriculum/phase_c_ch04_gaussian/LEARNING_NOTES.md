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

## S09 — Vector와 covariance

### Outer product 평균과 covariance matrix

- 공분산행렬은 centered sample vector들의 outer product를 모두 더한 뒤
  `N`으로 나눈 경험적 평균이다. 여기서 `1/N`은 기댓값을 표본평균으로
  근사한다는 의미다.
- sample vector를 데이터 행렬의 행 또는 열로 쌓으면, 올바른 방향의
  행렬곱이 outer product들의 합을 자연스럽게 만든다. 어떤 곱을 사용할지는
  기호가 아니라 데이터 행렬의 shape와 각 축의 의미로 판단한다.
- 행이 observation이고 열이 feature인 centered matrix `R`에서는 feature
  covariance의 shape가 `(D,D)`가 되도록 곱의 방향을 정한다. 반대 방향의
  곱은 `(N,N)`인 centered Gram matrix로, observation 간 inner product를
  나타내며 feature covariance와는 다른 객체다.

### Covariance와 correlation 해석

- covariance matrix의 대각 원소는 각 feature의 variance이고, 비대각 원소는
  두 feature가 평균에서 함께 벗어나는 방향과 크기를 나타내는 covariance다.
- correlation matrix의 대각은 자기 자신과의 correlation이므로 1이다.
  covariance matrix의 대각은 표준화된 경우가 아니면 1일 필요가 없다.
- covariance의 비대각 원소가 개별 대각 원소보다 항상 작아야 하는 것은
  아니다. 다만 두 대각 원소가 나타내는 variance와 연결된 크기 제약을 받는다.

### Linear transform 뒤의 covariance

- `y = A x`일 때 변환된 covariance는 `A Sigma A.T`다. 이는 원자료를 먼저
  선형변환한 뒤 covariance를 구하는 것과, 원래 covariance를 행렬로
  변환하는 것이 같은 연산임을 나타낸다.
- `A`가 한 행이면 여러 feature를 하나의 선형결합으로 바꾸므로 결과 변수는
  하나다. 따라서 변환된 covariance의 shape는 `(1,1)`이며 값은 그
  선형결합의 variance다.
- 이 규칙은 변환된 평균, centered value, outer product의 순서로 전개하여
  다시 설명할 수 있어야 한다. 직접 계산과 공식의 결과가 다르면 공식보다
  먼저 centering과 outer-product 합을 점검한다.

### NumPy shape 점검

- NumPy의 `(D,)` 배열은 row/column 방향을 구분하지 않으며 transpose해도
  shape가 바뀌지 않는다. 내적과 outer product를 구분하려면 연산 전에 각
  operand를 명시적인 column/row shape로 해석하고 결과 shape를 예측한다.
- 행렬 기호의 문자 이름이 달라도 차원의 역할이 같으면 같은 구조다. 암기한
  문자보다 `(입력 차원 -> 출력 차원)`과 곱의 안쪽 차원이 맞는지를 우선 본다.

### 현재 이해와 다음 점검

- outer product 평균, covariance와 correlation의 차이, 한 행짜리 `A`가
  만드는 선형결합의 variance까지의 직관은 형성되었다.
- 다음 세션에서는 공식을 계산하기 전에 데이터 행렬의 두 축, 각 operand의
  shape, 예상 결과 shape를 먼저 적는 습관을 확인한다.
- 튜터 채점에서는 명시적 요청 전까지 완성 코드나 직접 정답을 공개하지 않고,
  정오 판정과 단계적 힌트로 스스로 수정할 수 있게 한다.
