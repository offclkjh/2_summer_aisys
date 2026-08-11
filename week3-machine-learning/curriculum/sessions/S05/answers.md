# S05 답안

> 실행·테스트 전에 T1을 먼저 작성한다. 튜터의 힌트를 받았다면 어디서
> 받았는지와 처음 생각이 왜 달랐는지도 남긴다.

## T1. 실행 전 예측

1. 관측열의 순서를 유지한 likelihood와 성공 횟수만 남긴 probability의 크기 비교:
2. `theta = 0.4` 대신 `theta = 0.6`에서 데이터 likelihood가 어떻게 변할지와 그 이유:
3. MLE가 `0.5`보다 클지, 같을지, 작을지에 대한 예측:

## T2. 손계산

- `k`, `n - k`:
- 개별 Bernoulli PMF 다섯 항:
- 관측열 likelihood:
- log-likelihood:
- Binomial PMF와 조합계수의 역할:
- MLE 도출:

## T3. NumPy 직접 구현

- 완성한 함수와 사용한 배열 연산:
- 각 함수의 반환 type:

## T4. 검산

- 손계산과 구현 비교:
- `log(likelihood)`와 log-likelihood 비교:
- Binomial/Bernoulli 비율과 조합계수 비교:

## T5. 잘못된 해석 실패 사례

- 고른 오류 1과 틀린 이유:
- 고른 오류 2와 틀린 이유:
- 각 식이 실제로 계산하는 사건:

## T6. 설명 확인

- Bernoulli 관측열과 Binomial 성공 횟수가 같은 `theta`에 대해 어떻게
  연결되는지:
- likelihood가 확률분포와 달리 `theta`의 함수로 읽히는 이유:
- 왜 MLE가 표본 성공 비율인지:
