# S04 — 정보량·entropy·cross-entropy·KL

> 상태: `ready`. 한 과제씩 진행하고, 실행 전 예측을 먼저 기록한다.

## 목표와 비목표

- 목표: 세 범주의 확률분포에서 self-information과 entropy를 계산한다.
- 목표: 같은 source distribution `p`에 대해 cross-entropy와 KL divergence를 계산한다.
- 목표: `H(p, q) = H(p) + KL(p || q)`의 각 항이 무엇을 뜻하는지 설명한다.
- 목표: 손계산과 같은 정의식을 NumPy로 직접 구현한다.
- 이번 세션에서 하지 않는 것: softmax와 logits, 수치 안정화 기법,
  `torch.nn.CrossEntropyLoss`, 실제 분류모델 학습 또는 평가.

## 시작 전 선수지식 확인

1. `log2(1)`, `log2(1/2)`, `log2(1/4)`는 각각 얼마인가?
2. `sum_i p_i f_i`를 `p`에 대한 기대값으로 읽으려면 `p_i`가 어떤 조건을
   만족해야 하는가?
3. 확률표에서 한 변수를 합으로 제거해 얻은 길이 3의 marginal도 하나의
   확률분포로 사용할 수 있는가? 이유는 무엇인가?

막히면 [로그 복습 카드](../../concepts/logarithm.md),
[S03의 기대값 정의](../S03/PROBLEM.md#사용할-정의),
[S02의 joint와 marginal 정의](../S02/PROBLEM.md#사용할-정의)를 먼저 복습한다.

## 교재 연결

- 판본: Kevin P. Murphy, *Machine Learning: A Probabilistic Perspective* (2012).
- 주제명: Chapter 2의 information theory.
- 확인할 개념: self-information, entropy, cross-entropy, KL divergence.
- 필요한 정의와 수치는 아래에 모두 제공된다.

## 문제에서 주어진 정보

한 source가 세 범주 `0`, `1`, `2` 중 하나를 출력한다. `p`는 source의
분포이고, `q`는 같은 세 범주에 대해 한 모델이 제시한 분포다. 두 배열의 index
순서는 같다.

```python
p = np.array([0.50, 0.25, 0.25], dtype=np.float64)
q = np.array([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], dtype=np.float64)
```

두 배열은 shape `(3,)`이고 모든 원소가 양수이며 각각 합이 1이다. 이 세션에서는
로그의 밑을 `2`로 고정하므로 정보량의 단위는 **bit**다. `p`는 실제로 outcome에
가중치를 주는 source distribution이고, `q`는 그 outcome에 확률을 부여하는
모델 distribution이다.

## 사용할 정의

범주 `i`에 모델 `q`가 부여한 self-information은 다음과 같다.

```text
I_q(i) = -log2(q_i)
```

Entropy는 source `p` 자체의 self-information을 `p`로 평균낸 값이다.

```text
H(p) = -sum_i p_i log2(p_i)
     = E_p[-log2(p_i)]
```

Cross-entropy는 모델 `q`의 self-information을 source `p`로 평균낸 값이다.

```text
H(p, q) = -sum_i p_i log2(q_i)
        = E_p[-log2(q_i)]
```

KL divergence는 `p`와 `q`의 log probability ratio를 `p`로 평균낸 값이다.

```text
KL(p || q) = sum_i p_i log2(p_i / q_i)
```

이 정의들에는 다음 관계가 있다.

```text
H(p, q) = H(p) + KL(p || q)
```

`KL(p || q)`는 0 이상이고 `p`와 `q`가 같을 때 0이다. 일반적으로 두 입력의
순서를 바꿀 수 있는 대칭 거리가 아니다. 이번 세션은 모든 확률이 양수인 경우만
다루므로 `log2(0)`이나 `0 log 0` 규칙은 필요하지 않다.

## 과제

### T1. 실행 전 예측

코드나 테스트를 실행하기 전 `answers.md`에 답한다.

1. `H(p)`, `H(p, q)`, `KL(p || q)`에서 합의 가중치로 사용되는 분포는 각각
   무엇인가?
2. 주어진 `p`와 `q`에서 `H(p, q)`가 `H(p)`보다 클지, 같을지, 작을지 예측하고
   이유를 적는다.
3. `KL(p || q)`의 부호를 예측한다.

### T2. 세 정보량 손계산

1. 각 범주에 대해 `-log2(p_i)`와 `-log2(q_i)`를 계산한다.
2. `-p_i log2(p_i)` 세 항을 적고 더해 `H(p)`를 구한다.
3. `-p_i log2(q_i)` 세 항을 적고 더해 `H(p, q)`를 구한다.
4. `p_i log2(p_i / q_i)` 세 항을 적고 더해 `KL(p || q)`를 구한다.
5. 세 결과가 `H(p, q) = H(p) + KL(p || q)`를 만족하는지 확인한다.

계산 과정에서는 `log2(3)` 같은 항을 기호로 유지해도 된다. 마지막에는 계산기나
NumPy를 이용해 소수값도 함께 기록한다.

### T3. 같은 정의의 NumPy 직접 구현

`starter.py`의 세 함수를 완성한다.

- `entropy(p)`: `H(p)`를 반환한다.
- `cross_entropy(p, q)`: `H(p, q)`를 반환한다.
- `kl_divergence(p, q)`: `KL(p || q)`를 반환한다.

함수 계약은 다음과 같다.

- 각 입력은 비어 있지 않은 1차원 `float64` 배열이다.
- 모든 확률은 양수이고 각 분포의 합은 1이다.
- 두 입력을 받는 함수에서 `p`와 `q`의 shape는 같다.
- 세 함수는 base-2 logarithm을 사용하고 Python `float` 하나를 반환한다.
- 정의식을 NumPy 배열 연산으로 직접 구현한다.

필수 구현은 유효한 입력 계산에 집중하며 입력 validation은 선택 확장으로 둔다.

### T4. 관계식 검산

T2와 T3을 마친 뒤 다음을 확인한다.

1. 세 함수의 결과가 손계산과 일치하는지 `np.isclose`로 확인한다.
2. `cross_entropy(p, q)`와
   `entropy(p) + kl_divergence(p, q)`가 일치하는지 `np.isclose`로 확인한다.
3. `kl_divergence(p, p)`가 0에 가까운지 확인하고 그 이유를 적는다.

### T5. 방향을 바꾼 실패 사례

실행 전 다음 두 변경의 결과를 예측한 뒤 실제로 확인한다.

1. Cross-entropy에서 항의 가중치를 `p`가 아니라 `q`로 바꾸면 어떤 양을
   계산하게 되는가?
2. `kl_divergence(q, p)`는 `kl_divergence(p, q)`와 같은가? 두 표현이 각각
   어느 분포에 대한 기대값인지 설명한다.

shape와 전체 합이 모두 정상이어도 분포의 역할이나 입력 순서가 바뀌면 다른
질문을 계산할 수 있다는 점을 기록한다. 확인 후 올바른 구현으로 되돌린다.

### T6. 설명 확인

다음을 자기 말로 설명한다.

> `H(p)`, `H(p, q)`, `KL(p || q)`는 각각 무엇을 `p`로 평균낸 값인가?
> 모델 분포 `q`가 source 분포 `p`와 다를 때 cross-entropy에는 어떤 추가량이
> 생기며, KL의 두 입력 순서는 왜 중요한가?

## 검산

T1–T4를 작성하고 구현한 뒤 프로젝트 root에서 실행한다.

```bash
cd week3-machine-learning/curriculum/sessions/S04
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```

테스트는 중심 사례의 정답을 대신하지 않으며, 다른 유효한 확률분포에서도 각
함수가 공개된 정의와 일치하는지 확인한다.

## 제출물

- `answers.md`: T1–T6의 예측, 항별 손계산, 검산, 설명
- 완성한 `starter.py`
- 통과한 `test_contract.py` 실행 결과

## 완료 기준

- 세 범주의 같은 `p`, `q`로 entropy, cross-entropy, KL을 항별로 손계산한다.
- 세 함수가 base-2 정의식을 구현하고 다른 유효한 입력에서도 올바르게 동작한다.
- 세 양의 관계식을 수치와 의미 양쪽에서 설명한다.
- 합의 가중치가 `p`라는 점과 `p`, `q`의 역할을 구분한다.
- KL의 입력 순서가 나타내는 기대값의 기준을 설명한다.
- 제공된 계약 테스트를 통과한다.

## 선택 확장

입력 validation을 추가한다. 배열 차원, dtype, 양수 조건, 확률 합, 두 배열의
shape 일치를 나누어 검사하고 각 위반에 대한 자신의 테스트를 작성한다. 확률 0을
허용하는 일반화는 이 확장에도 포함하지 않는다.
