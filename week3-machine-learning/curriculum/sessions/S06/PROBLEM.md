# S06 — Categorical·Multinomial

> 상태: `ready`. 실행 전 예측을 `answers.md`에 먼저 적는다.

## 목표와 비목표

- 목표: label sequence, one-hot matrix, count vector를 서로 변환한다.
- 목표: Categorical sequence likelihood와 Multinomial count PMF를 구분한다.
- 목표: simplex 위 Categorical MLE를 성공 비율의 일반화로 이해한다.
- 비목표: Dirichlet prior, 생성분류, 신경망 loss.

## 시작 전 선수지식 확인

1. S05에서 ordered likelihood와 count PMF가 어떤 상수배로 연결되었는가?
2. `theta[labels]`의 shape을 예측하라.
3. 각 원소가 0 이상이고 전체 합이 1인 vector를 유효한 확률 vector로
   볼 수 있는 이유를 설명한다. 이 조건을 만족하는 공간을 simplex라고 한다.

막히면 [S05 정의](../S05/PROBLEM.md#사용할-정의)와
[S01 indexing](../S01/PROBLEM.md#문제에서-주어진-정보)을 복습한다.

## 교재 연결

- Kevin P. Murphy, *MLAPP* (2012), Ch.3 Categorical/Multinomial distribution.

## 문제에서 주어진 정보

```python
labels = np.array([0, 2, 1, 2, 2], dtype=np.int64)  # shape (5,)
theta = np.array([0.2, 0.3, 0.5], dtype=np.float64) # shape (3,)
```

label은 `0,1,2`, `theta[j]=P(X=j)`이며 관측은 iid다.

## 사용할 정의

```text
p(x_i=j | theta) = theta_j
L_seq = product_i theta[x_i]
c_j = number of labels equal to j
P(C=c | theta) = n! / product_j(c_j!) * product_j theta_j^c_j
theta_hat_j = c_j / n
one_hot[i,j] = 1 if labels[i]=j else 0
```

## 구현 도구 구분

- **직접 구현:** `(N,K)` one-hot에 행별 label 열을 1로 배치하는
  과정, one-hot 열합과 count의 관계, Categorical sequence likelihood,
  Multinomial count PMF, `counts/n` MLE.
- **사용 권장 API:** `np.zeros((N,K))`, `np.arange(N)`, paired advanced
  indexing, `.sum(axis=0)`, `theta[labels]`, `np.prod`, `math.factorial`, `math.prod`.
  이 primitive들을 조합해 정의식을 표현한다.
- **검산 전용 API:** `np.eye(K)[labels]`, `np.bincount(labels,
  minlength=K)`, `np.unique(..., return_counts=True)`. one-hot/count를 한 호출로
  완성하므로 T3 직접 구현에는 쓰지 않고 T4에서만 비교한다.
- **표준 검산 선택:** one-hot은 `np.eye(K, dtype=np.float64)[labels]`,
  count는 `np.bincount(labels, minlength=K)`다. 둘 다 NumPy의 대표적인 vectorized
  표현이고 결과 shape가 명확하다. `minlength=K`를 빼면 관측되지 않은
  마지막 category가 출력에서 사라질 수 있다.

## 과제

### T1. 실행 전 예측
1. **T1-1** count vector와 가장 큰 MLE 성분을 예측한다.
2. **T1-2** sequence likelihood와 count PMF 중 더 큰 것과 이유를 예측한다.
3. **T1-3** one-hot matrix의 shape와 각 행의 합을 예측한다.

### T2. 손계산
1. **T2-1** labels를 count vector와 one-hot matrix로 바꾼다.
2. **T2-2** 다섯 Categorical PMF 항과 sequence likelihood를 계산한다.
3. **T2-3** Multinomial 계수와 count PMF를 계산한다.
4. **T2-4** `theta_hat` vector를 구하고 합을 확인한다.

### T3. 직접 구현
1. **T3-1** `one_hot`, `counts_from_labels`를 완성한다.
2. **T3-2** `categorical_likelihood`, `multinomial_pmf`를 완성한다.
3. **T3-3** `categorical_mle`를 완성한다.

계약: labels는 nonempty 1D `int64`, theta는 합이 1인 positive 1D `float64`,
counts는 1D `int64`다. one-hot은 `(n,K)` `float64`, counts는 `(K,)` `int64`,
likelihood/PMF는 Python `float`, MLE는 `(K,)` `float64`를 반환한다.
`num_categories=K`는 positive Python `int`, labels는 `0 <= label < K`, counts의 합은
양수이다. Multinomial 계수에는 `math.factorial(n)`과 여러 값을 곱하는
`math.prod(...)`를 사용해도 된다. 부동소수 비교 허용오차는 `rtol=1e-7`,
`atol=1e-12`다.

### T4. 검산

T4에서 새 검산 코드를 작성하지 않는다. T1–T3을 마친 뒤 제공된
`verify.py`를 실행하고 각 PASS/FAIL의 의미를 `answers.md`에 기록한다.

1. **T4-1** one-hot의 열합과 count vector를 비교한다.
2. **T4-2** count PMF / sequence likelihood와 Multinomial 계수를 비교한다.
3. **T4-3** label 순서를 바꿔도 count, 두 확률, MLE가 변하지 않는지 확인한다.

### T5. 잘못된 해석
1. **T5-1** Multinomial 계수를 sequence likelihood에 곱하는 오류를 설명한다.
2. **T5-2** 원래 labels 길이가 5인데 count vector의 합이 5가 아니면
   왜 그 labels의 요약이 아닌지 설명한다.

### T6. 설명 확인
1. **T6-1** label sequence와 count vector가 보존/제거하는 정보를 설명한다.
2. **T6-2** 두 확률의 값은 다르지만 MLE가 같은 이유를 설명한다.

## 검산
```bash
cd week3-machine-learning/curriculum/sessions/S06
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python verify.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```

`verify.py`는 표준 API와 개념 관계를 읽을 수 있는 검산 예시이고,
`test_contract.py`는 다른 유효한 입력에서도 함수 계약을 자동 검사한다.

## 제출물
`answers.md`, 완성한 `starter.py`, 통과한 계약 테스트.

## 완료 기준
T1–T6을 설명하고 다섯 함수가 공개 계약과 다른 유효한 입력을 통과한다.

## 선택 확장
입력 validation과 log-likelihood를 추가한다.
