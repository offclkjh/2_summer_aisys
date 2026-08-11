# S06 답안
## T1. 실행 전 예측
- **T1-1** count vector / 가장 큰 MLE 성분: (1 1 3), 0.6 for label 2
- **T1-2** 더 큰 확률과 이유: PMF, 순서 고려에 있어서 그러하다.
- **T1-3** one-hot shape / 행합: (5,3), 모두 1
## T2. 손계산
- **T2-1** count vector / one-hot: x
- **T2-2** PMF 항 / sequence likelihood:0.2 0.5 0.3 0.5 0.5
- **T2-3** Multinomial 계수 / PMF: x. dir로 이해할래
- **T2-4** MLE vector / 합: (0.2 0.2 0.6), 1
## T3. 직접 구현
- **T3-1** one-hot / counts:
- **T3-2** sequence likelihood / count PMF:
- **T3-3** MLE:
## T4. 표준 API 참조 (선택, 작성 없음)
## T5. 잘못된 해석
- **T5-1** 계수 오류: 왜 오류임? 곱하면 pmf겠지. 뭔말인지몰겠음
- **T5-2** labels 길이 / count 합 불일치: 아 이딴거 문제로 내지좀마삼
## T6. 설명 확인
- **T6-1** sequence/count 정보: order
- **T6-2** 같은 MLE의 이유: 현 데이터에서 추출한 것이 그 데이터의 두 확률을 동시에 가장 잘 설명하기 때문
