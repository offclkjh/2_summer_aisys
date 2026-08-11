# Phase A — 연구를 위한 누적 학습 노트

세션에서 새로 배운 내용 중 연구 코드에 다시 사용할 지식을 누적한다. 각 세션은
**라이브러리 기능**, **문법·구현 개선**, **MLAPP 코어** 세 부분으로 정리한다.
단순 실수나 일회성 오류 메시지는 기록하지 않는다.

우선순위 표시는 다음과 같다.

- **필수**: 검색 없이 읽고 쓸 정도로 익힌다.
- **익숙**: 의미를 알고 반복 사용하면서 익힌다.
- **참조**: 존재와 용도를 알고 필요할 때 문서를 찾는다.

## S01 — 확률모형의 객체와 shape

### 1. 새로운 라이브러리와 기능

| 우선순위 | 종류 | 표현 | 역할 |
|---|---|---|---|
| 필수 | NumPy 함수 | `np.array(data, dtype=...)` | Python 데이터를 NumPy 배열로 만든다. |
| 필수 | NumPy 클래스 | `np.ndarray` | NumPy 배열 객체의 타입이다. `isinstance` 검사에 사용한다. |
| 필수 | 인스턴스 속성 | `x.shape` | 각 축의 길이를 tuple로 나타낸다. |
| 필수 | 인스턴스 속성 | `x.ndim` | 배열의 축 개수를 나타낸다. |
| 필수 | 인스턴스 속성 | `x.size` | 모든 축을 합친 전체 원소 수를 나타낸다. |
| 필수 | 인스턴스 속성 | `x.dtype` | 배열 원소의 저장 자료형을 나타낸다. |
| 필수 | indexing | `x[i]` | 배열에서 `i`번째 관측 또는 부분 배열을 꺼낸다. |
| 익숙 | Python 함수 | `isinstance(x, np.ndarray)` | 객체가 NumPy 배열 타입인지 확인한다. |
| 익숙 | NumPy 함수 | `np.issubdtype(x.dtype, np.integer)` | dtype이 특정 개별 타입이 아니라 정수 계열인지 확인한다. |
| 익숙 | NumPy 함수 | `np.all(condition)` | Boolean 배열의 모든 원소가 참인지 확인한다. |
| 익숙 | NumPy 타입 계열 | `np.integer` | `int32`, `int64` 등을 포함하는 NumPy 정수 계열을 나타낸다. |

구조를 비교할 때 기억할 예:

```python
np.array(1).shape       # ()     : 0차원 배열
np.array([1]).shape     # (1,)   : 길이 1인 1차원 배열
np.array([[1]]).shape   # (1, 1) : 두 축을 가진 2차원 배열
np.array([]).shape      # (0,)   : 비어 있는 1차원 배열
```

### 2. 문법·구현 개선안

- 축의 개수를 표현할 때 `len(x.shape)`보다 의도가 직접 드러나는 `x.ndim`을
  우선한다.
- 전체 원소 수가 목적이면 `x.size`, 첫 번째 축의 길이가 목적이면
  `x.shape[0]` 또는 `len(x)`을 사용한다.
- dtype 하나씩 비교하지 않고 타입 계열을 계약으로 검사한다.

  ```python
  np.issubdtype(x.dtype, np.integer)
  ```

- 원소별 Python 반복보다 배열 조건과 reduction이 의도를 더 잘 표현할 때는
  vectorized NumPy 연산을 사용한다.

  ```python
  np.all((x == 0) | (x == 1))
  ```

- 정보를 반환하기 전에 입력 계약을 검증하는 설계는 유효하다. 반복 검증 비용이
  실제 병목으로 확인되기 전에는 안전성과 명확성을 우선한다.

### 3. MLAPP 코어

1. **관측 전체, 관측 하나, 파라미터를 구분한다.**
   - `D`: 관측 데이터 전체
   - `x_i`: `D`에 포함된 관측 하나
   - `theta`: 데이터를 생성하는 모형의 알려지지 않은 파라미터

2. **파라미터와 추정량을 구분한다.**
   `theta`는 알려지지 않은 대상이고, 관측 비율 `3/4`은 이 사례에서 얻은
   frequentist MLE이다. 추정값을 실제 파라미터와 동일시하지 않는다.

3. **shape를 데이터 의미로 읽는다.**
   `D.shape == (4,)`는 단순히 숫자 4가 아니라, 관측을 세는 축 하나에 관측이
   네 개 있다는 뜻이다. 각 축이 무엇을 세는지 설명할 수 있어야 한다.

4. **입력 validation은 데이터 계약의 실행 가능한 표현이다.**
   객체 종류, shape, 비어 있음, dtype, 허용 값은 함수가 어떤 데이터를 의미
   있는 입력으로 인정하는지를 정의한다.

## S03 — 기대값·분산·공분산

### 1. 새로운 라이브러리와 기능

| 우선순위 | 종류 | 표현 | 역할 |
|---|---|---|---|
| 필수 | NumPy 함수 | `np.sum(x)` | 배열 원소를 합하며, 원소별 곱과 결합해 유한 가중합을 표현한다. |
| 익숙 | Python 함수 | `float(x)` | NumPy scalar 등을 Python `float` 반환 계약에 맞게 변환한다. |

### 2. 문법·구현 개선안

- 수식의 유한합은 원소별 연산과 `np.sum`을 조합해 직접 표현할 수 있다.

  ```python
  expectation = np.sum(probabilities * values)
  variance = np.sum(probabilities * (values - expectation) ** 2)
  ```

- 이론적 기대값과 공분산의 중심에는 모든 값에 같은 비중을 주는 단순평균이
  아니라 outcome의 발생확률을 반영한 확률가중평균을 사용한다.
- 단순평균과 가중평균이 우연히 같은 입력만으로는 잘못된 구현을 발견하지 못할
  수 있다. 불균등한 확률과 비대칭 값을 가진 다른 유효 입력으로도 검산한다.
- 반환 계약이 Python `float`이면 계산 결과를 반환할 때 명시적으로 변환한다.

  ```python
  return float(result)
  ```

## S04 — 정보량·entropy·cross-entropy·KL

### 1. 새로운 라이브러리와 기능

| 우선순위 | 종류 | 표현 | 역할 |
|---|---|---|---|
| 필수 | NumPy 함수 | `np.log2(x)` | base-2 logarithm을 원소별로 계산한다. 정보량의 단위는 bit가 된다. |
| 필수 | NumPy 함수 | `np.sum(x)` | 범주별 가중항을 합해 entropy, cross-entropy, KL을 계산한다. |
| 익숙 | NumPy 함수 | `np.isclose(a, b)` | 부동소수점 계산 결과와 관계식을 허용오차 안에서 비교한다. |

### 2. 문법·구현 개선안

- 정보이론 정의식은 원소별 정보량, 확률 가중, 합산으로 나누어 읽는다.

  ```python
  information = -np.log2(p)
  weighted_terms = p * information
  result = np.sum(weighted_terms)
  ```

- 계산할 때는 같은 구조를 한 줄의 NumPy 배열 연산으로 표현할 수 있다.
- 부동소수점 결과는 `==`보다 `np.isclose`로 비교한다.
- shape와 확률 합 validation은 배열이 유효한 분포인지는 확인하지만,
  `p`와 `q`의 의미상 역할이 뒤바뀐 오류까지 확인하지는 못한다.

### 3. MLAPP 코어

1. **Self-information은 드문 결과일수록 크다.**

   \[
   I_p(i)=-\log_2p_i
   \]

   코드 길이 관점에서는 자주 발생하는 결과에 짧은 코드를, 드문 결과에 긴
   코드를 배정한다. Entropy는 이 이상적인 코드 길이의 확률가중평균이다.

2. **세 양은 모두 source distribution `p`로 평균낸다.**

   \[
   H(p)=E_p[-\log_2p_i]
   \]

   \[
   H(p,q)=E_p[-\log_2q_i]
   \]

   \[
   KL(p\|q)=E_p\left[\log_2\frac{p_i}{q_i}\right]
   \]

   `p`는 실제 발생확률과 평균의 가중치를 정하고, `q`는 모델이 부여한 정보량을
   정한다.

3. **Cross-entropy는 entropy와 추가 비용으로 분해된다.**

   \[
   H(p,q)=H(p)+KL(p\|q)
   \]

   모델 `q`가 source `p`와 다를 때 KL만큼의 평균 정보량이 추가된다.

4. **KL의 방향은 중요하다.**

   `KL(p || q)`는 `p`로 평균내고 `KL(q || p)`는 `q`로 평균낸다. 첫 번째
   인수가 기대값의 기준을 정하므로 일반적으로 두 값은 다르다.

5. **균등분포는 유한한 범주에서 entropy를 최대화한다.**

   균등분포 `u`에 대해

   \[
   KL(p\|u)=-H(p)+\log_2|\mathcal X|\geq0
   \]

   이므로 \(H(p)\leq\log_2|\mathcal X|\)이고, 등호는 `p`가 균등분포일 때 성립한다.

6. **MLE와 KL은 같은 최적화 문제로 연결된다.**

   경험분포를 \(\hat p\), 모델을 \(q_\theta\)라 하면

   \[
   KL(\hat p\|q_\theta)=H(\hat p,q_\theta)-H(\hat p)
   \]

   이다. \(H(\hat p)\)는 파라미터와 무관한 상수이므로 MLE, 평균 NLL 최소화,
   경험분포에 대한 cross-entropy 최소화, KL 최소화는 같은 최적해를 갖는다.

## Phase A 완료 시 연결

1. 확률분포는 음이 아닌 값들의 배열이며 전체 확률 합은 1이다.
2. `np.sum`의 축은 어떤 확률변수를 제거하거나 어떤 outcome을 평균내는지 나타낸다.
3. 기대값, 분산, entropy는 모두 outcome별 값을 확률로 가중한 유한합이다.
4. shape와 수치 조건이 같아도 source, model, 관측, 파라미터의 의미는 서로 다르다.
5. 정보이론의 cross-entropy와 KL은 이후 likelihood와 MLE를 loss 관점으로 연결하는
   기반이 된다.
