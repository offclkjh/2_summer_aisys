# S01 답안

## T1. 실행 전 예측

1. `D`에는 관측이 몇 개 있는가?

   답: 4

2. `D`의 shape는 무엇이며 유일한 축은 무엇을 세는가?

   답: shape : (4,), counts the numnber of data

3. `x_0`의 값과 shape는 무엇인가?

   답: 1, () <- scalar

4. `theta`의 값을 현재 데이터에서 직접 관측했는가?

   답: no, just have to infer

5. `observations`의 dtype은 무엇인가?

   답: np.int64

## T5. 실패 사례

T3의 서로 다른 규칙을 위반하는 입력 세 개를 직접 만들고 실행 전에 적는다.

### 사례 1

```python
o1 = np.array([], dtype=np.int64)
```

- 위반한 규칙: no observ.
- 예상 예외: no observations
- 실행 후 확인: correct

### 사례 2

```python
o2 = np.array(1)
```

- 위반한 규칙: not dim 1 (scaler)
- 예상 예외: not dim 1
- 실행 후 확인: correct

### 사례 3

```python
o3 = 1
```

- 위반한 규칙: not numpy ar
- 예상 예외: not numpy array
- 실행 후 확인: correct

## T6. 설명 확인

이 문제에서 `D`, `x_i`, `theta`는 각각 무엇이며, `D.shape == (4,)`의 두 표시는 무엇을 뜻하는가?

답: D: numpy array observations,
   x_i: each observation 0 or 1,
   theta: don't know,, mle is 3/4
   D.shape: dim and len of each axis
   (4,): 1 dim, 4 observation
