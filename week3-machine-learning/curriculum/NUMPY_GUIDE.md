# NumPy 핵심 연산 가이드

이 문서는 특정 세션의 정답이 아니라, 전체 커리큘럼과 연구 코드에서 반복해
사용할 NumPy 연산의 참조표다. 프로젝트 작성 기준은 NumPy 2.x이며,
현재 가상환경에서 확인한 버전은 2.4.4다.

## 1. 가장 먼저 확인할 것

배열 연산을 읽거나 쓸 때는 다음 네 가지를 먼저 확인한다.

```python
x.shape  # 각 축의 길이
x.ndim   # 축의 개수
x.size   # 전체 원소 수
x.dtype  # 저장 자료형
```

shape는 숫자만이 아니라 데이터의 의미로 읽는다.

```text
(N,)       N개의 scalar 관측
(N, D)     N개 관측, 관측당 D개 feature
(K, D)     K개 component/class, component당 D개 parameter
(N, K)     N개 관측에 대한 K개 score/probability
(D, D)     D차원 정사각행렬
```

핵심 규칙:

1. 각 axis가 무엇을 세는지 먼저 이름 붙인다.
2. 연산 전·후 shape를 예측한다.
3. 확률, count, label, feature의 dtype을 구분한다.
4. 작은 예시로 값과 shape를 검산한다.

## 2. 배열 생성과 dtype

```python
import numpy as np

x = np.array([1, 2, 3], dtype=np.float64)
zeros = np.zeros((2, 3), dtype=np.float64)
ones = np.ones((2, 3), dtype=np.float64)
filled = np.full((2, 3), 7.0)
identity = np.eye(3, dtype=np.float64)
integers = np.arange(0, 10, 2)
grid = np.linspace(0.0, 1.0, num=6)
same_shape = np.zeros_like(x)
```

자주 쓰는 dtype:

| 용도 | 권장 dtype | 예 |
|---|---|---|
| 확률, 파라미터, 특징 | `np.float64` | likelihood, covariance |
| label, count, index | `np.int64` | class label, 빈도 |
| 조건 mask | `np.bool_` | `x > 0` |

변환은 `astype`을 사용한다.

```python
x_float = x.astype(np.float64)
```

`astype`은 보통 새 배열을 만든다. float를 int로 바꾸면 소수 부분이 잘릴 수
있으므로 의도를 명확히 한다.

## 3. Indexing, slicing, mask

```python
x = np.array([[10, 11, 12], [20, 21, 22]])

x[1, 2]      # 행 1, 열 2의 scalar
x[0]         # 첫 행, shape (3,)
x[:, 1]      # 모든 행의 열 1, shape (2,)
x[0:2, 1:3]  # slicing, shape (2, 2)
x[-1]        # 마지막 행
```

조건을 만족하는 원소를 고를 때는 Boolean mask를 사용한다.

```python
mask = x > 15
selected = x[mask]
valid = x[(x >= 10) & (x < 20)]
```

NumPy 배열 조건은 Python의 `and`, `or`, `not` 대신 `&`, `|`, `~`를 쓰고
각 조건을 괄호로 감싼다.

원본을 변경하지 않으려면 copy 여부를 확인한다.

```python
view = x[:, 1]       # 원본과 메모리를 공유할 수 있음
independent = x.copy()
```

## 4. Shape 변환과 축 추가

```python
x = np.arange(6)
matrix = x.reshape(2, 3)
flat = matrix.reshape(-1)  # 또는 matrix.ravel()
transposed = matrix.T
```

`reshape`는 원소 수를 바꾸지 않는다. `-1`은 나머지 shape로부터 길이를
추론하라는 뜻이다.

```python
v = np.array([1.0, 2.0, 3.0])  # (3,)
column = v[:, None]             # (3, 1)
row = v[None, :]                # (1, 3)

# 같은 의미의 명시적 표현
column = np.expand_dims(v, axis=1)
```

길이 1인 축을 제거할 때는 `np.squeeze`를 사용한다. 의도하지 않은 축까지
제거하지 않도록 가능하면 `axis`를 지정한다.

```python
restored = np.squeeze(column, axis=1)
```

## 5. 결합과 분할

```python
a = np.ones((2, 3))
b = np.zeros((2, 3))

rows = np.concatenate([a, b], axis=0)  # (4, 3)
cols = np.concatenate([a, b], axis=1)  # (2, 6)
stacked = np.stack([a, b], axis=0)      # (2, 2, 3), 새 축 추가
```

- `concatenate`: 기존 axis를 이어 붙인다.
- `stack`: 새 axis를 만든다.

`np.split`, `np.array_split`은 배열을 여러 부분으로 나눈다. 같은 크기로
나누어지지 않을 수 있으면 `array_split`을 사용한다.

## 6. Vectorized 산술과 비교

기본 산술은 원소별로 적용된다.

```python
x + y
x - y
x * y       # 원소별 곱셈
x / y       # 원소별 나눗셈
x ** 2
np.sqrt(x)
np.abs(x)
np.exp(x)
np.log(x)
```

비교도 원소별 Boolean 배열을 만든다.

```python
x == y
x > 0
np.isclose(x, y)
np.allclose(x, y)
```

float은 반올림 오차가 있으므로 보통 `==`보다 `isclose`/`allclose`로 비교한다.

조건에 따라 값을 고를 때는 `where`를 사용한다.

```python
clipped_sign = np.where(x >= 0, 1.0, -1.0)
```

## 7. Reduction과 axis

reduction은 여러 원소를 하나 또는 더 작은 배열로 요약한다.

```python
x.sum()
x.mean()
x.var()
x.std()
x.min()
x.max()
x.argmin()
x.argmax()
np.prod(x)
np.any(condition)
np.all(condition)
```

`axis=k`는 **k번 축을 따라 연산하고 그 축을 제거**한다.

```python
x = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)

x.sum(axis=0).shape  # (3,), axis 0이 제거됨
x.sum(axis=1).shape  # (2,), axis 1이 제거됨
```

축을 길이 1로 남겨 broadcasting에 재사용하려면 `keepdims=True`를 쓴다.

```python
row_sums = x.sum(axis=1, keepdims=True)  # (2, 1)
normalized = x / row_sums
```

여러 축을 한번에 제거할 수도 있다.

```python
x.sum(axis=(0, 2))
```

## 8. Broadcasting

NumPy는 뒤쪽 axis부터 shape를 비교한다. 각 위치의 길이가 같거나 둘 중 하나가
1이면 확장해 연산할 수 있다.

```python
matrix = np.ones((4, 3))
feature_offset = np.array([10.0, 20.0, 30.0])  # (3,)
shifted = matrix + feature_offset               # (4, 3)
```

관측별 scalar를 각 행에 적용하려면 column shape로 만든다.

```python
scale = np.arange(4.0)[:, None]  # (4, 1)
scaled = matrix * scale          # (4, 3)
```

주의: shape가 연산 가능하다고 의미까지 맞는 것은 아니다. 결과 shape를 예측하고
각 axis의 의미를 확인한다.

## 9. 정렬, index, unique, count

```python
sorted_values = np.sort(x)
order = np.argsort(x)
unique_values = np.unique(x)
values, counts = np.unique(x, return_counts=True)
```

class label이 0부터 시작하는 음이 아닌 정수일 때 count는 `bincount`로 빠르게 구할
수 있다.

```python
counts = np.bincount(labels, minlength=num_classes)
```

`argmax` 결과로 최대 score의 index를 얻는다.

```python
predicted_class = scores.argmax(axis=1)
```

## 10. 기술통계와 가중 연산

```python
mean = np.mean(x, axis=0)
variance_population = np.var(x, axis=0, ddof=0)
variance_unbiased = np.var(x, axis=0, ddof=1)
standard_deviation = np.std(x, axis=0, ddof=1)
quantiles = np.quantile(x, [0.25, 0.5, 0.75], axis=0)
```

- `ddof=0`: 분모 `n`, 분포 또는 주어진 데이터 자체의 분산에 주로 사용
- `ddof=1`: 분모 `n-1`, 불편 표본분산에 주로 사용

가중평균:

```python
weighted_mean = np.average(values, weights=weights)
```

공분산 행렬:

```python
# rows: 관측, columns: 변수
covariance = np.cov(data, rowvar=False, ddof=1)
```

`np.cov`의 기본 `rowvar=True`는 행을 변수로 해석한다. 일반적인 `(N, D)` 데이터에서는
`rowvar=False`를 명시하는 편이 안전하다.

## 11. 선형대수

### 원소별 곱과 행렬 곱의 구분

```python
a * b   # 원소별 곱
a @ b   # 행렬 곱
np.matmul(a, b)
```

주요 연산:

```python
dot = x @ y
outer = np.outer(x, y)
transpose = matrix.T
diagonal = np.diag(matrix)
trace = np.trace(matrix)
norm = np.linalg.norm(x)
```

선형방정식 `A x = b`는 inverse를 직접 곱하지 말고 `solve`로 푼다.

```python
solution = np.linalg.solve(A, b)
```

최소제곱:

```python
coef, residuals, rank, singular_values = np.linalg.lstsq(X, y, rcond=None)
```

그 외 주요 도구:

```python
eigenvalues, eigenvectors = np.linalg.eigh(symmetric_matrix)
singular_values = np.linalg.svdvals(matrix)
condition_number = np.linalg.cond(matrix)
sign, log_abs_det = np.linalg.slogdet(matrix)
```

- 대칭행렬은 가능하면 `eig`보다 `eigh`를 사용한다.
- determinant 자체보다 log determinant가 필요하면 `det` 후 `log`를 취하지 말고
  `slogdet`를 사용한다.
- `np.linalg.inv(A) @ b`보다 `np.linalg.solve(A, b)`가 의도가 명확하고 일반적으로
  더 안정적이다.

## 12. 난수와 재현성

새 코드에서는 legacy 전역 난수 함수보다 `Generator`를 사용한다.

```python
rng = np.random.default_rng(seed=42)

uniform = rng.uniform(0.0, 1.0, size=100)
normal = rng.normal(loc=0.0, scale=1.0, size=(100, 3))
integers = rng.integers(0, 10, size=20)
sample = rng.choice(values, size=50, replace=True, p=probabilities)
permutation = rng.permutation(len(data))
```

- 테스트와 재현 실험은 seed를 명시한다.
- 실제 임의성이 필요한 실행은 seed를 고정하지 않을 수 있다.
- 함수 내부에서 매번 같은 seed로 generator를 새로 만들지 않는다. 필요하면
  `rng` 객체를 인자로 받는다.

## 13. 수치 안정성

### 로그와 0

```python
tiny = np.finfo(np.float64).tiny
safe_log = np.log(np.clip(probabilities, tiny, None))
```

`clip`으로 문제를 숨기기 전에 0이 수학적으로 허용되는지, smoothing이 모형의
일부인지 먼저 확인한다.

### log-sum-exp

큰 log value의 exponential overflow를 피하려면 최대값을 빼고 계산한다.

```python
m = np.max(log_values, axis=axis, keepdims=True)
log_total = m + np.log(np.sum(np.exp(log_values - m), axis=axis, keepdims=True))
```

실전에서는 SciPy의 `scipy.special.logsumexp`를 우선하고, NumPy 직접 구현은 정의와
shape를 학습할 때 사용한다.

### NaN과 infinity 확인

```python
np.isnan(x)
np.isinf(x)
np.isfinite(x)
np.all(np.isfinite(x))
```

경고를 무작정 숨기지 말고 원인을 확인한다. 필요한 구간에서만 부동소수점
오류 처리 규칙을 바꾼다.

```python
with np.errstate(divide="raise", invalid="raise", over="raise"):
    result = risky_operation(x)
```

## 14. 확률 구현에 자주 쓰는 패턴

### 빈도를 확률로 정규화

```python
probabilities = counts / counts.sum()
```

### 특정 axis를 따라 정규화

```python
normalizer = values.sum(axis=axis, keepdims=True)
normalized = values / normalizer
```

나누기 전에 normalizer가 0일 수 있는지 확인한다.

### 가중합과 기대값

```python
expectation = np.sum(probabilities * values)
```

### 행별 score의 최댓값

```python
prediction = scores.argmax(axis=1)
```

### one-hot encoding

```python
one_hot = np.eye(num_classes, dtype=np.float64)[labels]
```

### train/validation index 분할

```python
indices = rng.permutation(len(data))
train_idx = indices[:split]
valid_idx = indices[split:]
```

데이터와 label에 **같은 index**를 사용해 쌍을 보존한다.

## 15. 입력 계약과 검증

연구 코드에서 shape 오류를 초기에 드러내려면 함수 경계에서 의미 있는 계약을
검사한다.

```python
def validate_features(x: np.ndarray) -> None:
    if not isinstance(x, np.ndarray):
        raise TypeError("x must be a NumPy array")
    if x.ndim != 2:
        raise ValueError("x must have shape (N, D)")
    if x.shape[0] == 0:
        raise ValueError("x must contain at least one observation")
    if not np.issubdtype(x.dtype, np.floating):
        raise TypeError("x must have a floating dtype")
    if not np.all(np.isfinite(x)):
        raise ValueError("x must contain only finite values")
```

전체 설명이 잘못된 `assert` 대신 적절한 `TypeError`/`ValueError`를 사용한다. 단,
성능 핵심 내부 함수에서 같은 검증을 반복하기보다 외부 API 경계에서 한 번
검증하는 설계를 고려한다.

## 16. 테스트와 디버깅

```python
np.testing.assert_array_equal(actual, expected)       # 정확한 일치
np.testing.assert_allclose(actual, expected)          # 부동소수점 근사 일치
np.testing.assert_equal(actual.shape, expected_shape)
```

중간 shape를 짧게 확인한다.

```python
print("x:", x.shape, x.dtype)
print("scores:", scores.shape)
```

연구 코드에 임시 print를 남기기보다 debugger나 logging으로 전환한다. 실패한 때는
다음 순서로 확인한다.

1. type, shape, dtype
2. axis의 의미
3. NaN/inf과 0으로 나눗셈
4. 원소별 곱 `*`과 행렬 곱 `@`의 혼동
5. broadcasting으로 우연히 통과한 shape
6. 표본 통계의 `ddof`
7. 원본 배열의 의도하지 않은 변경

## 17. 성능 원칙

- Python loop를 무조건 없애지 말고, 먼저 정답과 명확성을 확보한다.
- 단순 원소별 연산과 reduction은 vectorization을 우선한다.
- 큰 임시 배열을 만드는 broadcasting은 메모리 사용량을 확인한다.
- 성능을 추측하지 말고 실제 입력 크기로 측정한다.
- 불필요한 copy를 피하되, view로 인한 원본 변경 버그를 조심한다.

## 18. 우선순위 빠른 참조표

### 필수 — 검색 없이 쓸 수 있게

| 목적 | 표현 |
|---|---|
| 배열 생성 | `np.array`, `np.zeros`, `np.ones` |
| 구조 확인 | `shape`, `ndim`, `size`, `dtype` |
| 선택 | `x[i]`, `x[:, j]`, Boolean mask |
| shape 변환 | `reshape`, `.T`, `None`/`newaxis` |
| 기본 요약 | `sum`, `mean`, `min`, `max`, `argmax` |
| 배열 산술 | `+`, `-`, `*`, `/`, `**` |
| 행렬 곱 | `@` |
| float 비교 | `isclose`, `allclose` |
| 유효성 | `isfinite`, `issubdtype` |

### 익숙 — 반복 사용하며 익히기

| 목적 | 표현 |
|---|---|
| 축 보존 요약 | `keepdims=True` |
| 조건부 선택 | `where`, `clip` |
| 결합 | `concatenate`, `stack` |
| 기술통계 | `var`, `std`, `quantile`, `cov` |
| 가중 평균 | `average(..., weights=...)` |
| 난수 | `default_rng`, `choice`, `permutation` |
| 선형방정식 | `linalg.solve`, `linalg.lstsq` |
| 행렬 진단 | `linalg.norm`, `cond`, `slogdet` |

### 참조 — 필요할 때 찾아 쓰기

`einsum`, `take_along_axis`, `searchsorted`, `histogram`, `meshgrid`, `einsum_path`,
`memmap` 등은 필요한 세션이나 성능 문제가 생겼을 때 별도로 학습한다.
참조 항목을 외우는 것보다 기본 axis·shape·broadcasting을 정확히 이해하는 것이
우선이다.
