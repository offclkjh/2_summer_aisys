# S09 — Vector와 covariance
> 상태: `ready`. 실행 전 예측을 먼저 기록한다.

## 목표와 비목표
- 목표: 2D data를 center하고 outer product로 covariance matrix를 만든다.
- 목표: covariance의 각 원소와 `A Sigma A.T` 변환을 설명한다.
- 비목표: eigendecomposition, whitening, unbiased covariance.

## 시작 전 선수지식 확인
1. shape `(N,D)`에서 행과 열은 각각 무엇을 세는가?
2. feature별 mean을 구할 NumPy axis는 무엇인가?
3. scalar covariance의 부호는 두 편차의 어떤 관계를 나타내는가?

막히면 [vector/matrix 복습](../../concepts/vector_matrix.md),
[S03 covariance](../S03/PROBLEM.md#사용할-정의),
[S02 axis](../S02/PROBLEM.md#배열의-축)를 복습한다.

## 교재 연결
- Kevin P. Murphy, *MLAPP* (2012), Ch.4 multivariate moments and covariance geometry.

## 문제에서 주어진 정보
```python
data = np.array([[1., 1.], [2., 3.], [3., 2.]], dtype=np.float64) # (N=3,D=2)
A = np.array([[1., 1.]], dtype=np.float64)                       # (M=1,D=2)
```
행은 observation, 열은 feature다.

## 사용할 정의
```text
mean = data.mean(axis=0)                    shape (D,)
R = data - mean                            shape (N,D)
outer(r) = r r^T                           shape (D,D)
Sigma = R^T R / N                          shape (D,D)
y = A x,  Sigma_y = A Sigma A^T            shape (M,M)
batched transformed = data @ A.T           shape (N,M)
```
구현에서 `np.outer(v, v)`는 vector `v`의 outer product를 반환한다.
이 세션은 경험분포에 동일 가중치 `1/N`을 주는 covariance만 다룬다.
대각은 feature variance, 비대각은 feature 사이 covariance이며 Sigma는 대칭이다.

## 과제
### T1. 실행 전 예측
1. **T1-1** mean, centered data, outer product, covariance의 shape을 예측한다.
2. **T1-2** off-diagonal covariance의 부호를 예측한다.
3. **T1-3** transformed covariance의 shape을 예측한다.
### T2. 손계산
1. **T2-1** mean vector와 세 centered row를 구한다.
2. **T2-2** 세 outer product와 그 합을 구한다.
3. **T2-3** `1/N` covariance matrix를 구한다.
4. **T2-4** 대각/비대각 원소를 해석한다.
5. **T2-5** transformed values의 variance와 `A Sigma A.T`를 구해 비교한다.
### T3. 직접 구현
1. **T3-1** `center_data(data) -> (mean, centered)`를 완성한다.
2. **T3-2** `outer_product(vector) -> (D,D) float64`를 완성한다.
3. **T3-3** `covariance_matrix_mle(data) -> (D,D) float64`를 완성한다.
4. **T3-4** `transform_covariance(matrix, covariance) -> (M,M) float64`를 완성한다.
계약: data는 nonempty 2D `float64`, vector는 `(D,)`, matrix는 `(M,D)`다.
부동소수 비교 허용오차는 `rtol=1e-7`, `atol=1e-12`다.
### T4. 검산
1. **T4-1** centered 열평균이 0인지 확인한다.
2. **T4-2** outer 합과 `R.T @ R`을 비교한다.
3. **T4-3** covariance가 대칭이고 대각이 직접 구한 variance와 같은지 확인한다.
4. **T4-4** transformed data의 covariance와 `A Sigma A.T`를 비교한다.
### T5. 잘못된 해석
1. **T5-1** `R @ R.T`를 쓰면 shape과 의미가 어떻게 바뀌는지 설명한다.
2. **T5-2** 분모 `N-1`을 쓰면 이 세션과 다른 어떤 통계량인지 설명한다.
3. **T5-3** `A Sigma A` 처럼 transpose를 누락한 식의 shape/의미 문제를 설명한다.
### T6. 설명 확인
1. **T6-1** covariance matrix의 대각과 비대각을 설명한다.
2. **T6-2** off-diagonal 부호가 두 feature의 co-movement를 어떻게 나타내는지 설명한다.
3. **T6-3** `A Sigma A.T` 규칙을 shape과 함께 설명한다.

## 검산
```bash
cd week3-machine-learning/curriculum/sessions/S09
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```
## 제출물
`answers.md`, 완성한 `starter.py`, 통과한 계약 테스트.
## 완료 기준
T1–T6을 설명하고 covariance와 linear transform을 shape·수치·의미로 연결한다.
## 선택 확장
shape `(2,2)`인 transform으로 같은 규칙을 검산한다.
