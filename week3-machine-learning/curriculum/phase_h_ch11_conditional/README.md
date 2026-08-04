# Phase H — Ch.11 일부(범위 확인 후 확정)

## Phase 계약

- **MLAPP 범위:** README의 “Ch.11 일부”만 확정되어 있다. S37에서 소유 판본의 실제 선택 절·제목을 기록한다. 아래 S38–S39는 선택 범위가 latent mixture/EM일 때의 설계이며 다르면 동일 학습 계약으로 교체한다.
- **필요한 수학:** joint/marginal, latent variable, Jensen/기대값의 직관, total expectation/variance.
- **코딩 지식:** log-sum-exp, responsibility matrix, iterative state, convergence trace.
- **구현 경계:** 작은 latent state 열거, responsibility, 한 번의 update를 직접 구현한다. 범용 sampler/optimizer나 대규모 clustering library는 검산에만 쓴다.
- **객체 템플릿:** $D=X$ 관측, $z_i$ component/state, $\theta$ component·mixing parameter, $\alpha$ prior/초기화 설정, $a$는 state prediction/이상 판단.
- **과정 종료 결과:** 선택 범위가 명시된 모델 카드와 joint→inference→predictive→decision capstone.

## S37. 선택 범위 확정과 latent 구조

- **중심 질문:** 실제 선택 절에서 관측·잠재·파라미터는 무엇이며 어떤 inference가 필요한가?
- **MLAPP 참고 범위:** Ch.11의 사용자가 선택한 절—판본·절·제목을 이 문서에 먼저 기록.
- **큰 그림:** $p(D,z,\theta\mid\alpha)$ factorization과 원하는 marginal/posterior/action을 그린다.
- **먼저 할 손수학:** 작은 이산 $z$를 모두 열거해 joint, marginal, posterior를 계산한다.
- **직접 구현:** factor table과 exact sum; 필요 시 PyTorch tensor reduction으로 대조한다.
- **새 코딩 지식:** latent axis, normalized log weight, model-card 기록.
- **연결:** signal frame 뒤의 source/noise state; hidden representation과 probabilistic latent variable의 차이.
- **검증:** joint 합, marginal 합, posterior normalization과 factorization 가정을 확인한다.
- **완료 기준:** 선택 절이 mixture/EM이 아니면 S38–S39의 대체 제목·산출물을 명시한다.
- **시간/선수:** 120분 / S02,S36.

## S38. Mixture와 responsibility (조건부)

- **중심 질문:** soft assignment는 어떤 posterior이며 mixture likelihood는 어떻게 안정적으로 계산하는가?
- **MLAPP 참고 범위:** Ch.11 mixture model 절이 선택 범위에 있을 때만 수행(판본 절 확인).
- **큰 그림:** $z_i\sim\mathrm{Cat}(\pi)$, $x_i\mid z_i=k\sim\mathcal N(\mu_k,\Sigma_k)$, $p(z_i\mid x_i)$.
- **먼저 할 손수학:** 1D two-component 한 점의 log-joint와 responsibility를 계산한다.
- **직접 구현:** component log-density, log-sum-exp marginal, responsibility; library mixture의 score와 대조한다.
- **새 코딩 지식:** `[N,K]` responsibility, component axis, initialization.
- **연결:** 정상/이상 noise regime; soft routing과 mixture-of-experts의 기초.
- **검증:** row 합 1, component swap 불변성, extreme scale에서 유한값을 확인한다.
- **완료 기준:** clustering label이 아니라 posterior assignment임을 설명한다.
- **시간/선수:** 120분 / S10,S37.

## S39. EM과 반복 추론 (조건부)

- **중심 질문:** E/M step은 무엇을 기대하고 무엇을 최적화하는가?
- **MLAPP 참고 범위:** Ch.11 EM 절이 선택 범위에 있을 때만 수행(판본 절 확인).
- **큰 그림:** 현재 $\theta$로 $q(z)$를 구하고 expected complete log-likelihood로 $\theta$를 갱신한다.
- **먼저 할 손수학:** 1D two-component 자료에 한 E-step과 M-step을 수행한다.
- **직접 구현:** 한 step, iteration loop, observed-data likelihood trace; reference implementation과 비교한다.
- **새 코딩 지식:** iterative state copy, tolerance, multiple initialization, empty component guard.
- **연결:** 다중 noise state 분리; alternating optimization의 일반 패턴.
- **검증:** likelihood non-decrease(수치 tolerance), 여러 초기값과 local optimum을 확인한다.
- **완료 기준:** EM이 latent label을 “정답처럼 생성”하는 절차가 아님을 설명한다.
- **시간/선수:** 120분 / S38.

## S40. 전체 capstone

- **중심 질문:** 하나의 신호 문제를 확률모형에서 평가·결정까지 일관되게 설명할 수 있는가?
- **MLAPP 참고 범위:** Ch.1–8 및 확정된 Ch.11 선택 절의 통합.
- **큰 그림:** $D,z,\theta,\alpha,a$, factorization, inference target, predictive, loss를 한 장에 쓴다.
- **먼저 할 손수학:** 작은 데이터 한 건의 likelihood/posterior 또는 objective와 expected decision cost를 계산한다.
- **직접 구현:** chosen latent/no-latent model, deterministic 또는 `nn.Linear` baseline, independent split, predictive/metric/cost report.
- **새 코딩 지식:** experiment configuration, reproducible report, failure taxonomy.
- **연결:** 신호처리 문제 자체를 데이터 생성가정으로 명시; DNN baseline의 출력과 확률모형을 같은 metric으로 비교.
- **검증:** analytic/library/표본 검산 중 적합한 둘, split assertion, ablation 한 개를 수행한다.
- **완료 기준:** 5분 구두 설명과 한 페이지 한계 분석에서 model·inference·prediction·decision을 혼동하지 않는다.
- **시간/선수:** 120분 / S23,S29,S36,S37–S39.
