# MLAPP practice curriculum

MLAPP의 확률적 관점을 손계산, NumPy 정의식 구현, PyTorch 검증, 신호처리·DNN 적용으로 연결하는 40세션(80시간) 과정이다. 읽은 장 수가 아니라 선수개념의 무게를 기준으로 배분했다. 특히 Ch.3–5를 충분히 반복하며, 표본 계산은 별도 주제로 분리하지 않고 필요한 기대값·적분·검산 안에서만 사용한다.

## 시간 배분

| 범위 | 세션 | 시간 | 문서 |
|---|---:|---:|---|
| Ch.1–2 | 4 | 8시간 | [Phase A](phase_a_ch01_02/README.md) |
| Ch.3 | 3 | 6시간 | [Phase B](phase_b_ch03_discrete/README.md) |
| Ch.4 | 5 | 10시간 | [Phase C](phase_c_ch04_gaussian/README.md) |
| Ch.5 | 6 | 12시간 | [Phase D](phase_d_ch05_bayesian/README.md) |
| Ch.6 | 5 | 10시간 | [Phase E](phase_e_ch06_evaluation/README.md) |
| Ch.7 | 6 | 12시간 | [Phase F](phase_f_ch07_regression/README.md) |
| Ch.8.1–8.3 | 7 | 14시간 | [Phase G](phase_g_ch08_logistic/README.md) |
| Ch.11 일부 | 4 | 8시간 | [Phase H](phase_h_ch11_conditional/README.md) |
| 합계 | **40** | **80시간** | |

## Tutor 루프와 구현 경계

각 세션은 120분이다: 문제·shape 예측 10분 → 손수학 25분 → NumPy 정의식 구현 40분 → PyTorch/신뢰할 수 있는 라이브러리 대조 20분 → 실패 사례·독립 검증 15분 → 5분 설명과 기록 10분. 핵심 PMF/PDF, likelihood, posterior update, loss, gradient는 한 번 직접 구현한다. 난수 생성, 선형계 풀이, Cholesky, 분위수처럼 이미 검증된 저수준 수치 알고리즘은 라이브러리에 맡긴다. 라이브러리 호출은 직접 구현을 대체하지 않고 검산한다.

## 40세션 색인

| ID | 제목 | 핵심 질문 | 선수 | 상세 |
|---|---|---|---|---|
| S01 | 확률모형의 객체와 shape | 무엇이 관측·잠재·학습·고정인가? | 없음 | [A](phase_a_ch01_02/README.md#s01-확률모형의-객체와-shape) |
| S02 | Joint·marginal·conditional | 어떤 축을 합하고 정규화하는가? | S01 | [A](phase_a_ch01_02/README.md#s02-jointmarginalconditionalbayes) |
| S03 | 기대값·분산·공분산 | 분포 요약과 표본 요약은 어떻게 다른가? | S02 | [A](phase_a_ch01_02/README.md#s03-기대값분산공분산) |
| S04 | 정보량과 cross-entropy | 분류 loss가 왜 NLL인가? | S02 | [A](phase_a_ch01_02/README.md#s04-entropycross-entropykl) |
| S05 | Bernoulli·Binomial | 시행과 count의 likelihood는 어떻게 연결되는가? | S02–03 | [B](phase_b_ch03_discrete/README.md#s05-bernoullibinomial) |
| S06 | Categorical·Multinomial | 한 범주와 count vector를 어떻게 모델링하는가? | S04–05 | [B](phase_b_ch03_discrete/README.md#s06-categoricalmultinomial) |
| S07 | Dirichlet 생성분류 | prior count가 예측을 어떻게 바꾸는가? | S06 | [B](phase_b_ch03_discrete/README.md#s07-dirichlet과-생성분류) |
| S08 | 1D Gaussian | MSE는 언제 Gaussian NLL인가? | S03 | [C](phase_c_ch04_gaussian/README.md#s08-1차원-gaussian) |
| S09 | Vector와 covariance | 공분산은 방향별 변동을 어떻게 담는가? | S03,S08 | [C](phase_c_ch04_gaussian/README.md#s09-vector와-covariance) |
| S10 | Multivariate Gaussian | log-density를 안정적으로 어떻게 계산하는가? | S09 | [C](phase_c_ch04_gaussian/README.md#s10-multivariate-gaussian-계산) |
| S11 | Gaussian 조건화 | 관측 후 평균·불확실성은 어떻게 변하는가? | S10 | [C](phase_c_ch04_gaussian/README.md#s11-gaussian-conditioning과-marginalization) |
| S12 | Gaussian 생성분류 | covariance 가정이 경계를 어떻게 바꾸는가? | S10 | [C](phase_c_ch04_gaussian/README.md#s12-gaussian-생성분류) |
| S13 | Beta–Bernoulli Bayes | prior와 data가 posterior에서 어떻게 합쳐지는가? | S05 | [D](phase_d_ch05_bayesian/README.md#s13-bayes-구조와-betabernoulli) |
| S14 | MLE·MAP·posterior mean | 세 점추정은 언제 달라지는가? | S13 | [D](phase_d_ch05_bayesian/README.md#s14-mlemapposterior-mean) |
| S15 | 구간과 prior sensitivity | 불확실성과 prior 영향은 어떻게 보고하는가? | S14 | [D](phase_d_ch05_bayesian/README.md#s15-credible-interval과-prior-sensitivity) |
| S16 | Gaussian Bayesian inference | 정밀도는 정보의 가중치로 어떻게 작동하는가? | S08,S13 | [D](phase_d_ch05_bayesian/README.md#s16-gaussian-parameter의-bayesian-추론) |
| S17 | Posterior predictive | parameter uncertainty를 예측에 어떻게 전달하는가? | S15–16 | [D](phase_d_ch05_bayesian/README.md#s17-posterior-predictive) |
| S18 | Bayesian decision·MAP | 예측과 행동, prior와 penalty는 어떻게 연결되는가? | S17 | [D](phase_d_ch05_bayesian/README.md#s18-bayesian-decision과-map-regularization) |
| S19 | Sampling distribution | 반복 표본에서 무엇이 변하는가? | S05,S08 | [E](phase_e_ch06_evaluation/README.md#s19-sampling-distribution과-standard-error) |
| S20 | Bias·variance·risk | unbiased가 항상 좋은가? | S19 | [E](phase_e_ch06_evaluation/README.md#s20-biasvariance와-estimator-risk) |
| S21 | Confidence와 credible | 두 구간의 확률 문장은 어떻게 다른가? | S15,S19 | [E](phase_e_ch06_evaluation/README.md#s21-confidence-interval과-credible-interval) |
| S22 | Bootstrap·검정 | 닫힌형이 없을 때 불확실성을 어떻게 평가하는가? | S20–21 | [E](phase_e_ch06_evaluation/README.md#s22-bootstrap과-hypothesis-testing) |
| S23 | Split·CV·모델 비교 | leakage 없이 일반화를 어떻게 비교하는가? | S22 | [E](phase_e_ch06_evaluation/README.md#s23-splitcv와-모델-비교) |
| S24 | 선형회귀 생성 가정 | squared error 뒤의 확률가정은 무엇인가? | S08 | [F](phase_f_ch07_regression/README.md#s24-선형회귀의-생성-가정) |
| S25 | 최소제곱 수치계산 | 해를 안정적으로 어떻게 구하는가? | S24 | [F](phase_f_ch07_regression/README.md#s25-최소제곱과-수치-안정성) |
| S26 | Gradient descent | 수식 gradient와 autograd는 일치하는가? | S25 | [F](phase_f_ch07_regression/README.md#s26-gradient-descent와-pytorch) |
| S27 | Basis와 과적합 | 표현력 증가는 언제 일반화를 해치는가? | S23,S25 | [F](phase_f_ch07_regression/README.md#s27-basis-expansion과-overfitting) |
| S28 | Ridge·MAP·Bayes 회귀 | regularization과 불확실성은 어떻게 연결되는가? | S16,S18,S27 | [F](phase_f_ch07_regression/README.md#s28-ridgemapbayesian-linear-regression) |
| S29 | System identification | 세 회귀 접근은 noisy filter에서 어떻게 다른가? | S23,S28 | [F](phase_f_ch07_regression/README.md#s29-system-identification-통합) |
| S30 | Sigmoid conditional model | 선형 score를 확률로 어떻게 바꾸는가? | S05,S24 | [G](phase_g_ch08_logistic/README.md#s30-sigmoid와-bernoulli-conditional-model) |
| S31 | Stable BCE | 극단 logit에서도 loss를 어떻게 안정화하는가? | S30 | [G](phase_g_ch08_logistic/README.md#s31-stable-binary-cross-entropy) |
| S32 | Logistic gradient | 왜 gradient가 $X^T(p-y)$인가? | S26,S31 | [G](phase_g_ch08_logistic/README.md#s32-logistic-gradient) |
| S33 | Softmax regression | binary를 multiclass로 어떻게 일반화하는가? | S04,S32 | [G](phase_g_ch08_logistic/README.md#s33-multiclass-softmax-regression) |
| S34 | Regularized logistic | 분리 가능 데이터에서 prior가 왜 필요한가? | S18,S32 | [G](phase_g_ch08_logistic/README.md#s34-regularized-logistic-regression) |
| S35 | Calibration·decision | 좋은 분류와 좋은 확률·행동은 같은가? | S17,S21,S33 | [G](phase_g_ch08_logistic/README.md#s35-calibrationthreshold와-decision) |
| S36 | 신호분류 통합 | model·feature·decision 실패를 구분할 수 있는가? | S23,S34–35 | [G](phase_g_ch08_logistic/README.md#s36-신호분류-통합) |
| S37 | Ch.11 범위·latent 구조 | 선택 절의 관측·잠재 구조는 무엇인가? | S02,S36 | [H](phase_h_ch11_conditional/README.md#s37-선택-범위-확정과-latent-구조) |
| S38 | Mixture·responsibility | soft assignment는 어떤 posterior인가? | S10,S37 | [H](phase_h_ch11_conditional/README.md#s38-mixture와-responsibility-조건부) |
| S39 | EM | 반복 추론은 무엇을 번갈아 최적화하는가? | S38 | [H](phase_h_ch11_conditional/README.md#s39-em과-반복-추론-조건부) |
| S40 | 전체 capstone | 모델에서 decision까지 한 흐름으로 설명할 수 있는가? | S23,S29,S36,S37–39 | [H](phase_h_ch11_conditional/README.md#s40-전체-capstone) |

## 전체 선수관계

```text
S01 → S02 → S03 ─────────→ S08 → S09 → S10 → S11
       └────→ S04              └───────────→ S12
S02,S03 → S05 → S06 → S07
S05 → S13 → S14 → S15 ┐
S08,S13 → S16 ─────────┴→ S17 → S18
S05,S08 → S19 → S20 → S21 → S22 → S23
S08 → S24 → S25 → S26 → S27 → S28 → S29
S05,S24 → S30 → S31 → S32 → S33 → S34 → S35 → S36
S02,S36 → S37 → S38 → S39 → S40
S23,S29,S36 ───────────────────────────────→ S40
```

Ch.11의 정확한 절과 주제는 소유한 판본의 목차로 확인한 뒤 Phase H의 조건부 세션을 교체 또는 확정한다.
