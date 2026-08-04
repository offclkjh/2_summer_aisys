# Phase B — Ch.3 이산 생성모형

## Phase 계약

- **MLAPP 범위:** Ch.3 discrete generative models. 정확한 절은 판본 목차에서 확인한다.
- **필요한 수학:** 곱을 log 합으로 바꾸기, 조합계수, Lagrange multiplier의 직관, Bayes rule.
- **코딩 지식:** NumPy boolean sum, `bincount`, indexing, grid; PyTorch distribution API는 검산에만 사용.
- **구현 경계:** PMF, log-likelihood, MLE, conjugate update와 predictive를 직접 구현한다. 난수·특수함수는 라이브러리에 맡긴다.
- **객체 템플릿:** $D$는 시행/범주 또는 count, $z$는 필요 시 class, $\theta$는 probability simplex, $\alpha$는 prior count, $a$는 예측/분류 행동.
- **다음 Phase로 넘길 결과:** 시행과 count 데이터 구분, 안정적인 이산 log-likelihood, 생성분류의 joint→posterior 경로.

## S05. Bernoulli·Binomial

- **중심 질문:** 개별 시행과 집계 count의 likelihood는 어떻게 연결되는가?
- **MLAPP 참고 범위:** Ch.3 Bernoulli/Binomial(판본 절 확인).
- **큰 그림:** $D=(x_1,\ldots,x_N)$, $\theta=P(x=1)$, sufficient statistic $s=\sum x_i$.
- **먼저 할 손수학:** $[1,0,1]$의 PMF, likelihood, log-likelihood와 $\hat\theta=s/N$을 유도한다.
- **직접 구현:** PMF/NLL/grid/MLE를 NumPy와 tensor 기본연산으로 작성한다.
- **새 코딩 지식:** boolean validation, scalar broadcasting, boundary-safe log.
- **연결:** bit/packet error rate; binary label likelihood와 BCE의 출발점.
- **검증:** grid 최대, 폐형식 MLE, PyTorch distribution 결과를 비교한다.
- **완료 기준:** likelihood가 일반적으로 $\theta$에 대해 정규화된 분포가 아님을 설명한다.
- **시간/선수:** 120분 / S02–S03.

## S06. Categorical·Multinomial

- **중심 질문:** 단일 범주 관측과 count vector는 어떤 likelihood를 갖는가?
- **MLAPP 참고 범위:** Ch.3 categorical/multinomial(판본 절 확인).
- **큰 그림:** $D=(y_i)$ 또는 $n=(n_1,\ldots,n_K)$, $\theta\in\Delta^{K-1}$.
- **먼저 할 손수학:** 3-class 표본의 count, MLE, categorical과 multinomial likelihood의 상수항 차이를 계산한다.
- **직접 구현:** `bincount`, simplex validation, log-likelihood, MLE; Torch tensor indexing과 대조한다.
- **새 코딩 지식:** integer labels, one-hot, `[N,K]`와 `[K]`, `lgamma`.
- **연결:** 양자화 심볼 histogram; class prior와 multiclass NLL.
- **검증:** 원자료 순서를 바꿔도 count likelihood의 parameter-dependent 부분이 같은지 확인한다.
- **완료 기준:** categorical sample과 multinomial count의 데이터 단위를 구분한다.
- **시간/선수:** 120분 / S04–S05.

## S07. Dirichlet과 생성분류

- **중심 질문:** prior count가 희소한 범주의 posterior prediction을 어떻게 바꾸는가?
- **MLAPP 참고 범위:** Ch.3 Dirichlet-multinomial 및 discrete generative classifier(판본 절 확인).
- **큰 그림:** $\theta\sim\mathrm{Dir}(\alpha)$, class별 $p(x\mid y,\theta)$와 $p(y)$에서 $p(y\mid x)$를 만든다.
- **먼저 할 손수학:** posterior $\alpha'_k=\alpha_k+n_k$, posterior mean과 predictive를 작은 count로 계산한다.
- **직접 구현:** update, posterior predictive, log-joint 기반 categorical naive Bayes; PyTorch/Scipy 분포는 검산만 한다.
- **새 코딩 지식:** class-feature count table, vectorized log-joint, unseen category 처리.
- **연결:** symbol 상태 분류; smoothing, class prior, label smoothing과의 차이.
- **검증:** 순차/일괄 update 일치, predictive 합 1, unseen category에서 유한값을 확인한다.
- **완료 기준:** smoothing을 임의의 0 방지가 아니라 prior 가정으로 설명한다.
- **시간/선수:** 120분 / S06.
