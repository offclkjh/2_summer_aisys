# S07 — Categorical 생성분류와 zero-count 문제

> 상태: `ready`. 실행 전 예측을 먼저 기록한다.

## 목표와 비목표
- 목표: class prior와 class-conditional Categorical likelihood로 분류한다.
- 목표: unseen category가 log-joint를 `-inf`로 만드는 과정을 재현한다.
- 목표: additive smoothing 규칙의 보장과 한계를 설명한다.
- 비목표: Dirichlet posterior, 다중 feature naive Bayes, posterior 정규화.

## 시작 전 선수지식 확인
1. `p(y|x) ∝ p(y)p(x|y)`에서 분류 argmax에 공통 분모가 필요한가?
2. count 행을 확률로 바꾸려면 어느 축으로 정규화해야 하는가?
3. Categorical likelihood에 0인 항이 하나 포함되면 전체 곱은 어떻게 되는가?

막히면 [S02 Bayes rule](../S02/PROBLEM.md#사용할-정의),
[S06 Categorical 정의](../S06/PROBLEM.md#사용할-정의),
[S05 likelihood](../S05/PROBLEM.md#사용할-정의)를 복습한다.

## 교재 연결
- Kevin P. Murphy, *MLAPP* (2012), Ch.3 discrete generative classifiers.

## 문제에서 주어진 정보
```python
counts = np.array([[3, 1, 0],
                   [1, 4, 0]], dtype=np.int64)  # rows=class, columns=category
query_category = 2
alpha = 1.0
```

## 사용할 정의
```text
N_c = sum_j N_cj,  N = sum_c N_c
p(c) = N_c/N
p(x=j|c) = N_cj/N_c
score_c = log p(c) + log p(x=j|c)
smoothed p(x=j|c) = (N_cj+alpha)/(N_c+alpha*K)
```
score의 argmax만으로 분류할 수 있다. 모든 score가 `-inf`면 `argmax`가
숫자를 내더라도 의미 있는 클래스 선택이 아니다. smoothing은 위 규칙으로만
다루며 Bayes 정답으로 해석하지 않는다.
NumPy에서 `np.log(0)`은 `-np.inf`로 표현되며, 예상된 warning은
`np.errstate(divide="ignore")`로 범위를 한정해 숨길 수 있다.

## 구현 도구 구분

- **직접 구현:** count에서 class prior/conditional로 정규화하는 식,
  additive smoothing 분자·분모, log-joint score.
- **사용 권장 API:** `np.sum(..., axis=..., keepdims=True)`, broadcasting,
  `np.log`, `np.argmax`, `np.isfinite`, `np.errstate`. 이 API는 직접 재구현하지
  않는다.
- **검산 전용 API:** 현재 필수 범위에는 완성된 분류기 API를
  사용하지 않는다. `test_contract.py`의 독립 reference 계산으로 검산한다.
- **표준 검산 선택:** `np.testing.assert_allclose` 또는 `np.allclose`로
  prior 합·conditional 행합·reference score를 비교한다. 외부 분류기는 prior·
  smoothing 규칙을 숨기고 추가 의존성이 필요하므로 이 세션의 표준 검산이 아니다.

## 과제
### T1. 실행 전 예측
1. **T1-1** 더 큰 class prior를 예측한다.
2. **T1-2** category `0`의 예측 class와 이유를 적는다.
3. **T1-3** category `2`의 unsmoothed score와 분류 가능 여부를 예측한다.
4. **T1-4** smoothing 후 category `2` score와 예측 class를 예측한다.
### T2. 손계산
1. **T2-1** 행합, 전체 합, priors를 구한다.
2. **T2-2** unsmoothed conditional table과 행합을 구한다.
3. **T2-3** category `0`의 joint/log-joint와 prediction을 구한다.
4. **T2-4** category `2`의 joint/log-joint와 failure를 설명한다.
5. **T2-5** `alpha=1` conditional table과 행합을 구한다.
6. **T2-6** smoothed category `2` joint/log-joint와 prediction을 구한다.
### T3. 직접 구현
1. **T3-1** `class_priors(feature_counts) -> (C,) float64`를 완성한다.
2. **T3-2** `conditional_probabilities(feature_counts, alpha) -> (C,K) float64`를 완성한다.
3. **T3-3** `log_joint_scores(priors, conditionals, category) -> (C,) float64`를 완성한다.
4. **T3-4** `predict_class(...) -> int`를 완성한다. 의미 있는 예측은
   최소 한 score가 finite인 입력에만 적용한다.
계약: feature_counts는 nonnegative 2D `int64` shape `(C,K)`이고 각 행합은
양수이다. `alpha>=0`, `0<=category<K`이다. priors `(C,)`/conditionals `(C,K)`는
`float64` 확률 배열이고 `predict_class`는 Python `int`를 반환한다.
부동소수 비교 허용오차는 `rtol=1e-7`, `atol=1e-12`다.
### T4. 검산
1. **T4-1** prior 합과 conditional 행합을 확인한다.
2. **T4-2** category `0` 손계산과 코드를 비교한다.
3. **T4-3** category `2`의 unsmoothed `-inf` 두 개를 재현한다.
4. **T4-4** smoothing 후 모든 conditional과 score가 finite인지 확인한다.
### T5. 잘못된 해석
1. **T5-1** 열 방향으로 정규화했을 때 깨지는 의미를 설명한다.
2. **T5-2** all-`-inf` score에 `argmax`를 바로 쓰면 안 되는 이유를 설명한다.
3. **T5-3** 분자에만 alpha를 더하면 행합이 어떻게 되는지 설명한다.
### T6. 설명 확인
1. **T6-1** prior×conditional과 Bayes argmax의 연결을 설명한다.
2. **T6-2** zero count가 예측을 무너뜨리는 과정을 설명한다.
3. **T6-3** smoothing이 보장하는 것과 보장하지 않는 것을 설명한다.

## 검산
```bash
cd week3-machine-learning/curriculum/sessions/S07
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```
## 제출물
`answers.md`, 완성한 `starter.py`, 통과한 계약 테스트.
## 완료 기준
T1–T6을 설명하고 zero-count failure와 smoothing 후 변화를 코드로 재현한다.
## 선택 확장
alpha 값 두 개를 비교하되 Dirichlet posterior로 해석하지 않는다.
