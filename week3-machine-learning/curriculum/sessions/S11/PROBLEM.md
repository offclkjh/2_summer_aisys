# S11 — Gaussian conditioning과 marginalization

> 상태: `draft`. 실제 튜터 풀이로 검수한 뒤에만 `ready`로 승격한다.
> Core는 120분 이내이며, 실행 전 예측을 먼저 기록한다.

## 목표와 비목표

### Core (120분 이내)

- joint Gaussian의 mean과 covariance를 target/observed block으로 나눈다.
- marginal distribution이 원래 mean·covariance의 부분 블록으로 정해지는 이유를
  설명한다.
- 관측값이 주어졌을 때 conditional mean과 covariance를 손으로 계산한다.
- block slicing과 `solve`를 사용해 여러 차원에도 적용되는 함수를 구현한다.
- marginal과 conditional에서 무엇을 버리고 무엇을 고정하는지 구분한다.

### 선택 확장

- joint Gaussian의 quadratic form에서 conditional 공식을 guided derivation한다.
- Ch. 5의 parameter posterior와 이번 장의 random-variable conditioning을 객체
  수준에서 비교한다.
- Schur complement와 conditional covariance의 positive definiteness를 연결한다.

Kalman filter, missing-data dataset, singular covariance, 일반적인 Gaussian graphical
model은 이번 세션의 범위가 아니다.

## 시작 전 선수지식 확인

이 세션은 joint·marginal·conditional의 뜻, 다변량 Gaussian, 선형계 계산을
사용한다. 현재 계산에 필요한 정의는 다음과 같다.

- **Marginal:** 관심 없는 변수를 적분해 없앤 분포다.
- **Conditional:** 일부 변수의 관측값을 고정한 뒤 나머지 변수에 대한 분포다.
- **Block covariance:** 변수 순서를 두 묶음으로 나누어 covariance의 행과 열을
  같은 순서로 선택한 부분행렬이다.
- **Linear solve:** $Az=b$에서 $A^{-1}$를 만들지 않고 필요한 해를 구하는
  계산이다. NumPy에서는 `np.linalg.solve(A, b)`를 사용한다.

복습 위치:

- [S02 joint·marginal·conditional](../S02/PROBLEM.md#사용할-정의)
- [S10 multivariate Gaussian](../S10/PROBLEM.md#사용할-정의)
- [linear system 카드](../../concepts/linear_system.md)

진단할 때는 다음을 자신의 말과 shape으로 설명한다.

1. $p(x_t)$와 $p(x_t\mid x_o)$는 어떤 정보를 다르게 사용하는가?
2. `A`가 `(O,O)`, `b`가 `(O,)`일 때 `np.linalg.solve(A, b)`의 결과 shape은?
3. covariance에서 target 행과 observed 열을 선택한 block의 shape은?

새로 발견된 선수지식 공백은 오답으로 채점하지 않는다. 위 정의와 복습 자료로
guided teaching한 뒤 Core로 돌아온다.

## 교재 연결

- 정렬 상태: `inferred`
- 확인 근거: 저장소의 진도표와 커리큘럼 계약은 MLAPP Ch. 4의 Gaussian
  marginals/conditionals를 지목하지만, 원문·공식 발췌·상세 절 번호는 저장소에
  없다.
- 판본: Kevin P. Murphy, *Machine Learning: A Probabilistic Perspective* (2012)
- 주제명: Gaussian marginals and conditionals
- 이 세션에서 읽을 범위: 정확한 절 순서를 재현하지 않고
  `MLAPP-style probabilistic depth`로 block Gaussian 계산을 다룬다.
- 문제를 푸는 데 필요한 식은 아래에 모두 제공한다. 확인하지 못한 원문 유도는
  Core 회상·채점 대상으로 삼지 않는다.

상위 진도표에는 Ch. 5까지 읽었다고 기록되어 있지만, 이번 Core는 S02와 S10에서
확인된 개념만 요구한다. Ch. 5와의 연결은 선택 확장에서 다룬다.

## 모델과 가정

하나의 random vector를 target $x_t$와 observed $x_o$로 나눈다.

$$
\begin{bmatrix}x_t\\x_o\end{bmatrix}
\sim
\mathcal N\!\left(
\begin{bmatrix}\mu_t\\\mu_o\end{bmatrix},
\begin{bmatrix}
\Sigma_{tt} & \Sigma_{to}\\
\Sigma_{ot} & \Sigma_{oo}
\end{bmatrix}
\right).
$$

$\Sigma$는 symmetric positive definite이고 target index와 observed index는 서로
겹치지 않는다고 가정한다. 따라서 $\Sigma_{oo}$에 대한 linear solve가 가능하다.
변수 순서는 index 배열에 적힌 순서를 그대로 따른다.

## 문제에서 주어진 정보

하나의 2D sensor vector에서 첫 번째 변수를 target, 두 번째 변수를 observed로
사용한다.

```python
mean = np.array([1.0, 2.0], dtype=np.float64)                  # (D,)
covariance = np.array([[4.0, 2.0], [2.0, 2.0]], dtype=np.float64)  # (D,D)
target_indices = np.array([0], dtype=np.int64)                # (T,)
observed_indices = np.array([1], dtype=np.int64)              # (O,)
observed_values = np.array([4.0], dtype=np.float64)            # (O,)
```

이 수치는 T1의 예측, T2 손계산, T3 직접 구현에서 동일하게 사용한다. 구체적인
marginal·conditional 결과는 먼저 계산해 `answers.md`에 기록한 뒤 테스트로
확인한다.

구현 계약에서 입력은 다음을 만족한다.

- `mean`: `(D,)` `float64`
- `covariance`: `(D,D)` `float64` SPD
- `indices`: 서로 겹치지 않는 1D integer array이며 각 배열의 길이는 1 이상
- `observed_values`: `(O,)` `float64`
- 반환 mean은 `(K,)` 또는 `(T,)`, 반환 covariance는 `(K,K)` 또는 `(T,T)`인
  `float64`; 차원이 1이어도 matrix 축을 없애지 않는다.

## 사용할 정의

### 1. Gaussian marginal

joint Gaussian에서 index 묶음 $t$만 남긴 marginal은

$$
x_t\sim\mathcal N(\mu_t,\Sigma_{tt})
$$

이다. Mean에서는 해당 원소를, covariance에서는 해당 index의 행과 열을 모두
선택한다.

### 2. Gaussian conditional

$x_o$를 값 $v_o$로 관측했을 때

$$
x_t\mid x_o=v_o
\sim
\mathcal N(\mu_{t\mid o},\Sigma_{t\mid o})
$$

이며

$$
\mu_{t\mid o}
=\mu_t+\Sigma_{to}\Sigma_{oo}^{-1}(v_o-\mu_o),
$$

$$
\Sigma_{t\mid o}
=\Sigma_{tt}-\Sigma_{to}\Sigma_{oo}^{-1}\Sigma_{ot}.
$$

이 두 식은 Core에서 **주어진 정의**로 사용한다. 완전제곱 유도는 이전에 배웠다고
가정하지 않으며 선택 확장 D0에서 안내받아 진행한다.

### 3. Shape과 inverse 없는 계산 경로

| 객체 | Shape | 의미 |
|---|---:|---|
| `mu_t` | `(T,)` | target mean |
| `mu_o` | `(O,)` | observed mean |
| `sigma_tt` | `(T,T)` | target covariance block |
| `sigma_to` | `(T,O)` | target-observed cross block |
| `sigma_ot` | `(O,T)` | observed-target cross block |
| `sigma_oo` | `(O,O)` | observed covariance block |
| `delta_o` | `(O,)` | `observed_values - mu_o` |
| `solve(sigma_oo, delta_o)` | `(O,)` | conditional mean correction의 해 |
| `solve(sigma_oo, sigma_ot)` | `(O,T)` | conditional covariance correction의 해 |

```text
conditional_mean = mu_t + sigma_to @ solve(sigma_oo, delta_o)
conditional_covariance = sigma_tt - sigma_to @ solve(sigma_oo, sigma_ot)
```

수학식의 inverse 표기는 선형변환을 설명하지만 구현에서 inverse 행렬을 만들라는
뜻은 아니다.

## 구현 도구 구분

- **직접 구현:** index에 따른 mean/covariance block 구성, marginal 반환,
  conditional mean·covariance 계산 경로
- **사용 권장 API:** NumPy integer indexing, `np.ix_`, matrix multiplication `@`,
  `np.linalg.solve`
- **Core에서 사용하지 않음:** `np.linalg.inv`, elementwise division으로 linear
  solve 대체, `squeeze`로 반환 축 제거
- **표준 검산 선택:** `scipy.stats.multivariate_normal.logpdf`
- **선택 이유:** SciPy에는 일반 partition을 직접 반환하는 단일 conditional API가
  없으므로, 표준 Gaussian log-density로
  `log p(x_t|x_o) = log p(x_t,x_o) - log p(x_o)`를 독립 확인한다.
- **주의할 점:** SciPy 검산은 T1–T3를 마친 뒤 `standard_api.py`에서만 수행하며,
  직접 구현 계약을 대신하지 않는다.

## 과제

T1–T3와 T5–T6이 Core다. T4는 Core 구현을 마친 뒤 읽는 선택 검산 자료다.

### T1. 실행 전 예측

1. `mu_t`, `mu_o`, 네 covariance block, 두 `solve` 결과, 최종 mean/covariance의
   shape을 적는다.
2. 관측값이 observed mean보다 큰 이번 사례에서 conditional mean이 marginal
   mean의 어느 방향으로 이동할지 cross-covariance의 부호로 예측한다.
3. conditional variance와 marginal variance 중 어느 쪽이 더 클지 예측하고,
   관측으로 얻은 정보와 연결해 설명한다.
4. observed value를 바꾸면 conditional mean과 conditional covariance 중 무엇이
   바뀔지 식의 항을 근거로 예측한다.

### T2. 같은 수치의 손계산

1. $\mu_t,\mu_o,\Sigma_{tt},\Sigma_{to},\Sigma_{ot},\Sigma_{oo}$를 적는다.
2. Marginal mean과 covariance를 구한다.
3. $\delta_o=v_o-\mu_o$와 $\Sigma_{oo}z=\delta_o$의 해를 구해 conditional
   mean을 계산한다.
4. $\Sigma_{oo}Z=\Sigma_{ot}$의 해를 구해 conditional covariance를 계산한다.
5. 계산 결과를 T1의 방향·크기 예측과 비교한다.

### T3. 직접 구현

`starter.py`의 두 함수를 완성한다.

1. `gaussian_marginal(mean, covariance, indices)`는 선택 순서를 보존해
   `(marginal_mean, marginal_covariance)`를 반환한다.
2. `gaussian_conditional(mean, covariance, target_indices, observed_indices,
   observed_values)`는 block slicing과 두 번의 `solve`로
   `(conditional_mean, conditional_covariance)`를 반환한다.
3. 1D central case뿐 아니라 target과 observed가 각각 여러 개인 partition에서도
   같은 shape 계약을 지킨다.

`np.linalg.inv`는 사용하지 않는다. 부동소수 비교 허용오차는 `rtol=1e-7`,
`atol=1e-12`다.

### T4. 표준 API 검산 (선택, 작성 없음)

T1–T3와 계약 테스트를 마친 뒤 `standard_api.py`를 읽고 실행한다. 여러 target
후보에서 closed-form conditional log-density와 joint-minus-marginal log-density가
일치하는지 확인한다.

### T5. 실패 해석

1. `covariance[indices, indices]`와 `covariance[np.ix_(indices, indices)]`의
   결과 shape이 왜 다른지 설명하고, 전자가 일반적인 covariance block이 되지
   않는 경우를 만든다.
2. `sigma_to / sigma_oo`가 여러 observed dimension에서 linear solve를 대신하지
   못하는 이유를 연산 의미와 shape으로 설명한다.
3. `squeeze()`가 1D central case를 편하게 보여도 generic 반환 계약을 깨뜨리는
   이유를 설명한다.
4. Target/observed index 순서를 바꾸면 block의 행·열과 반환값의 변수 순서를
   함께 추적해야 하는 이유를 적는다.

### T6. 설명 확인

1. Marginalization과 conditioning을 각각 "없애는 변수"와 "고정하는 값"을
   포함해 설명한다.
2. Conditional mean correction에서 cross-covariance, observed residual,
   observed covariance solve가 맡는 역할을 설명한다.
3. Conditional covariance가 이번 계약에서는 observed value 자체에 의존하지
   않는다는 것을 식에서 찾아 설명한다.
4. `T=2`, `O=3`인 경우 모든 block과 두 `solve` 결과의 shape을 다시 적는다.

## 제출물

- `answers.md`: T1–T2, T5–T6의 예측·계산·설명
- `starter.py`: T3의 두 함수 구현
- 통과한 `test_contract.py`
- 선택: D0–D2의 guided derivation과 비교 설명

## 완료 기준

- Joint mean/covariance를 임의의 target/observed index 순서에 맞게 block으로
  나누고 각 shape을 설명한다.
- 같은 central case에서 marginal과 conditional parameter를 손으로 계산하고
  실행 전 예측과 비교한다.
- Explicit inverse 없이 1D와 다차원 partition에서 계약된 shape의 결과를
  허용오차 안에서 계산한다.
- Marginalization과 conditioning의 확률적 의미, conditional mean 이동,
  uncertainty 감소를 자신의 말로 설명한다.

처음부터 혼자 모두 맞히는 것은 완료 조건이 아니다. 도움을 받은 뒤에는 정의와
계산 경로를 보지 않고 다시 설명하고, 다른 index partition에도 적용할 수 있어야
한다.

## 선택 확장

### D0. Guided quadratic-form 유도

Block matrix의 quadratic form과 완전제곱을 처음부터 안내받아 conditional Gaussian
공식을 유도한다. Block inverse 항등식을 미리 외운 것으로 가정하지 않으며 Core
채점 대상이 아니다.

### D1. Ch. 5 posterior와 객체 비교

이번 세션의 $p(x_t\mid x_o)$와 Ch. 5의 $p(\theta\mid D)$를 비교한다. 둘 다
conditioning이지만, 앞의 식은 한 random vector의 일부를 관측한 것이고 뒤의 식은
공유 parameter에 대한 믿음을 데이터로 갱신한 것이다. 이 구분을 데이터,
parameter, 관측값의 역할로 설명한다.

### D2. Schur complement

$\Sigma_{t\mid o}$를 $\Sigma$의 Schur complement로 보고, SPD joint covariance가
conditional covariance의 positive definiteness를 보장하는 이유를 guided proof로
살펴본다.

## 검산

예측과 손계산을 기록한 뒤 실행한다.

```bash
cd week3-machine-learning/curriculum/sessions/S11
../../../../.venv/bin/python -m unittest -v test_contract.py
../../../../.venv/bin/python standard_api.py  # Core 완료 후 선택
```
