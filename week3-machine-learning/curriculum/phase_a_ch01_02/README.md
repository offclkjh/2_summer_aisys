# Phase A — Ch.1–2 확률 언어와 계산 객체

## Phase 계약

- **MLAPP 범위:** Ch.1–2. 절 번호는 소유 판본 목차에서 세션 시작 전에 확인한다.
- **필요한 수학:** 합·곱 법칙, 조건부확률, Bayes rule, 합 기호, 로그, 벡터 내적.
- **코딩 지식:** Python 함수·반복·assert, NumPy `shape`, `dtype`, indexing, broadcasting, `axis` reduction; PyTorch tensor와 reduction 기초.
- **구현 경계:** 작은 joint table, normalization, moment, entropy 식은 직접 구현한다. 난수와 그래프는 라이브러리에 맡긴다.
- **객체 템플릿:** $D=(x_i,y_i)$는 관측, $z$는 잠재, $\theta$는 모델 파라미터, $\alpha$는 고정 hyperparameter, $a$는 action이다. 각 실습에서 의미·shape·고정/학습 여부를 채운다.
- **다음 Phase로 넘길 결과:** 확률식의 축과 객체를 표시한 노트, 안정적인 log 계산 함수, shape 검증 습관.

## S01. 확률모형의 객체와 shape

- **중심 질문:** 무엇이 관측·잠재·학습·고정 객체이며 배열에서 어느 축인가?
- **MLAPP 참고 범위:** Ch.1 모델링 개요 및 Ch.2 notation(판본 절 확인).
- **큰 그림:** $D,x,y,z,\theta,\alpha,a$를 모델→추론→예측→결정 흐름에 배치한다.
- **먼저 할 손수학:** 동전, noisy sensor, linear layer 사례의 객체와 scalar/vector/matrix shape를 표로 쓴다.
- **직접 구현:** NumPy 입력 계약과 shape assertion; 같은 데이터를 PyTorch tensor로 옮겨 값·shape·dtype를 대조한다.
- **새 코딩 지식:** 함수 signature, tuple shape, dtype/device, 명시적 batch 축.
- **연결:** 신호처리의 `[batch,time,channel]`; DNN의 input·label·weight와 activation 구분.
- **검증:** 잘못된 축과 dtype을 의도적으로 넣어 assertion이 잡는지 확인한다.
- **완료 기준:** 새 문제의 객체와 shape를 2분 안에 설명하고 코드 주석으로 남긴다.
- **시간/선수:** 120분 / 없음.
- **S01 산출물:** [워크시트](S01_NOTES.md) · [스켈레톤](s01_objects_and_shapes.py) · [계약 테스트](test_s01_objects_and_shapes.py)
- **실행(Phase 디렉터리):** `../../../.venv/bin/python s01_objects_and_shapes.py` · `../../../.venv/bin/python -m unittest -v test_s01_objects_and_shapes.py` (TODO 구현 전 실패가 정상)

## S02. Joint·marginal·conditional·Bayes

- **중심 질문:** joint table에서 어떤 축을 합하고 무엇으로 정규화하는가?
- **MLAPP 참고 범위:** Ch.2 joint, marginal, conditional probability와 Bayes rule(판본 절 확인).
- **큰 그림:** $p(x,z\mid\theta)$에서 $p(x)$와 $p(z\mid x)$를 얻는다.
- **먼저 할 손수학:** $2\times2$ table의 marginal, conditional, Bayes posterior를 계산한다.
- **직접 구현:** `sum(axis=...)`, conditional normalization, 독립성 검사; PyTorch reduction으로 같은 결과를 낸다.
- **새 코딩 지식:** `axis/dim`, `keepdims`, broadcasting division.
- **연결:** 실제 상태와 detector 출력; DNN의 $p(y\mid x,\theta)$.
- **검증:** 합이 1인지, Bayes 식 양변이 일치하는지 assert한다.
- **완료 기준:** axis 선택을 수식의 합산 변수와 연결해 설명한다.
- **시간/선수:** 120분 / S01.

## S03. 기대값·분산·공분산

- **중심 질문:** 분포의 moment와 유한 표본 통계량은 어떻게 다른가?
- **MLAPP 참고 범위:** Ch.2 expectation, variance, covariance(판본 절 확인).
- **큰 그림:** $p(x\mid\theta)$의 요약량과 $D$의 요약량을 분리한다.
- **먼저 할 손수학:** 작은 이산분포의 $E[X]$, $\mathrm{Var}(X)$, $\mathrm{Cov}(X,Y)$를 정의식으로 계산한다.
- **직접 구현:** weighted moment와 sample moment; NumPy/PyTorch 내장 결과와 비교한다.
- **새 코딩 지식:** weighted sum, centering, outer product, `ddof` 의미.
- **연결:** 잡음 전력·채널 covariance; activation 통계와 normalization.
- **검증:** 분포에서 생성한 표본 수가 늘 때 이론값에 접근하는지 확인하되 별도 주제로 만들지 않는다.
- **완료 기준:** population/sample variance의 분모 차이와 사용 맥락을 말한다.
- **시간/선수:** 120분 / S02.

## S04. Entropy·cross-entropy·KL

- **중심 질문:** 분류 cross-entropy가 왜 categorical NLL인가?
- **MLAPP 참고 범위:** Ch.2 information theory(판본 절 확인).
- **큰 그림:** 참 분포 $p$, 모델 $q_\theta$, 관측 label의 NLL을 연결한다.
- **먼저 할 손수학:** 3-class $H(p)$, $H(p,q)$, $D_{KL}(p\|q)$ 및 $H(p,q)=H(p)+D_{KL}$을 계산한다.
- **직접 구현:** entropy, cross-entropy, KL, stable log-softmax; PyTorch `log_softmax`/`cross_entropy`와 대조한다.
- **새 코딩 지식:** clipping의 한계, max-shift, gather/indexing.
- **연결:** symbol·spectral entropy; logits→log-softmax→NLL.
- **검증:** one-hot과 soft target, 큰 logit에서 유한값과 동일 결과를 확인한다.
- **완료 기준:** softmax를 `CrossEntropyLoss` 앞에 적용하지 않는 이유를 수치 안정성과 API 계약으로 설명한다.
- **시간/선수:** 120분 / S02.
