# S07 답안
## T1. 실행 전 예측
- **T1-1** 더 큰 prior: 1
- **T1-2** category 0 prediction/이유: 0, 관측에만 의존하는 prior 하에 posterior의 argmax가 0이니까.
- **T1-3** category 2 unsmoothed: likelihood가 둘다 0 나와서 score가 -inf로 분류 불가
- **T1-4** category 2 smoothed: 데이터가 없는 상황에서 prior 높은 1로 분류될것 같음
## T2. 손계산
- **T2-1** 행합/전체/prior: (4, 5), 9, (4/9, 5/9) 
- **T2-2** raw conditional/행합: ((3/4 1/4 0) (1/5 4/5 0)), (1 1), 열합 (19/20 21/20 0) <- 1이 아닐 수 있음
- **T2-3** category 0 joint/log/prediction:(3/9 1/9), 로그는 패스, 0
- **T2-4** category 2 joint/log/failure:(0 0), (-inf -inf), 음의무한 비교 불가, zero count error
- **T2-5** smoothed conditional/행합:((4/7 2/7 1/7) (2/8 5/8 1/8)), (1 1)
- **T2-6** smoothed category 2 joint/log/prediction: (4/63 5/72), 로그패스, 1
## T3. 직접 구현
- **T3-1** class_priors:
- **T3-2** conditional_probabilities:
- **T3-3** log_joint_scores:
- **T3-4** predict_class:
## T4. 표준 API 참조 (선택, 작성 없음)
## T5. 잘못된 해석
- **T5-1** wrong axis: 당연히 안되지 likelihood 의미랑 아예 다름
- **T5-2** all-`-inf` argmax: 비교 불가 오류 가 아니라 임의로 0 반환
- **T5-3** wrong denominator: 1이 되지 않는다, likelihood의 확률 의미가 사라짐
## T6. 설명 확인
- **T6-1** Bayes argmax: 주어진 category 관측에서 p(x)는 변하지 않기에 prior*conditional이 posterior에 비례하고, argmax로 가장 그럴듯한 class를 고를 수 있다. (사실은 관측에 따른 class의 분포를 예측할 수 있다.)
- **T6-2** zero-count failure: -inf라는 비교불가한 값을 만든다 가 아니라 임의로 0 반환
- **T6-3** smoothing 보장/한계: 보장은 zero count를 없애지만, 한계로는 여젼히 overfitting이 아니라 타당성 보장 x
