# S08 답안
## T1. 실행 전 예측
- **T1-1** candidate/data mean 비교:cand가 작네
- **T1-2** 더 작은 SSE/NLL: cand가 큼
- **T1-3** 두 variance 비교: 같을 이유가 딱히 없음. 실제로 다름
## T2. 손계산
- **T2-1** residual/squared/SSE:skip residuals, SSE: 2.75
- **T2-2** log-density/NLL:skip density, NLL: 1/2*(3log(4pi)+1.375)
- **T2-3** mean MLE/SSE: 2, 2
- **T2-4** variance MLE/unbiased variance: 2/3, 1, 자유도 차이로 mle가 더 작음
## T3. 직접 구현
- **T3-1** gaussian_logpdf:
- **T3-2** gaussian_nll:
- **T3-3** squared_error_sum:
- **T3-4** gaussian_mean_mle:
- **T3-5** gaussian_variance_mle:
## T4. 표준 API 참조 (선택, 작성 없음)
## T5. 잘못된 해석
- **T5-1** sigma/variance: 
- **T5-2** MLE의 n-1: mle의 의미 왜곡, 알고 있는 데이터의 분산이 그게 아님.
- **T5-3** 변하는 variance: fixed에서만 보장가능
## T6. 설명 확인
- **T6-1** residual penalty:두번째 항으로, 평균과 실제 데이터 간 거리가 클수록 더 높은 error를 부여한다.
- **T6-2** 같은 minimizer:의미상, 데이터 분포를 가장 잘 설명하는 가우시안 분포의 중심점과, 주어진 데이터의 실제 표본평균이기 때문.
- **T6-3** 두 variance의 목적: MLE는 현 데이터를 가장 잘 설명하는 것이고, unbiased는 평균이란 parameter로 자유도 하나만큼 이미 예측했기에 그만큼 보수적인 분산을 잡는 것이다.
