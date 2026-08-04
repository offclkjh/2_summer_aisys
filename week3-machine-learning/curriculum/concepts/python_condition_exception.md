# `coding.python_condition_exception` — Python 조건문과 예외

- 필요한 수준: 조건이 참일 때 지정된 예외를 발생시키는 코드를 읽고 빈 조건을 채운다.
- 뜻: `if`는 조건에 따라 코드 실행을 나누고 `raise`는 함수가 계약 위반을 알리게 한다.
- 진단: `value = -1`일 때 아래 함수가 어떤 예외를 내는지 말한다.

```python
def require_nonnegative(value):
    if value < 0:
        raise ValueError("value must be nonnegative")
```

- 최소 복습: type이 잘못됐으면 보통 `TypeError`, 값·shape가 잘못됐으면 `ValueError`를 사용한다.
- 예제: `isinstance(value, int)`는 `value`가 정수 객체인지 검사한다.
