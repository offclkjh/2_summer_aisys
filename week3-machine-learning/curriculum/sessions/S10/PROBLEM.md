# S10 — Multivariate Gaussian 계산

> 상태: `ready`. 학부 2학년 수준의 선형대수와 확률론을 이수했다고 가정한다.
> 핵심 문제와 deep dive를 구분하며, 실행 전 예측을 먼저 기록한다.

## 목표와 비목표

### Core (120분 이내)

- 표준 Gaussian의 affine transform과 Jacobian으로 다변량 Gaussian density를 유도한다.
- SPD covariance, Mahalanobis quadratic form, determinant의 확률·기하적 의미를 연결한다.
- residual, linear solve, log-determinant로 batched log-density를 계산한다.
- explicit inverse/determinant 대신 `solve`/`slogdet`를 사용하는 수치적 이유를 설명한다.

### Deep dive (선택)

- eigendecomposition으로 covariance의 주축과 축별 분산을 해석한다.
- Cholesky factor를 whitening과 log-determinant 계산에 연결한다.
- condition number와 거의 singular한 covariance가 계산에 미치는 영향을 관찰한다.

Cholesky·eigendecomposition **알고리즘 자체를 구현**하거나 고차원 성능을
benchmark하는 것은 이번 세션의 범위가 아니다.

## 시작 전 선수지식 확인

기초 정의를 다시 강의하지는 않는다. 다음을 식과 shape으로 설명할 수 있으면 바로
진행한다.

1. 대칭행렬이 positive definite라는 조건을 quadratic form으로 쓰면?
2. `Az=b`에서 inverse를 만들지 않고 `z`를 구하는 NumPy 함수는?
3. 선형변환 `x=Az+b`에서 density의 change-of-variables 식에 어떤
   determinant가 등장하는가?
4. orthogonal matrix `Q`에 대해 `Q^-1`과 determinant의 절댓값은?

특정 항목만 막히면 [vector/matrix](../../concepts/vector_matrix.md),
[linear system](../../concepts/linear_system.md),
[S09 covariance](../S09/PROBLEM.md#사용할-정의)의 해당 부분만 복습한다.

## 교재 연결

- Kevin P. Murphy, *Machine Learning: A Probabilistic Perspective* (2012), Ch. 4
- 주제: multivariate Gaussian density, Mahalanobis distance, covariance geometry
- 이 세션은 교재의 수학적 관점을 한 개의 2D 사례와 안정적 NumPy 구현에 연결한다.

## 모델과 가정

$$
x\in\mathbb R^D,\qquad
\mu\in\mathbb R^D,\qquad
\Sigma\in\mathbb R^{D\times D}.
$$

`Sigma`는 symmetric positive definite(SPD)라고 가정한다.

- 대칭성: `Sigma = Sigma.T`
- 양의 정부호: 모든 `v != 0`에 대해 $v^T\Sigma v>0$
- 결과: 모든 고유값이 양수이고, $\det\Sigma>0$이며, $\Sigma^{-1}$와
  Cholesky factor가 존재한다.

이 가정은 단순한 구현 편의가 아니다. Full-rank Gaussian이 모든 방향에서 양의
분산을 갖고, 유한한 density로 정규화되기 위한 조건이다. Positive semidefinite지만
singular한 covariance는 더 낮은 차원의 부분공간에 놓인 별도 분포로 다뤄야 한다.

## 사용할 정의

### 1. Affine transform과 density 유도

표준 Gaussian $z\sim\mathcal N(0,I_D)$와 invertible matrix $L$에 대해

$$
x=\mu+Lz,\qquad \Sigma=LL^T
$$

로 둔다. 이 affine transform의 평균과 covariance는

$$
\mathbb E[x]=\mu,\qquad
\operatorname{Cov}[x]=L\operatorname{Cov}[z]L^T=LL^T=\Sigma.
$$

역변환은 $z=L^{-1}(x-\mu)$이고, density는 change of variables에 의해

$$
p_x(x)=p_z\!\left(L^{-1}(x-\mu)\right)|\det L^{-1}|.
$$

여기서 $r=x-\mu$라 하면

$$
\|L^{-1}r\|_2^2
=r^TL^{-T}L^{-1}r
=r^T\Sigma^{-1}r,
$$

그리고 $\det\Sigma=\det(LL^T)=(\det L)^2$다. 따라서

$$
p(x\mid\mu,\Sigma)
=(2\pi)^{-D/2}|\Sigma|^{-1/2}
\exp\!\left(-\frac12r^T\Sigma^{-1}r\right).
$$

로그를 취하면 실제 구현에 사용할 식을 얻는다.

$$
\log p(x\mid\mu,\Sigma)
=-\frac12\left[D\log(2\pi)+\log|\Sigma|+r^T\Sigma^{-1}r\right].
$$

### 2. Mahalanobis quadratic form

$$
q(x)=r^T\Sigma^{-1}r
$$

는 squared Mahalanobis distance다. $\Sigma^{-1}$는 precision matrix이며,
분산이 작은 방향의 오차를 더 크게 벌점화한다. SPD 가정으로 $q(x)\ge 0$이고
$q(x)=0$은 $x=\mu$일 때뿐이다.

### 3. Eigen 관점의 covariance geometry

대칭 SPD covariance는

$$
\Sigma=Q\Lambda Q^T,
\qquad Q^TQ=I,
\qquad \Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_D),
$$

로 직교대각화된다. Principal coordinates $y=Q^Tr$에서는

$$
q(x)=\sum_{j=1}^D\frac{y_j^2}{\lambda_j},
\qquad
|\Sigma|=\prod_{j=1}^D\lambda_j.
$$

따라서 $q(x)=c$인 등밀도면은 고유벡터 방향을 주축으로 하고, 각 반축 길이는
$\sqrt{c\lambda_j}$다. Determinant의 제곱근
$\sqrt{|\Sigma|}$는 이 타원체의 부피 scale이며, density의 정규화항이
분포가 넓어질수록 낮아지는 이유를 설명한다.

### 4. Shape과 계산 경로

| 객체 | Shape | 의미 |
|---|---:|---|
| `observations` | `(N,D)` | 행마다 관측 하나 |
| `mean` | `(D,)` | 평균 벡터 |
| `covariance` | `(D,D)` | SPD covariance |
| `residuals` | `(N,D)` | `observations - mean` |
| `solutions` | `(N,D)` | 행마다 `covariance @ z_i = r_i`의 해 |
| `q` | `(N,)` | 관측별 squared Mahalanobis distance |
| `logpdf` | `(N,)` | 관측별 log-density |

수학식에 $\Sigma^{-1}$가 있어도 inverse를 만들 필요는 없다.

```text
residuals = observations - mean
solve covariance @ solutions.T = residuals.T
q_i = residuals_i.T @ solutions_i
logpdf_i = -0.5 * (D*log(2*pi) + logdet + q_i)
```

## 확률적 의미와 수치적 구현

Gaussian log-density의 세 항은 서로 다른 역할을 한다.

- $D\log(2\pi)$: 차원에 따른 상수
- $\log|\Sigma|$: 전체 분포의 부피 scale과 정규화
- $q(x)$: 관측 위치에 따른 상대적 벌점

같은 $\mu,\Sigma$ 아래에서는 앞의 두 항이 모든 관측에 공통이므로 density
순서는 $q(x)$의 역순이다. 서로 다른 covariance를 가진 모델을 비교할 때는
Mahalanobis 항만 비교하면 안 되고 log-determinant 항도 반드시 필요하다.

### 왜 `solve`와 `slogdet`인가

- `inv(covariance) @ residual`은 필요하지 않은 inverse 전체를 명시적으로 만들고
  추가 행렬곱과 반올림 오차를 만든다.
- `solve(covariance, residuals.T)`는 한 번의 호출에서 여러 RHS를 함께 풀며,
  우리가 실제로 원하는 해를 직접 계산한다.
- `log(det(covariance))`는 determinant를 먼저 너무 크거나 작게 만든 뒤 log를
  취한다. `slogdet`는 sign과 log absolute determinant를 직접 반환한다.
- 두 방법 모두 dense matrix에서는 주된 계산이 대체로 $O(D^3)$이지만,
  같은 차수라는 사실이 불필요한 계산과 수치 오차까지 같다는 뜻은 아니다.

### Cholesky, eigen, condition number

SPD가 보장되면 $\Sigma=LL^T$인 Cholesky factor를 사용할 수 있다. 먼저
$Ly=r$을 풀면 $q=\|y\|_2^2$,
$\log|\Sigma|=2\sum_j\log L_{jj}$가 된다. 이는 whitening 관점과 계산이
직접 연결되는 경로다. Core 구현은 generic `solve`/`slogdet` 계약을 유지하고,
Cholesky 경로는 deep dive에서 동치성을 검산한다.

Eigendecomposition은 주축 해석에 가장 투명하지만, log-density 하나를 계산하기
위해 매번 고유벡터 전체가 필요한 것은 아니다. 반면 작은 고유값을 관찰하면
거의 singular한 방향과 큰 condition number를 진단할 수 있다.

## 문제에서 주어진 정보

```python
mean = np.array([0., 0.], dtype=np.float64)                    # (D,)
covariance = np.array([[2., 1.], [1., 2.]], dtype=np.float64) # (D,D)
observations = np.array([[1., 0.], [0., 2.]], dtype=np.float64) # (N,D)
```

이 세션의 구현 계약에서는 입력 dtype이 `float64`, $N,D\ge 1$, covariance가
SPD라고 주어진다.

## 구현 도구 구분

- **직접 구현:** residual → linear solve → Mahalanobis reduction → log-density의
  전체 계산 경로
- **사용 권장 API:** `np.linalg.solve`, `np.linalg.slogdet`, transpose `.T`,
  `np.sum(..., axis=1)`, broadcasting, `np.log`
- **Core에서 사용하지 않음:** `np.linalg.inv`, `np.linalg.det`, 완성된 Gaussian
  분포 함수
- **Deep dive/검산:** `np.linalg.eigh`, `np.linalg.cholesky`, `np.linalg.cond`,
  `scipy.stats.multivariate_normal.logpdf`

표준 검산은 먼저 `covariance @ solutions.T == residuals.T`를 확인하고, 공개된
log-density 식으로 결과를 비교한다. Core를 마친 뒤 `standard_api.py`에서
solve, Cholesky, eigen 세 관점의 동치성을 확인한다.

## 과제

다음 T1–T6은 Core다. Deep dive는 Core를 마친 뒤 선택한다.

### T1. 실행 전 예측

1. **T1-1** residuals, solutions, Mahalanobis 배열, logpdf의 shape을 예측한다.
2. **T1-2** 두 observation 중 mean에 Mahalanobis 기준으로 더 가까운 것을
   수치 계산 전에 예측하고 근거를 적는다.
3. **T1-3** 어느 observation의 log-density가 더 높은지 예측한다.
4. **T1-4** `slogdet`의 sign과 그 근거를 SPD 성질로 설명한다.

### T2. 유도 재구성

1. **T2-1** $x=\mu+Lz$에서 change of variables를 적용해 정규화항의
   $|\det L|^{-1}$를 얻는 과정을 자신의 식으로 다시 쓴다.
2. **T2-2** $\|L^{-1}r\|^2=q(x)$와 $|\Sigma|=(\det L)^2$를 보여 최종
   density 식으로 연결한다.
3. **T2-3** SPD가 보장하는 성질 중 이번 density와 계산에 실제 사용되는 것을
   세 가지 이상 골라 연결 관계를 설명한다.

### T3. 2D 손계산

1. **T3-1** 두 residual vector를 구한다.
2. **T3-2** 각 $\Sigma z_i=r_i$를 풀어 $z_i$를 구한다.
3. **T3-3** 두 $q_i=r_i^Tz_i$를 구한다.
4. **T3-4** determinant, sign, logabsdet를 구한다.
5. **T3-5** 두 log-density를 구하고 T1의 예측과 비교한다.

### T4. 직접 구현

1. **T4-1** `mahalanobis_squared(x, mean, covariance) -> float`를 `solve`로
   완성한다.
2. **T4-2**
   `multivariate_gaussian_logpdf(observations, mean, covariance) -> (N,) float64`
   를 `solve`/`slogdet`로 완성한다.

`np.linalg.inv`, `np.linalg.det`는 사용하지 않는다. 부동소수 비교 허용오차는
`rtol=1e-7`, `atol=1e-12`다. Batch size가 1이어도 반환 shape `(1,)`을 유지한다.

### T5. 수치해석과 실패 해석

1. **T5-1** `residual/covariance`가 선형계를 대신하지 못하는 이유를 연산의
   의미로 설명한다.
2. **T5-2** `residuals*solutions`를 `axis=0`으로 합했을 때 생기는 shape과
   의미 오류를 설명한다.
3. **T5-3** explicit inverse와 `solve`의 복잡도가 같은 차수일 수 있는데도
   `solve`를 선택하는 이유를 설명한다.
4. **T5-4** determinant가 아주 크거나 작은 상황에서 `log(det(Sigma))`와
   `slogdet(Sigma)`의 중간 계산이 어떻게 다른지 설명한다.

### T6. 통합 설명

1. **T6-1** affine transform → covariance → quadratic form → log-density를
   하나의 흐름으로 설명한다.
2. **T6-2** Euclidean distance와 Mahalanobis distance의 차이를 covariance
   ellipse의 방향과 축 길이로 설명한다.
3. **T6-3** batch 계산의 모든 중간 shape과 관측별 reduction axis를 설명한다.

## Deep dive 과제

### D1. Eigendecomposition과 주축

1. 주어진 covariance의 eigenvalue/eigenvector를 손으로 구한 뒤 `np.linalg.eigh`로
   검산한다.
2. 두 residual을 principal coordinates로 바꾸고
   $q=\sum_j y_j^2/\lambda_j$로 다시 계산한다.
3. 등밀도 타원의 장축 방향과 두 반축 길이의 비를 eigenvalue로 설명한다.

### D2. Cholesky와 whitening

1. `np.linalg.cholesky`로 $L$을 구해 $LL^T=\Sigma$를 검산한다.
2. $Ly_i=r_i$를 풀고 $\|y_i\|^2$가 Core의 Mahalanobis 값과 같은지 확인한다.
3. $2\sum_j\log L_{jj}$가 `slogdet`의 logabsdet와 같은지 확인한다.

### D3. Conditioning 실험

서로 다른 작은 양의 $\epsilon$에 대해
$\Sigma_\epsilon=Q\operatorname{diag}(1,\epsilon)Q^T$를 만든다.

1. 실행 전에 $\epsilon$이 작아질 때 condition number와 타원 모양을 예측한다.
2. 작은 고유값 방향의 residual에 대한 Mahalanobis term 변화를 관찰한다.
3. Mathematical SPD와 numerically reliable한 계산이 왜 별개의 질문인지 설명한다.

### D4. Covariance scale과 정규화

$\Sigma$를 $c\Sigma$, $c>0$로 바꾸었을 때 Mahalanobis 항과
log-determinant 항이 각각 어떻게 변하는지 유도한다. 평균에 가까운 점과 먼 점의
log-density가 같은 방식으로 변하는지도 분석한다.

## 검산

```bash
cd week3-machine-learning/curriculum/sessions/S10
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
../../../../.venv/bin/python standard_api.py  # Core 완료 후 선택
```

## 제출물

- `answers.md`: T1–T3, T5–T6의 식과 설명
- `starter.py`: T4 구현
- 통과한 `test_contract.py`
- 선택: D1–D4의 계산과 관찰

## 완료 기준

- affine transform과 Jacobian에서 Gaussian density를 재구성할 수 있다.
- SPD, eigen geometry, Mahalanobis term, determinant 정규화의 관계를 설명한다.
- inverse 없이 `(N,)` batched log-density를 허용오차 안에서 계산한다.
- `solve`/`slogdet` 선택을 shape뿐 아니라 수치 안정성 관점에서도 설명한다.

Deep dive는 Core 완료 조건에 포함하지 않지만, 이후 PCA·whitening·Gaussian
conditioning을 위한 선형대수 연결을 제공한다.
