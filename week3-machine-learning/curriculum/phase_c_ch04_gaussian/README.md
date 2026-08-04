# Phase C — Ch.4 Gaussian 모델

## Phase 계약

- **MLAPP 범위:** Ch.4 Gaussian models. 절 번호는 소유 판본에서 확인한다.
- **필요한 수학:** 미분, 벡터·행렬 곱, determinant, positive definiteness, eigenvector의 기하, block matrix 직관.
- **코딩 지식:** NumPy `@`, transpose, broadcasting, covariance; PyTorch linear algebra와 autograd.
- **구현 경계:** 1D/다변량 log-density와 MLE 식을 직접 구성한다. inverse·determinant를 직접 알고리즘으로 만들지 않고 `solve`, `slogdet`, Cholesky에 맡긴다.
- **객체 템플릿:** $D=X\in\mathbb R^{N\times d}$, $z/y$는 class 또는 미관측 채널, $\theta=(\mu,\Sigma)$, $\alpha$는 고정 regularizer, $a$는 추정/분류.
- **다음 Phase로 넘길 결과:** covariance 기하, stable Gaussian log-density, Gaussian conditioning과 생성분류 구현.

## S08. 1차원 Gaussian

- **중심 질문:** MSE가 Gaussian NLL과 같아지는 가정은 무엇인가?
- **MLAPP 참고 범위:** Ch.4 univariate Gaussian과 MLE(판본 절 확인).
- **큰 그림:** $x_i\sim\mathcal N(\mu,\sigma^2)$, $D$로 $\theta=(\mu,\sigma^2)$를 추정한다.
- **먼저 할 손수학:** log-density, $\hat\mu$, 두 분산 추정량을 작은 표본으로 계산한다.
- **직접 구현:** density/NLL/MLE; PyTorch autograd로 $\mu$ 최적화 후 폐형식과 대조한다.
- **새 코딩 지식:** parameter constraint, log-variance parameterization, reduction.
- **연결:** additive Gaussian noise·SNR; fixed variance 회귀의 MSE loss.
- **검증:** 정규화 수치적분, 폐형식/optimizer 일치, 분산 convention을 확인한다.
- **완료 기준:** iid·Gaussian·constant variance 가정을 명시한다.
- **시간/선수:** 120분 / S03.

## S09. Vector와 covariance

- **중심 질문:** covariance matrix는 데이터의 방향과 scale을 어떻게 표현하는가?
- **MLAPP 참고 범위:** Ch.4 multivariate moments와 geometry(판본 절 확인).
- **큰 그림:** $x_i\in\mathbb R^d$, $\mu\in\mathbb R^d$, $\Sigma\in\mathbb R^{d\times d}$.
- **먼저 할 손수학:** 2D 자료를 center하고 outer product로 covariance를 계산한다; $AX+b$의 moment를 유도한다.
- **직접 구현:** covariance 정의식, correlation, 선형변환; NumPy/PyTorch 내장 함수와 비교한다.
- **새 코딩 지식:** `[N,d]` centering, outer product, transpose conventions.
- **연결:** 다채널 colored noise·whitening; feature covariance와 normalization.
- **검증:** symmetry, PSD eigenvalue, $\mathrm{Cov}(AX)=A\Sigma A^T$를 확인한다.
- **완료 기준:** covariance 원소와 주축의 의미를 그림 없이 설명한다.
- **시간/선수:** 120분 / S03,S08.

## S10. Multivariate Gaussian 계산

- **중심 질문:** inverse와 underflow 없이 Gaussian log-density를 어떻게 계산하는가?
- **MLAPP 참고 범위:** Ch.4 multivariate Gaussian density(판본 절 확인).
- **큰 그림:** residual, Mahalanobis term, log determinant가 sample log-density를 구성한다.
- **먼저 할 손수학:** diagonal $2\times2$ covariance에서 Mahalanobis distance와 log-density를 계산한다.
- **직접 구현:** `solve`/Cholesky 기반 batched log-density; PyTorch `MultivariateNormal`과 대조한다.
- **새 코딩 지식:** `slogdet`, triangular solve, batch dimension, jitter.
- **연결:** colored-noise matched distance; multivariate regression head.
- **검증:** diagonal case를 1D 합과 비교하고 ill-conditioned covariance 실패를 재현한다.
- **완료 기준:** 명시적 inverse가 불리한 이유와 jitter의 가정 변화를 말한다.
- **시간/선수:** 120분 / S09.

## S11. Gaussian conditioning과 marginalization

- **중심 질문:** 일부 변수를 관측하면 나머지 평균과 불확실성은 어떻게 변하는가?
- **MLAPP 참고 범위:** Ch.4 marginals/conditionals of Gaussian(판본 절 확인).
- **큰 그림:** $x=(x_a,x_b)$의 block $\mu,\Sigma$에서 $p(x_a\mid x_b)$를 구한다.
- **먼저 할 손수학:** 2D block formula로 conditional mean/variance를 계산한다.
- **직접 구현:** block slicing, marginal/conditional parameters; joint density ratio와 대조한다.
- **새 코딩 지식:** block indexing, solve의 다중 RHS, shape 보존.
- **연결:** 관측 센서로 누락 채널 추정; Gaussian posterior/attention의 조건화 직관.
- **검증:** conditional covariance가 관측값 자체에는 의존하지 않으며 PSD인지 확인한다.
- **완료 기준:** correlation이 없을 때 관측이 예측을 바꾸지 않는 이유를 설명한다.
- **시간/선수:** 120분 / S10.

## S12. Gaussian 생성분류

- **중심 질문:** shared/class-specific covariance가 decision boundary를 어떻게 바꾸는가?
- **MLAPP 참고 범위:** Ch.4 Gaussian discriminant analysis, LDA/QDA(판본 절 확인).
- **큰 그림:** $p(y)p(x\mid y,\theta_y)$에서 log-joint와 $p(y\mid x)$를 계산한다.
- **먼저 할 손수학:** 1D 두 Gaussian의 log-joint 차와 경계; shared covariance의 이차항 소거를 확인한다.
- **직접 구현:** class prior, mean/covariance MLE, stable posterior, LDA/QDA prediction; 라이브러리와 비교한다.
- **새 코딩 지식:** class mask, per-class parameters, log-sum-exp.
- **연결:** tone/noise-state 검출; generative와 discriminative classifier 비교.
- **검증:** probability 합, shared covariance의 선형 경계, held-out NLL을 확인한다.
- **완료 기준:** 작은 표본에서 QDA covariance가 불안정한 이유를 말한다.
- **시간/선수:** 120분 / S10.
