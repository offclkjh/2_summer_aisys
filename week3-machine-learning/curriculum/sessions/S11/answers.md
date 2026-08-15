# S11 답안

## T1. 실행 전 예측

- **T1-1** block, solve, 반환 shape:
- **T1-2** conditional mean 이동 방향과 근거:
- **T1-3** marginal/conditional variance 비교와 근거:
- **T1-4** observed value에 따라 바뀌는 항:

## T2. 같은 수치의 손계산

- **T2-1** mean/covariance block:
- **T2-2** marginal parameter:
- **T2-3** residual/solve/conditional mean:
- **T2-4** matrix solve/conditional covariance:
- **T2-5** T1 예측과 비교:

## T3. 직접 구현

- **T3-1** `gaussian_marginal`에서 보존한 index 순서와 shape:
- **T3-2** `gaussian_conditional`의 두 solve와 중간 shape:
- **T3-3** 다차원 partition 테스트에서 확인한 점:

## T4. 표준 API 검산 (선택)

- 관찰:

## T5. 실패 해석

- **T5-1** paired indexing과 block indexing:
- **T5-2** elementwise division과 linear solve:
- **T5-3** `squeeze`와 generic 반환 계약:
- **T5-4** index 순서와 block 의미:

## T6. 설명 확인

- **T6-1** marginalization과 conditioning:
- **T6-2** conditional mean correction의 세 요소:
- **T6-3** observed value와 conditional covariance:
- **T6-4** `T=2`, `O=3`의 shape:

## 선택 확장

- **D0** guided quadratic-form 유도:
- **D1** Ch. 5 posterior와 객체 비교:
- **D2** Schur complement:
