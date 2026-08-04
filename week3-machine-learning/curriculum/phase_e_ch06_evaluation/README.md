# Phase E — Ch.6 추정과 평가

## Phase 계약

- **MLAPP 범위:** Ch.6의 frequentist inference/model evaluation 관련 실제 절을 판본 목차에서 확인한다.
- **필요한 수학:** estimator, expectation, standard error, quantile, null distribution, risk.
- **코딩 지식:** 반복 실험, resampling, index split, seed 관리, 결과 집계.
- **구현 경계:** coverage, bootstrap/permutation의 핵심 loop와 split index를 직접 구현한다. 분위수·선형대수·검정 reference 결과는 라이브러리에 맡긴다.
- **객체 템플릿:** $D$는 반복 가능한 표본, $\theta$는 고정된 data-generating parameter, $\hat\theta(D)$는 random estimator, $z$는 resample index, $\alpha$는 유의수준/설정, $a$는 채택·선택.
- **다음 Phase로 넘길 결과:** leakage 없는 평가 protocol, estimator uncertainty와 모델 비교 보고서 형식.

## S19. Sampling distribution과 standard error

- **중심 질문:** 반복 표본에서 무엇이 고정되고 무엇이 변하는가?
- **MLAPP 참고 범위:** Ch.6 sampling distribution/estimation(판본 절 확인).
- **큰 그림:** 고정 $\theta$, 반복 $D^{(r)}$, 변하는 $\hat\theta(D^{(r)})$.
- **먼저 할 손수학:** Bernoulli mean estimator의 expectation, variance, SE를 유도한다.
- **직접 구현:** 반복 데이터와 estimator distribution; NumPy/PyTorch reduction 비교.
- **새 코딩 지식:** RNG 객체, simulation/result axis, vectorized repetition.
- **연결:** 반복 측정의 error-rate; 여러 training run의 metric 변동.
- **검증:** $N$ 증가에 따른 SE의 $1/\sqrt N$ scaling을 확인한다.
- **완료 기준:** parameter와 estimator에 붙는 확률을 구분한다.
- **시간/선수:** 120분 / S05,S08.

## S20. Bias·variance와 estimator risk

- **중심 질문:** unbiased estimator가 항상 최소 오차인가?
- **MLAPP 참고 범위:** Ch.6 bias-variance/risk(판본 절 확인).
- **큰 그림:** $E[(\hat\theta-\theta)^2]=\mathrm{Bias}^2+\mathrm{Var}$.
- **먼저 할 손수학:** Gaussian mean과 shrinkage estimator의 bias/variance/MSE를 계산한다.
- **직접 구현:** shrinkage sweep과 empirical decomposition; analytic 값과 비교한다.
- **새 코딩 지식:** broadcasting parameter grid, metric decomposition.
- **연결:** noisy coefficient shrinkage; DNN regularization의 bias-variance tradeoff.
- **검증:** 양변의 수치 일치와 최적 shrinkage가 조건에 따라 변함을 확인한다.
- **완료 기준:** bias를 허용해 risk를 줄이는 조건을 설명한다.
- **시간/선수:** 120분 / S19.

## S21. Confidence interval과 credible interval

- **중심 질문:** 두 95% 구간이 말하는 확률은 왜 다른가?
- **MLAPP 참고 범위:** Ch.6 confidence interval 관련 절 및 Ch.5와 대조(판본 절 확인).
- **큰 그림:** frequentist procedure의 coverage와 Bayesian posterior mass를 분리한다.
- **먼저 할 손수학:** 알려진 분산 Gaussian mean CI와 S15 credible interval 문장을 비교한다.
- **직접 구현:** CI와 반복 coverage; Bayesian interval 함수 결과를 나란히 표로 만든다.
- **새 코딩 지식:** boolean coverage aggregation, quantile API.
- **연결:** 평균 신호 수준의 장기 보장; model metric uncertainty.
- **검증:** 여러 $\theta,N$에서 coverage를 확인한다.
- **완료 기준:** 관측된 frequentist interval에 parameter 확률을 부여하지 않는다.
- **시간/선수:** 120분 / S15,S19.

## S22. Bootstrap과 hypothesis testing

- **중심 질문:** 닫힌형 SE가 없을 때 uncertainty와 차이를 어떻게 평가하는가?
- **MLAPP 참고 범위:** Ch.6 bootstrap/testing 관련 실제 절(판본 절 확인).
- **큰 그림:** resample index $z$와 null 아래 재배열로 statistic distribution을 만든다.
- **먼저 할 손수학:** p-value를 $p(D\mid H_0)$ 계열의 tail probability로 쓰고 $p(H_0\mid D)$와 구분한다.
- **직접 구현:** median bootstrap CI, paired permutation/sign-flip test; reference library와 비교한다.
- **새 코딩 지식:** resampling indices, paired axis, empirical quantile.
- **연결:** spectral centroid·전후 SNR; 두 모델의 paired metric 차이.
- **검증:** Gaussian mean의 analytic SE와 bootstrap, null data의 p-value 분포를 확인한다.
- **완료 기준:** resampling unit이 왜 독립 단위여야 하는지 설명한다.
- **시간/선수:** 120분 / S20–S21.

## S23. Split·CV와 모델 비교

- **중심 질문:** leakage 없이 일반화 성능과 불확실성을 어떻게 비교하는가?
- **MLAPP 참고 범위:** Ch.6 model selection/evaluation 관련 실제 절(판본 절 확인).
- **큰 그림:** train은 $\theta$ 학습, validation은 $\alpha$ 선택, test는 최종 action 평가에 쓴다.
- **먼저 할 손수학:** nested data reuse가 만드는 optimistic bias를 작은 예로 추적한다.
- **직접 구현:** deterministic split/K-fold indices, paired fold comparison, summary CI; sklearn은 결과 검산만 한다.
- **새 코딩 지식:** grouped split, immutable test set, experiment record.
- **연결:** 동일 녹음 frame/화자의 leakage; early stopping과 test 격리.
- **검증:** overlap assertion, label-independent split, leakage 사례의 과대성능을 확인한다.
- **완료 기준:** 모델 선택과 최종 성능추정에 같은 자료를 쓰면 안 되는 이유를 설명한다.
- **시간/선수:** 120분 / S22.
