# `coding.random_sampling` — 난수 표본과 seed

- 필요한 수준: 동일 seed가 재현 가능한 표본을 만든다는 점을 안다.
- 뜻: 분포에서 값을 뽑는 연산이며, seed는 의사난수열의 시작 상태를 고정한다.
- 진단: 실험 비교에서 seed를 기록해야 하는 이유와 길이 5 자료에서 복원추출 index 5개가 중복될 수 있는 이유를 말한다.
- 최소 복습: `rng = np.random.default_rng(0)`처럼 generator를 만들고 이를 재사용한다. `rng.integers(0, 5, size=5)`는 `0`부터 `4`까지의 index를 복원추출한다.
- 예제: 같은 seed로 새 generator를 만들면 같은 첫 표본을 얻는다. bootstrap에서는 중복 index가 정상이다.
