# S02 — Joint·marginal·conditional·Bayes

> 상태: `ready`. 한 과제씩 진행하고, 실행 전 예측을 먼저 기록한다.

## 목표와 비목표

- 목표: 하나의 2×2 count table에서 joint distribution을 만든다.
- 목표: joint에서 두 marginal과 conditional probability를 계산한다.
- 목표: 같은 posterior를 joint 정의와 Bayes rule 두 방식으로 계산한다.
- 목표: NumPy의 `axis`가 어떤 변수를 합으로 제거하는지 설명한다.
- 이번 세션에서 하지 않는 것: 연속분포, likelihood parameter inference,
  broadcasting 일반화, 실제 detector 성능 평가.

## 시작 전 선수지식 확인

1. `[2, 3, 5]`의 모든 값을 합하면 얼마인가?
2. shape `(2, 3)`에서 축은 몇 개이며 각 축의 길이는 얼마인가?
3. 2차원 배열 `x`에서 `x[1, 0]`은 어느 위치인가?
4. S01의 `D`와 `x_i`는 어떻게 다른가?

막히면 다음 자료만 복습하고 다시 답한다.

- [유한합](../../concepts/finite_sum.md)
- [S01 shape와 indexing](../S01/PROBLEM.md#사용할-정의)

## 교재 연결

- 판본: Kevin P. Murphy, *Machine Learning: A Probabilistic Perspective* (2012).
- 주제명: Chapter 2의 joint, marginal, conditional probability와 Bayes rule.
- 이 세션에서 확인할 기호: `p(A, Y)`, `p(A)`, `p(Y)`, `p(Y|A)`, `p(A|Y)`.
- 교재는 정의의 참고자료이며, 계산에 필요한 수치는 아래에 모두 주어진다.

## 문제에서 주어진 정보

100번의 상황에서 실제 alarm 상태 `A`와 detector 출력 `Y`를 함께 기록했다.

- `A=0`: 실제 alarm 상황이 아님
- `A=1`: 실제 alarm 상황임
- `Y=0`: detector가 음성을 출력함
- `Y=1`: detector가 양성을 출력함

행은 `A=0, 1`, 열은 `Y=0, 1` 순서다.

```python
counts = np.array(
    [
        [72, 8],
        [6, 14],
    ],
    dtype=np.int64,
)
```

`counts[a, y]`는 `A=a`와 `Y=y`가 동시에 관측된 횟수다. 이 표 밖의 사례나
추가 수치는 만들지 않는다.

## 사용할 정의

전체 횟수를 `N`이라 할 때 joint probability table은 다음과 같다.

```text
p(A=a, Y=y) = counts[a, y] / N
```

한 변수를 합으로 제거하면 다른 변수의 marginal distribution을 얻는다.

```text
p(A=a) = sum_y p(A=a, Y=y)
p(Y=y) = sum_a p(A=a, Y=y)
```

조건부확률은 조건에 해당하는 marginal로 joint를 나눈다.

```text
p(Y=y | A=a) = p(A=a, Y=y) / p(A=a)
p(A=a | Y=y) = p(A=a, Y=y) / p(Y=y)
```

Bayes rule은 같은 posterior를 다음처럼 표현한다.

```text
p(A=a | Y=y) = p(Y=y | A=a) p(A=a) / p(Y=y)
```

### 배열의 축

`counts`와 joint table의 shape는 `(2, 2)`다.

- axis `0`은 행 방향의 변수 `A`를 센다.
- axis `1`은 열 방향의 변수 `Y`를 센다.
- `x.sum(axis=k)`는 axis `k`를 따라 더하고 그 축을 결과에서 제거한다.

따라서 marginal을 만들 때는 **결과에 남길 변수**와 **합으로 제거할 변수**를
먼저 구분해야 한다. 어느 axis를 지정할지는 과제에서 직접 결정한다.

## 과제

### T1. 실행 전 예측

코드나 테스트를 실행하기 전에 `answers.md`에 답한다.

1. `counts.shape`는 무엇이며 axis `0`, axis `1`은 각각 무엇을 세는가?
2. `p(A)`를 얻으려면 어느 변수를 합으로 제거해야 하는가?
3. `p(Y)`를 얻으려면 어느 변수를 합으로 제거해야 하는가?
4. `p(Y=1|A=1)`과 `p(A=1|Y=1)`은 같은 질문인가? 이유는 무엇인가?

### T2. Joint와 marginal 손계산

1. count table 전체를 합해 `N`을 구한다.
2. 2×2 joint probability table을 계산한다.
3. `p(A)`와 `p(Y)`를 각각 길이 2인 vector로 계산한다.
4. joint와 두 marginal이 각각 합해서 1인지 확인한다.

결과와 중간 계산을 `answers.md`에 기록한다.

### T3. NumPy 구현

`starter.py`의 다음 두 함수를 완성한다.

- `normalize_joint(counts)`: count table을 합이 1인 `float64` joint table로
  변환한다. shape는 입력과 같다.
- `compute_marginals(joint)`: `(p_a, p_y)`를 반환한다. 두 결과는 shape `(2,)`이고
  index 순서는 각각 `A=0,1`과 `Y=0,1`이다.

반환할 구체적인 숫자와 `sum`의 axis는 T2의 계산과 배열 의미에서 직접 정한다.

### T4. Conditional과 Bayes

손으로 다음 값을 계산해 `answers.md`에 기록한다.

1. detector의 실제 alarm 조건 양성률 `p(Y=1|A=1)`
2. detector 양성이 주어졌을 때 실제 alarm posterior `p(A=1|Y=1)`

그다음 `compute_alarm_posterior(joint)`를 완성한다. 이 함수는 같은
`p(A=1|Y=1)`을 다음 순서의 tuple로 반환한다.

1. conditional probability의 정의로 joint에서 직접 계산한 값
2. Bayes rule로 계산한 값

두 계산이 같은지 `np.isclose`로 확인한다.

### T5. Axis 실패 사례

`compute_marginals()`에서 `p(A)`와 `p(Y)`에 사용할 axis를 서로 바꿔 실행한다.
코드 수정 전 다음을 `answers.md`에 적는다.

- 각 결과의 숫자가 어떤 변수의 marginal인지
- shape와 합이 모두 정상이어도 의미가 틀릴 수 있는 이유

확인 후 올바른 구현으로 되돌린다.

### T6. 설명 확인

다음을 자기 말로 설명한다.

> Joint table에서 marginal과 conditional을 각각 어떻게 만들며,
> `p(Y=1|A=1)`과 `p(A=1|Y=1)`은 왜 다른가? Bayes rule은 둘을 어떻게 연결하는가?

## 검산

T1–T4를 작성하고 구현한 뒤 프로젝트 root에서 실행한다.

```bash
cd week3-machine-learning/curriculum/sessions/S02
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```

테스트는 구현 후 검산에만 사용한다.

## 제출물

- `answers.md`: T1, T2, T4, T5, T6의 예측·계산·설명
- 완성한 `starter.py`
- 통과한 `test_contract.py` 실행 결과

## 완료 기준

- joint, marginal, conditional, posterior를 같은 표에서 구분한다.
- 합으로 제거하는 axis와 결과에 남는 변수의 관계를 설명한다.
- posterior를 joint 정의와 Bayes rule 두 방식으로 계산해 일치시킨다.
- 도움 없이 다른 2×2 joint table에서도 같은 계산 순서를 설명한다.
- 제공된 테스트를 모두 통과한다.

## 선택 확장

핵심을 마친 뒤에만 count table의 한 칸을 바꾸고 posterior가 어떻게 변하는지
예측한 뒤 다시 계산한다. 이 확장은 완료 기준에 포함하지 않는다.
