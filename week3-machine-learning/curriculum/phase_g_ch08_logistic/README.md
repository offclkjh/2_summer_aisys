# Phase G — Ch.8.1–8.3 Logistic regression

## Phase 계약

- **MLAPP 범위:** Ch.8.1–8.3. 해당 판본의 실제 제목과 포함 모델을 시작 전에 확인한다.
- **필요한 수학:** sigmoid/logit, Bernoulli/categorical NLL, chain rule, convexity 직관, decision cost.
- **코딩 지식:** stable elementwise function, gradient check, minibatch, `nn.Linear`, metric binning.
- **구현 경계:** sigmoid/log-softmax, logits-based loss, analytic gradient, metric을 직접 구현한다. autograd/optimizer와 library loss는 대조에 쓴다.
- **객체 템플릿:** $D=(X,y)$, $z$는 필요 시 hidden representation, $\theta=(W,b)$, $\alpha$는 regularization/calibration 설정, $a$는 threshold 기반 class action.
- **다음 Phase로 넘길 결과:** stable classifier, calibrated probability 평가, feature/model/decision 오류 분해.

## S30. Sigmoid와 Bernoulli conditional model

- **중심 질문:** 선형 score를 유효한 확률로 어떻게 바꾸는가?
- **MLAPP 참고 범위:** Ch.8.1 binary logistic regression(판본 절 확인).
- **큰 그림:** $p(y=1\mid x,\theta)=\sigma(w^Tx+b)$.
- **먼저 할 손수학:** log-odds와 sigmoid 역관계, 작은 sample likelihood를 계산한다.
- **직접 구현:** stable sigmoid, logits, probability/BCE; `nn.Linear` forward와 대조한다.
- **새 코딩 지식:** logits vs probabilities, decision boundary shape.
- **연결:** energy feature detector; binary DNN output head.
- **검증:** extreme score, $\sigma(-z)=1-\sigma(z)$, 확률 범위를 확인한다.
- **완료 기준:** linear regression 출력을 그대로 확률로 쓰지 못하는 이유를 말한다.
- **시간/선수:** 120분 / S05,S24.

## S31. Stable binary cross-entropy

- **중심 질문:** 큰 절댓값 logit에서도 loss를 유한하고 정확하게 계산하는가?
- **MLAPP 참고 범위:** Ch.8.1 likelihood/objective(판본 절 확인).
- **큰 그림:** Bernoulli NLL을 probability가 아닌 logit에서 계산한다.
- **먼저 할 손수학:** $\log(1+e^z)-yz$ 형태를 유도한다.
- **직접 구현:** naive/stable BCE-with-logits; PyTorch `BCEWithLogitsLoss`와 대조한다.
- **새 코딩 지식:** softplus/logaddexp, reduction 계약.
- **연결:** low/high SNR detector score; stable DNN loss.
- **검증:** $z=\pm1000$, 여러 shape/reduction에서 값·gradient를 확인한다.
- **완료 기준:** sigmoid+BCE를 분리 계산할 때 생기는 수치 문제를 설명한다.
- **시간/선수:** 120분 / S30.

## S32. Logistic gradient

- **중심 질문:** 왜 gradient가 $X^T(p-y)$이며 autograd와 일치하는가?
- **MLAPP 참고 범위:** Ch.8.1 optimization(판본 절 확인).
- **큰 그림:** conditional likelihood의 gradient로 $\theta$를 학습한다.
- **먼저 할 손수학:** sample별 derivative와 batch matrix form을 유도한다.
- **직접 구현:** analytic gradient, finite difference, NumPy GD; PyTorch one-step과 비교한다.
- **새 코딩 지식:** gradient norm, convergence trace, detach.
- **연결:** discriminative detector adaptation; output error가 backprop되는 첫 사례.
- **검증:** 세 gradient의 tolerance와 loss 감소를 확인한다.
- **완료 기준:** `p-y`의 부호와 update 방향을 sample 수준에서 해석한다.
- **시간/선수:** 120분 / S26,S31.

## S33. Multiclass softmax regression

- **중심 질문:** binary conditional model을 $K$ class로 어떻게 일반화하는가?
- **MLAPP 참고 범위:** Ch.8.2–8.3 중 multiclass logistic 부분(판본 절 확인).
- **큰 그림:** logits $Z=XW+b\in\mathbb R^{N\times K}$와 categorical likelihood.
- **먼저 할 손수학:** 3-class log-softmax/NLL과 gradient의 구조를 계산한다.
- **직접 구현:** stable log-softmax, gather NLL, prediction; PyTorch cross-entropy와 비교한다.
- **새 코딩 지식:** `[N,K]`, class dimension, integer target contract.
- **연결:** modulation/noise-state classification; multiclass DNN head.
- **검증:** shift invariance, probability 합, one-hot 식과 일치함을 확인한다.
- **완료 기준:** batch와 class reduction 축을 설명한다.
- **시간/선수:** 120분 / S04,S32.

## S34. Regularized logistic regression

- **중심 질문:** separable data에서 weight가 커지는 현상을 prior가 어떻게 제어하는가?
- **MLAPP 참고 범위:** Ch.8.1–8.3 regularization 관련 절(판본 절 확인).
- **큰 그림:** likelihood+Gaussian prior의 MAP, $\alpha$는 weight scale 가정.
- **먼저 할 손수학:** BCE+L2 objective와 gradient를 쓰고 intercept 처리 여부를 정한다.
- **직접 구현:** regularized NumPy optimizer, validation sweep; PyTorch weight decay와 설정을 맞춰 비교한다.
- **새 코딩 지식:** parameter groups, selective penalty, early-stop 기록.
- **연결:** 적은 labeled signal의 detector; DNN weight decay.
- **검증:** separable data의 norm/loss trace와 validation 선택을 확인한다.
- **완료 기준:** training loss와 parameter norm의 tradeoff를 설명한다.
- **시간/선수:** 120분 / S18,S32.

## S35. Calibration·threshold와 decision

- **중심 질문:** accuracy가 같아도 확률 품질과 운영 행동이 왜 달라지는가?
- **MLAPP 참고 범위:** Ch.8 예측 평가와 Ch.5 decision 연결(판본 절 확인).
- **큰 그림:** $p(y\mid x,D)$를 NLL/Brier/calibration으로 평가하고 cost로 $a$를 정한다.
- **먼저 할 손수학:** 작은 예측 목록의 NLL, Brier, confusion cost와 최적 threshold를 계산한다.
- **직접 구현:** reliability bins/ECE, ROC·PR points, expected cost; library metric과 대조한다.
- **새 코딩 지식:** threshold sweep, bin edge, class imbalance.
- **연결:** rare anomaly의 false alarm/miss; confidence calibration과 deployment threshold.
- **검증:** 동일 accuracy·다른 NLL 사례, base-rate 변화, endpoint를 확인한다.
- **완료 기준:** ROC-AUC가 운영 threshold를 정해주지 않는 이유를 말한다.
- **시간/선수:** 120분 / S17,S21,S33.

## S36. 신호분류 통합

- **중심 질문:** 성능 실패를 feature, model, probability, decision 층으로 구분할 수 있는가?
- **MLAPP 참고 범위:** Ch.8.1–8.3 통합 적용(판본 절 확인).
- **큰 그림:** signal→feature/raw $X$→conditional model→probability→cost action.
- **먼저 할 손수학:** sinusoid/noise 생성가정과 class conditional 차이를 명시한다.
- **직접 구현:** synthetic signal, binary/multiclass logistic, held-out NLL/calibration/cost; 동일 `nn.Linear` 모델과 비교한다.
- **새 코딩 지식:** reproducible dataset, metric report, error slicing by SNR.
- **연결:** 신호분류 전체 pipeline; PyTorch classifier의 최소 완결형.
- **검증:** grouped independent split, NumPy/Torch prediction 일치, SNR별 결과를 확인한다.
- **완료 기준:** 실패 사례 세 개를 서로 다른 층의 원인으로 진단한다.
- **시간/선수:** 120분 / S23,S34–S35.
