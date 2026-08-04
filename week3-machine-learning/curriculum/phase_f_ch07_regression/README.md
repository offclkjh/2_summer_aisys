# Phase F — Ch.7 선형회귀

## Phase 계약

- **MLAPP 범위:** Ch.7 linear regression. 세부 절은 소유 판본에서 확인한다.
- **필요한 수학:** matrix calculus, least squares, Gaussian likelihood, basis function, condition number.
- **코딩 지식:** NumPy `@`, `lstsq`, `solve`, feature matrix; PyTorch parameter/autograd/optimizer.
- **구현 경계:** prediction, SSE/NLL, gradient, ridge와 Bayesian posterior 식을 직접 구현한다. 안정적인 factorization은 라이브러리에 맡긴다.
- **객체 템플릿:** $D=(X,y)$, $z$는 필요 시 latent clean output, $\theta=w$와 noise variance, $\alpha$는 basis/regularization/prior, $a$는 point/predictive estimate.
- **다음 Phase로 넘길 결과:** NumPy와 PyTorch가 일치하는 학습 loop, split된 회귀 평가, predictive uncertainty.

## S24. 선형회귀의 생성 가정

- **중심 질문:** squared error 뒤에는 어떤 확률가정이 숨어 있는가?
- **MLAPP 참고 범위:** Ch.7 linear regression likelihood(판본 절 확인).
- **큰 그림:** $y=Xw+\epsilon$, $\epsilon\sim\mathcal N(0,\sigma^2I)$.
- **먼저 할 손수학:** scalar/2-feature prediction shape와 Gaussian NLL→SSE를 전개한다.
- **직접 구현:** design matrix, prediction, residual, SSE/NLL; `nn.Linear` forward와 대조한다.
- **새 코딩 지식:** intercept column, `[N,d]@[d]`, batch reduction.
- **연결:** sensor calibration/FIR coefficient; DNN affine layer.
- **검증:** synthetic noiseless/noisy data와 shape assertion을 사용한다.
- **완료 기준:** iid·linearity·homoscedastic Gaussian 가정을 열거한다.
- **시간/선수:** 120분 / S08.

## S25. 최소제곱과 수치 안정성

- **중심 질문:** 최소제곱 해를 왜 explicit inverse 없이 구하는가?
- **MLAPP 참고 범위:** Ch.7 least squares estimation(판본 절 확인).
- **큰 그림:** normal equation $X^TXw=X^Ty$와 수치 solver.
- **먼저 할 손수학:** 작은 full-rank $X$의 normal equation을 푼다.
- **직접 구현:** normal-equation `solve`, `lstsq`, condition number 비교.
- **새 코딩 지식:** rank, singular value, residual output 계약.
- **연결:** sinusoid amplitude/system identification; closed-form baseline.
- **검증:** ill-conditioned basis에서 inverse/solve/lstsq 오차를 비교한다.
- **완료 기준:** algebraic 동치와 numerical 동치가 다름을 설명한다.
- **시간/선수:** 120분 / S24.

## S26. Gradient descent와 PyTorch

- **중심 질문:** 손으로 유도한 gradient와 autograd가 같은 계산을 하는가?
- **MLAPP 참고 범위:** Ch.7 optimization 관련 절(판본 절 확인).
- **큰 그림:** forward→loss→gradient→update의 상태 변화를 추적한다.
- **먼저 할 손수학:** $\nabla_w\|Xw-y\|^2=2X^T(Xw-y)$와 한 step을 계산한다.
- **직접 구현:** NumPy GD, finite difference; 동일 초기값의 PyTorch one-step을 원소별 비교한다.
- **새 코딩 지식:** `requires_grad`, `.grad`, `zero_grad`, `no_grad`, optimizer state.
- **연결:** adaptive filter; DNN training loop.
- **검증:** gradient check와 S25 해로의 수렴을 확인한다.
- **완료 기준:** `backward()`와 optimizer의 책임을 분리해 말한다.
- **시간/선수:** 120분 / S25.

## S27. Basis expansion과 overfitting

- **중심 질문:** feature 표현력 증가는 언제 일반화를 해치는가?
- **MLAPP 참고 범위:** Ch.7 basis functions/model selection(판본 절 확인).
- **큰 그림:** 고정 $\phi(x)$로 $X_\phi$, 학습 파라미터 $w$, validation으로 basis hyperparameter 선택.
- **먼저 할 손수학:** polynomial/Fourier feature의 각 열과 parameter 수를 적는다.
- **직접 구현:** basis builder, train/validation curves, degree selection.
- **새 코딩 지식:** feature factory, pipeline fit/transform 분리.
- **연결:** Fourier basis와 고정 filter bank; learned representation과 대조.
- **검증:** train error 감소와 validation U-shape, leakage 없는 scaling을 확인한다.
- **완료 기준:** feature map과 weight 학습을 구분한다.
- **시간/선수:** 120분 / S23,S25.

## S28. Ridge·MAP·Bayesian linear regression

- **중심 질문:** L2 점추정과 weight posterior는 무엇을 공유하고 무엇이 다른가?
- **MLAPP 참고 범위:** Ch.7 regularized/Bayesian linear regression(판본 절 확인).
- **큰 그림:** Gaussian prior $p(w\mid\alpha)$, MAP와 $p(w\mid D)$, predictive.
- **먼저 할 손수학:** 1D ridge/MAP, posterior precision과 mean, predictive variance를 계산한다.
- **직접 구현:** ridge solve, posterior mean/covariance, analytic predictive; PyTorch weight decay MAP와 비교한다.
- **새 코딩 지식:** identity penalty와 intercept 제외, matrix RHS, covariance propagation.
- **연결:** noisy filter shrinkage·coefficient uncertainty; Bayesian last layer.
- **검증:** MAP/posterior mean 일치 조건, posterior weight 표본의 predictive moment를 analytic 식과 비교한다.
- **완료 기준:** observation noise와 parameter uncertainty 항을 분해한다.
- **시간/선수:** 120분 / S16,S18,S27.

## S29. System identification 통합

- **중심 질문:** OLS, ridge, Bayesian 회귀는 noisy FIR 추정에서 어떻게 다른가?
- **MLAPP 참고 범위:** Ch.7 개념 통합; 직접 적용 범위(판본 절 확인).
- **큰 그림:** 입력→unknown FIR $w$→noise→output, posterior predictive→평가 action.
- **먼저 할 손수학:** convolution을 Toeplitz/design matrix 곱으로 바꾼다.
- **직접 구현:** synthetic signal, OLS/ridge/Bayes, held-out RMSE와 predictive interval; PyTorch OLS 학습을 baseline으로 둔다.
- **새 코딩 지식:** sliding windows, time-aware split, experiment table.
- **연결:** FIR identification 자체; linear layer가 같은 행렬연산임을 확인.
- **검증:** true coefficient recovery, independent test, interval coverage, SNR sweep.
- **완료 기준:** 모델별 실패를 bias·variance·uncertainty 관점으로 설명한다.
- **시간/선수:** 120분 / S23,S28.
