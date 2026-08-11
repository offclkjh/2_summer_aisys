# S10 — Multivariate Gaussian 계산
> 상태: `ready`. 실행 전 예측을 먼저 기록한다.

## 목표와 비목표
- 목표: residual, Mahalanobis distance, log-determinant로 batched log-density를 계산한다.
- 목표: explicit inverse/determinant 대신 `solve`/`slogdet`를 사용한다.
- 비목표: Cholesky 구현, eigendecomposition, 고차원 benchmark.

## 시작 전 선수지식 확인
1. `A z=b`에서 inverse를 만들지 않고 `z`를 구하는 NumPy 함수는?
2. `(N,D)` residual에서 observation별 합을 구할 axis는?
3. covariance matrix의 shape와 대칭성은?

막히면 [vector/matrix 복습](../../concepts/vector_matrix.md),
[선형계 복습](../../concepts/linear_system.md),
[S09 covariance matrix](../S09/PROBLEM.md#사용할-정의)를 복습한다.

## 교재 연결
- Kevin P. Murphy, *MLAPP* (2012), Ch.4 multivariate Gaussian density.

## 문제에서 주어진 정보
```python
mean = np.array([0., 0.], dtype=np.float64)                    # (D,)
covariance = np.array([[2., 1.], [1., 2.]], dtype=np.float64) # (D,D)
observations = np.array([[1., 0.], [0., 2.]], dtype=np.float64) # (N,D)
```
covariance는 symmetric positive definite(SPD)라고 주어진다. 이로 인해 선형계의
해가 유일하고 determinant 부호가 양수다.

## 사용할 정의
```text
r = x-mu
q = r^T Sigma^-1 r
log N(x|mu,Sigma) = -0.5[D log(2*pi) + log|Sigma| + q]
```
inverse를 만들지 말고 `z=np.linalg.solve(Sigma,r)`, `q=r.T@z`로 계산한다.
batch에서는 RHS를 `residuals.T` shape `(D,N)`로 주고 결과를 다시 transpose한다.
`sign, logabsdet=np.linalg.slogdet(Sigma)`는 determinant를 먼저 크게/작게 만들지
않고 부호와 log absolute determinant를 준다. SPD에서 `sign=1`이다.

## 구현 도구 구분

- **직접 구현:** residual→linear solve→Mahalanobis quadratic term→
  multivariate Gaussian log-density의 전체 경로. 완성된 Gaussian 분포
  함수로 대체하지 않는다.
- **사용 권장 API:** `np.linalg.solve`, `np.linalg.slogdet`, transpose `.T`,
  `np.sum(..., axis=1)`, broadcasting, `np.log`. `solve`/`slogdet`는 이 세션에서
  재구현할 대상이 아니다.
- **검산 전용 API:** 추가 분포 라이브러리 없이 `test_contract.py`의
  독립 reference 계산으로 검산한다. `np.linalg.inv`/`np.linalg.det`는
  검산용으로도 권장하지 않는다.
- **표준 검산 선택:** `np.testing.assert_allclose(covariance @ z, residual)`로
  선형계를 먼저 검산하고, 공개된 scalar logpdf 정의식으로 최종 배열을
  비교한다. 추가 분포 패키지 없이 재현 가능하고 `solve` 경로를 직접
  확인할 수 있어 이 프로젝트의 표준 검산으로 사용한다.

## 과제
### T1. 실행 전 예측
1. **T1-1** residuals와 logpdf 출력 shape을 예측한다.
2. **T1-2** 두 observation 중 mean에 Mahalanobis 기준으로 더 가까운 쪽을 예측한다.
3. **T1-3** 더 높은 log-density를 갖는 observation을 예측한다.
4. **T1-4** `slogdet` sign을 예측한다.
### T2. 손계산
1. **T2-1** 두 residual vector를 구한다.
2. **T2-2** 각 `Sigma z=r`을 풀어 `z`를 구한다.
3. **T2-3** 두 Mahalanobis squared `q`를 구한다.
4. **T2-4** determinant, sign, logabsdet를 구한다.
5. **T2-5** 두 log-density를 구해 순서를 비교한다.
### T3. 직접 구현
1. **T3-1** `mahalanobis_squared(x, mean, covariance) -> float`를 `solve`로 완성한다.
2. **T3-2** `multivariate_gaussian_logpdf(observations, mean, covariance) -> (N,) float64`를
   `solve`/`slogdet`로 완성한다.
계약: observations `(N,D)`, mean `(D,)`, covariance `(D,D)`는 `float64`, `N,D>=1`,
covariance는 SPD다. `np.linalg.inv`, `np.linalg.det`는 사용하지 않는다.
부동소수 비교 허용오차는 `rtol=1e-7`, `atol=1e-12`다.
### T4. 표준 API 참조 (선택)

T4 답안이나 검산 코드는 작성하지 않아도 된다. T1–T3 후 `standard_api.py`를
읽어 `solve`, `slogdet`, `scipy.stats.multivariate_normal.logpdf` 표현을 참조한다.
solve, Mahalanobis reduction, slogdet, Gaussian logpdf의 표준 표현이 파일에
제공된다.
### T5. 잘못된 해석
1. **T5-1** `residual/covariance`로 선형계를 대체할 수 없는 이유를 설명한다.
2. **T5-2** batch `residual*solution`을 `axis=0`으로 합했을 때 shape/의미 오류를 설명한다.
3. **T5-3** 이 작은 예에서 inverse/determinant 값이 같더라도 수치 계약을 따라야 하는 이유를 설명한다.
### T6. 설명 확인
1. **T6-1** residual→solve→quadratic pipeline을 shape과 함께 설명한다.
2. **T6-2** Mahalanobis와 Euclidean distance의 차이를 covariance 관점에서 설명한다.
3. **T6-3** `solve`/`slogdet`를 쓰는 이유와 logpdf의 세 항을 설명한다.

## 검산
```bash
cd week3-machine-learning/curriculum/sessions/S10
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python standard_api.py  # 선택
../../../../.venv/bin/python -m unittest -v test_contract.py
```
## 제출물
`answers.md`, 완성한 `starter.py`, 통과한 계약 테스트.
## 완료 기준
T1–T3과 T5–T6을 설명하고 inverse 없이 batched log-density를 계산한다.
T4는 선택 참조다.
## 선택 확장
다른 SPD covariance와 batch size 1에서 shape `(1,)`를 유지하는지 확인한다.
