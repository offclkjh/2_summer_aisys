# Phase D — Ch.5 Bayesian 통계

## Phase 계약

- **MLAPP 범위:** Ch.5 Bayesian statistics. 정확한 절은 판본 목차에서 확인한다.
- **필요한 수학:** Bayes rule, 적분/합산, conjugacy, 완전제곱, 기대손실.
- **코딩 지식:** parameter grid, 누적 update, numerical normalization, sampling axis; PyTorch optimizer는 MAP 검산에 사용.
- **구현 경계:** conjugate posterior, point summary, predictive와 expected loss를 직접 구현한다. 특수함수·분위수·난수 생성은 라이브러리에 맡긴다.
- **객체 템플릿:** $D$ 관측, $z$ 잠재 상태, $\theta$ 불확실한 파라미터, $\alpha$ prior hyperparameter, $a$ decision. $p(\theta\mid D,\alpha)$와 $p(y_*\mid D)$를 구분한다.
- **다음 Phase로 넘길 결과:** posterior uncertainty, predictive, MAP/regularization, decision의 일관된 계산 흐름.

## S13. Bayes 구조와 Beta–Bernoulli

- **중심 질문:** prior와 likelihood가 posterior에서 어떻게 합쳐지는가?
- **MLAPP 참고 범위:** Ch.5 Bayes rule, conjugate analysis(판본 절 확인).
- **큰 그림:** $\theta\sim\mathrm{Beta}(a,b)$, $D\mid\theta$ Bernoulli, $p(\theta\mid D)$.
- **먼저 할 손수학:** 작은 표본의 prior·likelihood·unnormalized posterior와 $(a+s,b+N-s)$를 계산한다.
- **직접 구현:** analytic/grid posterior와 sequential update; library density로 검산한다.
- **새 코딩 지식:** log-grid normalization, trapezoid integration, immutable update.
- **연결:** packet error uncertainty; calibration probability의 posterior.
- **검증:** 일괄/순차 update, grid/analytic posterior가 일치하는지 확인한다.
- **완료 기준:** evidence의 역할과 likelihood의 정규화 축을 설명한다.
- **시간/선수:** 120분 / S05.

## S14. MLE·MAP·posterior mean

- **중심 질문:** 세 점추정은 데이터량과 prior에 따라 언제 달라지는가?
- **MLAPP 참고 범위:** Ch.5 point estimates and summaries(판본 절 확인).
- **큰 그림:** 하나의 posterior에서 서로 다른 estimator/action을 선택한다.
- **먼저 할 손수학:** Beta posterior의 mode/mean과 Bernoulli MLE를 경계 사례까지 계산한다.
- **직접 구현:** 세 estimator와 sample-size/prior sweep; Torch optimizer MAP과 대조한다.
- **새 코딩 지식:** parameter sweep, boundary branch, tidy result table.
- **연결:** 희귀 오류율 추정; weight prior와 MAP 학습.
- **검증:** 데이터 증가 시 prior 영향 감소, mode 존재조건을 확인한다.
- **완료 기준:** posterior 전체와 점 요약의 정보 차이를 말한다.
- **시간/선수:** 120분 / S13.

## S15. Credible interval과 prior sensitivity

- **중심 질문:** posterior 불확실성과 prior 선택의 영향을 어떻게 보고하는가?
- **MLAPP 참고 범위:** Ch.5 posterior intervals/prior sensitivity(판본 절 확인).
- **큰 그림:** $\alpha$ 변화가 $p(\theta\mid D,\alpha)$와 interval에 미치는 영향.
- **먼저 할 손수학:** posterior CDF와 equal-tail interval 의미를 작은 grid에서 표시한다.
- **직접 구현:** grid quantile, posterior variance, sensitivity table; library quantile과 비교한다.
- **새 코딩 지식:** cumulative sum normalization, interpolation, plotting multiple conditions.
- **연결:** 센서 신뢰도 보고; uncertainty-aware calibration.
- **검증:** interval mass, 강/약 prior, 대칭/비대칭 posterior를 확인한다.
- **완료 기준:** “95% credible” 문장을 parameter에 대한 확률로 정확히 말한다.
- **시간/선수:** 120분 / S14.

## S16. Gaussian parameter의 Bayesian 추론

- **중심 질문:** prior와 data precision은 posterior 평균의 가중치가 되는가?
- **MLAPP 참고 범위:** Ch.5 Gaussian conjugate inference 중 선택 범위(판본 절 확인).
- **큰 그림:** 알려진 $\sigma^2$, $\mu\sim\mathcal N(\mu_0,\tau_0^2)$에서 $p(\mu\mid D)$.
- **먼저 할 손수학:** 완전제곱으로 posterior mean/variance를 유도하고 precision을 정보량으로 해석한다.
- **직접 구현:** analytic posterior와 parameter grid; PyTorch log-posterior 최적화로 mode를 검산한다.
- **새 코딩 지식:** precision parameterization, log posterior decomposition.
- **연결:** noisy amplitude 추정; Bayesian final-layer weight의 축소.
- **검증:** 극한 prior/data precision과 grid normalization을 확인한다.
- **완료 기준:** observation noise와 prior uncertainty를 구분한다.
- **시간/선수:** 120분 / S08,S13.

## S17. Posterior predictive

- **중심 질문:** parameter uncertainty를 새로운 관측 예측에 어떻게 전달하는가?
- **MLAPP 참고 범위:** Ch.5 posterior predictive(판본 절 확인).
- **큰 그림:** $p(y_*\mid D)=\int p(y_*\mid\theta)p(\theta\mid D)d\theta$.
- **먼저 할 손수학:** Beta–Bernoulli predictive와 Gaussian predictive mean/variance를 계산한다.
- **직접 구현:** analytic predictive, grid integration; posterior에서 뽑은 parameter의 예측 평균은 적분 검산에만 쓴다.
- **새 코딩 지식:** sample/data 축 구분, vectorized expectation, reproducible generator.
- **연결:** 다음 packet/센서값 예측; epistemic·aleatoric uncertainty.
- **검증:** analytic/grid/표본 근사가 오차 범위 안에서 일치하는지 확인한다.
- **완료 기준:** plug-in prediction이 버리는 불확실성을 설명한다.
- **시간/선수:** 120분 / S15–S16.

## S18. Bayesian decision과 MAP regularization

- **중심 질문:** 예측분포에서 행동은 어떻게 정하며 prior는 왜 penalty가 되는가?
- **MLAPP 참고 범위:** Ch.5 decision theory/MAP 관련 선택 절(판본 절 확인).
- **큰 그림:** posterior predictive와 loss $L(a,y)$에서 $a^*=\arg\min_a E[L(a,Y)]$; $-\log p(\theta)$는 penalty.
- **먼저 할 손수학:** 비대칭 2-class cost의 threshold, Gaussian prior에서 L2 항을 유도한다.
- **직접 구현:** expected loss/action, MAP objective와 NumPy GD; PyTorch optimizer와 비교한다.
- **새 코딩 지식:** cost matrix, argmin axis, objective component logging.
- **연결:** miss/false-alarm 비용; weight decay와 운영 threshold.
- **검증:** 비용 변화 시 action 변화, analytic MAP/GD 일치를 확인한다.
- **완료 기준:** prior variance, regularization coefficient, learning rate의 층위를 구분한다.
- **시간/선수:** 120분 / S17.
