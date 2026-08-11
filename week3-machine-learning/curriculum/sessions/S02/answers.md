# S02 답안

## T1. 실행 전 예측

1. `counts.shape`와 두 axis의 의미:

   답: (2,2), 첫번쨰 축은 실제 데이터, 두번째 축은 모델의 출력

2. `p(A)`를 위해 합으로 제거할 변수:

   답: joint distribution에서 Y를 제거한다.

3. `p(Y)`를 위해 합으로 제거할 변수:

   답: A

4. `p(Y=1|A=1)`과 `p(A=1|Y=1)`의 차이:

   답: 수식적으로는 같은 joint에 다른 marginal을 나누었으며, 의미로는 조건이 A=1일 때 Y~ 와 Y=1일때 A~로 다르다.

## T2. Joint와 marginal 손계산

- `N`: sum_a sum_y joint = 100
- joint table: easy
- `p(A)`: easy
- `p(Y)`: easy
- 세 합의 확인:

## T4. Conditional과 Bayes

- `p(Y=1|A=1)`: 7/10
- `p(A=1|Y=1)`의 직접 계산: 7/11
- `p(A=1|Y=1)`의 Bayes 계산: 7/10 * 1/5 / 11/50 = 7/11
- 두 posterior 계산의 비교: same

## T5. Axis 실패 사례

- axis를 바꾼 첫 결과가 실제로 나타내는 marginal:
- axis를 바꾼 둘째 결과가 실제로 나타내는 marginal:
- shape와 합만으로 의미 오류를 잡을 수 없는 이유: 다르니까 축 의미가 easy

## T6. 설명 확인

답: easy
