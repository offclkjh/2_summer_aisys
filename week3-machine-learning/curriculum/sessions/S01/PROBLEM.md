# S01 — 확률모형의 객체와 shape

> 상태: `ready`. 이 문서에 문제를 푸는 데 필요한 상황 정보와 수치가 모두 들어 있다.

## 목표와 비목표

- 목표: 동전 관측 사례에서 데이터 한 개 `x_i`, 전체 데이터 `D`, 미지의 파라미터 `theta`를 구분한다.
- 목표: Python 리스트를 NumPy 배열로 만들고 `shape`, `dtype`, indexing을 직접 확인한다.
- 목표: 입력 함수가 기대하는 배열 계약을 문장과 코드로 표현한다.
- 이번 세션에서 하지 않는 것: Bayes 계산, 동전 확률 추정, 센서 tensor, linear layer, PyTorch.

## 시작 전 선수지식 확인

필요한 선수지식은 Python 리스트·숫자 하나·함수·조건문과 예외의 기초다. NumPy 경험은 필요하지 않다.

1. `[1, 0, 1, 1]`에는 값이 몇 개 있는가?
2. 숫자 하나 `1`과 값 하나를 담은 리스트 `[1]`은 같은 구조인가?
3. 함수의 입력과 반환값은 무엇인가?
4. 잘못된 type과 잘못된 값에 각각 어떤 예외를 사용하는가?

막히면 다음 두 자료만 읽고 다시 답한다.

- [Python 리스트](../../concepts/python_list.md)
- [Python 스칼라](../../concepts/python_scalar.md)
- [Python 함수](../../concepts/python_function.md)
- [Python 조건문과 예외](../../concepts/python_condition_exception.md)

## 교재 연결

- 판본: Kevin P. Murphy, *Machine Learning: A Probabilistic Perspective* (2012).
- 주제명: Chapter 1의 supervised learning 기본 표기와 Chapter 2의 random variable 표기.
- 이 세션에서 확인할 기호: 전체 데이터 `D`, 관측 하나 `x_i`, 모델 파라미터 `theta`.
- 교재는 기호의 일반적 의미를 확인하는 참고자료다. 아래 배열의 값과 shape는 이 문제에서 직접 준다.

## 문제에서 주어진 정보

한 동전을 네 번 던져 다음 결과를 관측했다.

```text
앞면, 뒷면, 앞면, 앞면
```

앞면을 `1`, 뒷면을 `0`으로 기록한다. 따라서 전체 관측 데이터는 다음과 같다.

```python
observations_list = [1, 0, 1, 1]
```

이 문제에서는 다음처럼 기호를 정의한다.

| 기호 | 이 문제에서의 뜻 | 알고 있는가? | 구조 |
|---|---|---|---|
| `x_i` | `i`번째 동전 던지기 결과 하나 | 직접 관측함 | 숫자 하나 |
| `D` | 네 번의 결과 전체 | 직접 관측함 | 값 네 개의 1차원 배열 |
| `theta` | 이 동전에서 앞면이 나올 확률 | 아직 모름 | 확률 하나 |

`y`, `z`, `alpha`, `a`는 이 문제에서 정의하지 않는다. 값을 만들어내거나 표에 추가하지 않는다.

NumPy에서는 다음 코드로 리스트를 배열로 바꾼다.

```python
import numpy as np

observations = np.array([1, 0, 1, 1], dtype=np.int64)
```

- `shape == (4,)`: 축이 하나이고 그 축에 값이 네 개 있다.
- `dtype == np.int64`: 각 값을 64-bit 정수로 저장한다.
- `observations[0] == 1`: index `0`으로 첫 관측을 꺼낸다.

여기서 `(4,)`의 `4`는 교재에서 유도한 값이 아니라 **문제에서 준 네 번의 관측 수**다.

## 사용할 정의

- scalar: 배열 축을 갖지 않는 값 하나. NumPy scalar array의 shape는 `()`다.
- 1차원 배열: 축이 하나인 배열. 값이 `N`개이면 shape는 `(N,)`다.
- shape: 각 축이 세는 원소 수를 순서대로 적은 tuple이다.
- dtype: 배열 원소를 저장하는 자료형이다.
- 입력 계약: 함수가 받아들일 입력의 type, shape, dtype, 값 범위를 명시한 규칙이다.

## 과제

### T1. 실행 전 예측

코드를 실행하기 전에 다음 답을 `answers.md`에 적는다.

1. `D`에는 관측이 몇 개 있는가?
2. `D`의 shape는 무엇이며 유일한 축은 무엇을 세는가?
3. `x_0`의 값과 shape는 무엇인가?
4. `theta`의 값을 현재 데이터에서 직접 관측했는가?
5. `observations`의 dtype은 무엇인가?

### T2. 직접 확인

`starter.py`의 `inspect_observations()`를 완성하여 배열의 구조와 첫 번째 관측을 조사한다. 반환값은 다음 정보를 이 순서로 담은 tuple이어야 한다.

1. 배열의 shape
2. 원소의 dtype
3. 첫 번째 관측값
4. 전체 관측 개수

구체적인 반환값은 T1의 예측을 옮겨 적지 말고 직접 구현한 뒤 실행해서 확인한다.

### T3. 입력 계약 구현

`validate_coin_observations(observations)`를 완성한다. 유효한 입력은 다음 조건을 모두 만족한다.

- NumPy 배열이다.
- 관측이 하나 이상인 1차원 배열이다.
- 정수 dtype이며 모든 값이 `0` 또는 `1`이다.

유효한 입력은 아무것도 반환하지 않는다. 잘못된 객체 종류나 dtype에는
`TypeError`를, 잘못된 shape·빈 배열·허용되지 않은 값에는 `ValueError`를
발생시킨다. 검사 순서와 NumPy 표현은 직접 정한다.

막히면 완성 표현을 한꺼번에 찾지 말고, 현재 확인하려는 조건 하나를 정한 뒤
튜터에게 그 조건을 조사할 NumPy 속성이나 함수에 대한 힌트만 요청한다.

### T4. 검산

프로젝트 root에서 다음 명령을 실행한다.

```bash
cd week3-machine-learning/curriculum/sessions/S01
../../../../.venv/bin/python starter.py
../../../../.venv/bin/python -m unittest -v test_contract.py
```

테스트는 요구사항을 새로 알려주는 문제문이 아니다. 위 T2–T3 계약이 지켜지는지만 확인한다.

### T5. 실패 사례

T3의 서로 다른 규칙을 하나씩 위반하는 입력 세 개를 직접 만든다. 각 입력에
대해 위반한 규칙과 예상 예외를 `answers.md`에 먼저 적고 실행해서 확인한다.
세 사례가 같은 규칙만 반복해서 검사하지 않게 한다.

### T6. 설명 확인

다음을 1분 안에 설명한다.

> 이 문제에서 `D`, `x_i`, `theta`는 각각 무엇이며, `D.shape == (4,)`의 두 표시는 무엇을 뜻하는가?

## 제출물

- `answers.md`: T1과 T5의 실행 전 답, T6의 짧은 설명
- 완성한 `starter.py`
- 통과한 `test_contract.py` 실행 결과

## 완료 기준

- `D`, `x_i`, `theta`의 역할을 문제에 정의된 범위 안에서 구분한다.
- `(4,)`, `()`, `(1, 4)`가 서로 다른 이유를 설명한다.
- 함수가 유효 입력을 받아들이고 다섯 계약 위반을 지정된 예외 유형으로 거부한다.
- 제공된 8개 테스트를 모두 통과한다.

## 선택 확장

핵심 과제를 끝낸 뒤에만 `[batch, time, channel]` 센서 배열을 별도 사례로 다룬다. 이 확장은 S01 완료 조건에 포함하지 않는다.
