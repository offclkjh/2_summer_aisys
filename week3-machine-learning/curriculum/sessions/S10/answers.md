# S10 답안

## Core

### T1. 실행 전 예측

- **T1-1** residuals/solutions/Mahalanobis/logpdf shape:
- **T1-2** 더 가까운 observation과 근거:
- **T1-3** 더 높은 log-density와 근거:
- **T1-4** `slogdet` sign과 SPD 근거:

### T2. 유도 재구성

- **T2-1** affine transform/change of variables:
- **T2-2** quadratic form/determinant 연결:
- **T2-3** SPD가 보장하는 성질과 사용처:

### T3. 2D 손계산

- **T3-1** residuals:
- **T3-2** linear-system solutions:
- **T3-3** Mahalanobis squared:
- **T3-4** determinant/sign/logabsdet:
- **T3-5** log-density/order와 예측 비교:

### T4. 직접 구현

- **T4-1** `mahalanobis_squared`:
- **T4-2** `multivariate_gaussian_logpdf`:

### T5. 수치해석과 실패 해석

- **T5-1** elementwise division과 linear solve:
- **T5-2** wrong reduction axis:
- **T5-3** inverse와 solve:
- **T5-4** `log(det(...))`와 `slogdet`:

### T6. 통합 설명

- **T6-1** affine transform부터 log-density까지:
- **T6-2** Euclidean/Mahalanobis와 covariance ellipse:
- **T6-3** batch pipeline과 shape:

## Deep dive (선택)

### D1. Eigendecomposition과 주축

- eigenpairs:
- principal coordinates에서의 quadratic form:
- 타원의 방향과 축 길이 비:

### D2. Cholesky와 whitening

- factorization 검산:
- whitened norm과 Mahalanobis:
- Cholesky log-determinant:

### D3. Conditioning 실험

- 실행 전 예측:
- 관찰:
- mathematical SPD와 numerical reliability:

### D4. Covariance scale과 정규화

- Mahalanobis 항 변화:
- log-determinant 항 변화:
- 위치에 따른 log-density 변화:
