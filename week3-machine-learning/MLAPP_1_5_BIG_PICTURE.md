# MLAPP 1~5장 큰 그림

> 머신러닝은 불확실한 현실을 확률모형으로 표현하고, 관측 데이터로 모형에 대한 믿음을 갱신한 뒤, 새 데이터를 예측하고 손실이 작은 행동을 선택하는 과정이다.

$$
\boxed{
\text{현실}
\rightarrow
\text{확률모형}
\rightarrow
\text{추론}
\rightarrow
\text{예측}
\rightarrow
\text{결정}
}
$$

## 1. 객체들의 층위

머신러닝 문제에는 보통 다음 네 종류의 객체가 있다.

| 층위 | 기호 | 의미 | 처리 방식 |
|---|---:|---|---|
| 관측 데이터 | $D$ | 실제로 관측한 값 | 이미 주어짐 |
| 잠재변수 | $z$ | 관측 뒤에 숨어 있는 상태 | 데이터마다 추론 |
| 파라미터 | $\theta$ | 전체 데이터에 공유되는 규칙 | 데이터로 학습 |
| 하이퍼파라미터 | $\alpha$ | 파라미터에 대한 가정 | 고정·선택·추론 |

지도학습 데이터는 보통 다음과 같다.

$$
D=\{(x_i,y_i)\}_{i=1}^{N}
$$

- $x_i$: 입력
- $y_i$: 정답
- $N$: 표본 수
- 신경망의 weight와 bias: $\theta$

잠재변수 $z_i$와 파라미터 $\theta$는 모두 알려지지 않았지만 역할이 다르다.

- $z_i$: 특정 데이터 $i$의 숨은 설명. 예를 들어 이 점이 어느 군집에 속하는가?
- $\theta$: 모든 데이터에 공유되는 규칙. 예를 들어 각 군집의 평균과 공분산.

## 2. 모델은 계산 가능한 가정이다

동전 던지기를 다음처럼 모델링할 수 있다.

$$
x_i\mid\theta\sim\operatorname{Bernoulli}(\theta)
$$

이 식에는 이미 여러 가정이 들어 있다.

- 결과는 0 또는 1이다.
- 앞면 확률 $\theta$는 모든 시행에서 같다.
- $\theta$가 주어지면 시행들은 서로 독립이다.

따라서 데이터 전체의 확률은 곱으로 표현된다.

$$
p(D\mid\theta)
=
\prod_{i=1}^N p(x_i\mid\theta)
=
\theta^{N_1}(1-\theta)^{N_0}
$$

여기서 $N_1$은 앞면 횟수, $N_0$은 뒷면 횟수다.

분포를 선택한다는 것은 단순히 공식을 고르는 일이 아니다. 변수의 범위와 데이터 생성 방식을 가정하는 일이다.

- Bernoulli: 이진 결과
- Categorical: 여러 범주 중 하나
- Gaussian: 연속값과 잡음
- Beta: Bernoulli 확률에 대한 prior
- Dirichlet: 범주별 확률 벡터에 대한 prior

## 3. Bayes 식에 전체 구조가 들어 있다

$$
\boxed{
p(\theta\mid D,\alpha)
=
\frac{p(D\mid\theta)p(\theta\mid\alpha)}{p(D\mid\alpha)}
}
$$

### Likelihood

$$
p(D\mid\theta)
$$

"$\theta$가 이 값이라면, 관측된 데이터가 얼마나 잘 설명되는가?"

- 데이터 $D$는 관측되어 고정한다.
- $\theta$를 바꿔가며 데이터 설명력을 평가한다.

Likelihood를 $\theta$의 함수로 사용한다고 해서 일반적으로 $\theta$에 관한 확률분포가 되는 것은 아니다. $\theta$에 대해 적분했을 때 1이 될 필요가 없기 때문이다.

### Prior

$$
p(\theta\mid\alpha)
$$

"데이터를 보기 전에 어떤 $\theta$를 더 그럴듯하다고 보는가?"

여기서 $\alpha$는 prior의 모양을 결정하는 하이퍼파라미터다.

### Posterior

$$
p(\theta\mid D,\alpha)
$$

"데이터를 본 뒤 어떤 $\theta$가 얼마나 그럴듯한가?"

가장 중요한 구분은 다음과 같다.

$$
p(\theta\mid D)\neq p(D\mid\theta)
$$

- $p(D\mid\theta)$: 파라미터가 데이터를 설명하는 정도
- $p(\theta\mid D)$: 데이터를 본 뒤 파라미터에 대한 믿음

### Evidence

$$
p(D\mid\alpha)
=
\int p(D\mid\theta)p(\theta\mid\alpha)d\theta
$$

가능한 모든 $\theta$를 고려했을 때 모델 전체가 데이터를 얼마나 잘 설명하는지를 나타낸다.

한 모델 안에서 posterior만 계산할 때는 다음처럼 쓸 수 있다.

$$
p(\theta\mid D,\alpha)
\propto
p(D\mid\theta)p(\theta\mid\alpha)
$$

하지만 서로 다른 모델이나 prior를 비교할 때 evidence는 달라지므로 무시할 수 없다.

## 4. Beta–Bernoulli로 층위 구체화하기

동전을 $N$번 던져 앞면이 $N_1$번 나왔다고 하자.

### 데이터와 likelihood

$$
p(D\mid\theta)
=
\theta^{N_1}(1-\theta)^{N-N_1}
$$

- $D$: 관측된 앞면·뒷면 결과
- $\theta$: 알 수 없는 실제 앞면 확률

### Prior와 하이퍼파라미터

$$
\theta\mid a,b\sim\operatorname{Beta}(a,b)
$$

- $\theta$: 추론할 파라미터
- $a,b$: prior를 결정하는 하이퍼파라미터

### Posterior

$$
\theta\mid D,a,b
\sim
\operatorname{Beta}(a+N_1,\;b+N-N_1)
$$

Prior 정보와 데이터의 횟수가 단순히 더해진다. 이렇게 prior와 posterior가 같은 분포족에 속하는 관계가 conjugacy다.

### MLE, MAP, posterior mean

Likelihood만 최대화하면:

$$
\hat\theta_{\mathrm{MLE}}=\frac{N_1}{N}
$$

Posterior를 최대화하면:

$$
\hat\theta_{\mathrm{MAP}}
=
\frac{N_1+a-1}{N+a+b-2}
$$

Posterior 전체의 평균은:

$$
\mathbb E[\theta\mid D]
=
\frac{N_1+a}{N+a+b}
$$

- MLE와 MAP은 하나의 점추정치다.
- Posterior mean도 posterior를 하나의 값으로 요약한 것이다.
- Bayesian 추론의 본체는 점 하나가 아니라 posterior 전체다.

## 5. Frequentist와 Bayesian

| 관점 | Frequentist | Bayesian |
|---|---|---|
| 파라미터 $\theta$ | 고정되어 있지만 모르는 값 | 불확실성을 분포로 표현 |
| 데이터 | 반복 표본에서 변함 | 관측 후 조건으로 주어짐 |
| 추정 | MLE, 신뢰구간 | posterior, MAP, credible interval |
| 불확실성 | 추정량의 반복 표본 변동 | 데이터 이후 파라미터의 분포 |
| 예측 | 보통 추정값을 대입 | posterior 전체를 평균 |
| 모델 선택 | validation, CV, AIC/BIC | evidence, Bayes factor 등 |

Frequentist도 불확실성을 다룬다. 다만 파라미터 자체에 확률을 부여하지 않고, 데이터를 반복해서 뽑을 때 추정량이 어떻게 변하는지를 본다.

Bayesian도 자동으로 정답을 주지는 않는다. 잘못된 likelihood나 prior를 선택하면 posterior 역시 잘못된 가정 위에 만들어진다.

## 6. MLE, MAP과 regularization

MLE는 다음 값을 찾는다.

$$
\hat\theta_{\mathrm{MLE}}
=
\arg\max_\theta p(D\mid\theta)
$$

MAP은 prior까지 포함한다.

$$
\hat\theta_{\mathrm{MAP}}
=
\arg\max_\theta p(D\mid\theta)p(\theta)
$$

음의 로그를 취하면:

$$
\hat\theta_{\mathrm{MAP}}
=
\arg\min_\theta
\left[-\log p(D\mid\theta)-\log p(\theta)\right]
$$

따라서:

- $-\log p(D\mid\theta)$: 데이터 적합 loss
- $-\log p(\theta)$: regularization

파라미터에 평균 0인 Gaussian prior를 두면:

$$
-\log p(\theta)
\propto
\lambda\lVert\theta\rVert_2^2
$$

이것이 $L_2$ regularization 또는 weight decay와 연결된다. 다만 모든 regularizer가 실제 사전 믿음에서 출발하는 것은 아니다. 실무에서는 일반화나 수치 안정성을 위해 적용하고, 사후적으로 prior 관점에서 해석하기도 한다.

## 7. 두 종류의 하이퍼파라미터

### 확률모형의 하이퍼파라미터

$$
p(\theta\mid\alpha)
$$

의 $\alpha$다.

- Beta prior의 $a,b$
- Gaussian prior의 분산
- 잡음 분산
- regularization 강도 $\lambda$

이 값들은 모델이나 목적함수 자체를 바꾼다.

### 최적화 하이퍼파라미터

- learning rate
- batch size
- momentum
- epoch 수

이 값들은 주어진 목적함수를 어떻게 수치적으로 최적화할지를 결정한다.

이론적으로 learning rate가 달라져도 같은 MLE/MAP 해에 도달해야 한다. 반면 prior의 분산이 달라지면 목표로 삼는 MAP 해 자체가 달라진다. 비볼록 신경망에서는 optimizer 설정도 실제 도달 지점과 일반화에 영향을 주지만, 개념적 층위는 여전히 다르다.

## 8. 추론의 목적은 예측이다

새 입력 $x_*$의 출력 $y_*$를 Bayesian 방식으로 예측하면:

$$
\boxed{
p(y_*\mid x_*,D,\alpha)
=
\int p(y_*\mid x_*,\theta)p(\theta\mid D,\alpha)d\theta
}
$$

가능한 각 $\theta$의 예측을 posterior 확률에 따라 평균 내는 것이다.

점추정 방식은 하나의 값을 대입한다.

$$
p(y_*\mid x_*,\hat\theta)
$$

둘의 차이는 파라미터 불확실성을 예측에 반영하는지 여부다.

## 9. 예측과 결정은 다르다

예측분포를 얻었다고 행동이 자동으로 결정되는 것은 아니다.

$$
a^*
=
\arg\min_a
\mathbb E[L(a,y_*)]
$$

- $a$: 우리가 선택할 행동
- $L(a,y)$: 실제 결과가 $y$일 때 행동 $a$의 손실

손실에 따라 최적 행동이 달라진다.

- 0–1 loss: 가장 확률이 높은 클래스
- squared error: predictive mean
- absolute error: predictive median
- 질병 누락 비용이 큰 경우: 분류 임계값을 0.5보다 낮춤

전체 흐름은 다음과 같다.

$$
\boxed{
D
\rightarrow
p(\theta\mid D)
\rightarrow
p(y_*\mid x_*,D)
\rightarrow
\text{loss를 최소화하는 행동}
}
$$

## 10. 정보이론의 위치

Entropy는 분포 자체의 불확실성이다.

$$
H(p)=-\sum_y p(y)\log p(y)
$$

Cross-entropy는 실제 분포 $p$를 모델 $q$로 표현할 때의 평균 비용이다.

$$
H(p,q)=-\sum_y p(y)\log q(y)
$$

KL divergence는 두 분포의 차이를 나타낸다.

$$
D_{\mathrm{KL}}(p\|q)
=
\sum_y p(y)\log\frac{p(y)}{q(y)}
$$

관계는 다음과 같다.

$$
H(p,q)=H(p)+D_{\mathrm{KL}}(p\|q)
$$

학습할 때 실제 데이터 분포 $p$는 고정되어 있으므로 $H(p)$도 고정이다. 따라서 cross-entropy 최소화는 모델 분포 $q$와 실제 분포 $p$ 사이의 KL divergence를 줄이는 것과 같다.

분류에서 한 샘플의 cross-entropy는:

$$
-\log p_\theta(y\mid x)
$$

즉 PyTorch의 `CrossEntropyLoss`는 동시에 정보이론적 cross-entropy, negative log-likelihood, MLE를 위한 목적함수로 해석할 수 있다.

## 11. 생성모형과 판별모형

생성모형은 보통 joint distribution을 모델링한다.

$$
p(x,y)=p(y)p(x\mid y)
$$

그리고 Bayes 식으로 $p(y\mid x)$를 구한다.

판별모형은 직접 다음을 모델링한다.

$$
p(y\mid x)
$$

- 생성모형: 각 클래스가 어떤 입력을 생성하는지까지 설명
- 판별모형: 입력에서 정답을 예측하는 관계에 집중

두 구분은 서로 다른 축이다.

- generative vs discriminative: 무엇을 모델링하는가?
- Bayesian vs frequentist: 파라미터 불확실성을 어떻게 다루는가?

생성모형이 항상 Bayesian인 것도 아니고, 판별모형이 항상 frequentist인 것도 아니다.

## 12. PyTorch 학습과의 연결

```python
logits = model(x)
loss = criterion(logits, y)

optimizer.zero_grad()
loss.backward()
optimizer.step()
```

| PyTorch 요소 | 확률적 의미 |
|---|---|
| `model(x)` | $\theta$로 예측분포의 파라미터 계산 |
| `softmax(logits)` | $p_\theta(y\mid x)$ |
| `CrossEntropyLoss` | $-\log p_\theta(y\mid x)$ |
| 전체 데이터 loss | negative log-likelihood |
| `weight_decay` | Gaussian prior에 대응 가능 |
| `backward()` | $\nabla_\theta$ 계산 |
| `optimizer.step()` | 목적함수를 줄이는 수치 최적화 |
| 학습된 weight | 하나의 점추정치 $\hat\theta$ |

`backward()`는 Bayesian inference가 아니다. 목적함수의 미분을 효율적으로 계산할 뿐이다.

일반적인 신경망 학습은:

- Cross-entropy만 사용하면 대체로 MLE
- Weight decay까지 사용하면 MAP으로 해석 가능
- 하지만 posterior 전체가 아니라 하나의 $\hat\theta$만 학습

한다.

Bayesian neural network라면 weight에 대한 posterior를 근사하고 다음 적분까지 다뤄야 한다.

$$
\int p(y_*\mid x_*,\theta)p(\theta\mid D)d\theta
$$

## 전체 사고 체크리스트

새로운 ML 문제를 보면 다음 순서로 질문한다.

1. 무엇을 관측했는가?
2. 무엇이 파라미터이고 무엇이 잠재변수인가?
3. 어떤 데이터 생성 과정을 가정했는가?
4. Likelihood $p(D\mid\theta)$는 무엇인가?
5. Prior $p(\theta\mid\alpha)$는 있는가?
6. 원하는 것이 MLE, MAP, posterior 전체 중 무엇인가?
7. 하이퍼파라미터는 모델의 것인가, optimizer의 것인가?
8. 새 데이터의 predictive distribution은 무엇인가?
9. 예측을 어떤 loss 아래 행동으로 바꿀 것인가?
10. Train·validation·test의 역할이 섞이지 않았는가?

가장 압축하면 다음 구조다.

$$
\boxed{
\underbrace{p(D\mid\theta)}_{\text{데이터 적합}}
\underbrace{p(\theta\mid\alpha)}_{\text{사전 가정}}
\Rightarrow
\underbrace{p(\theta\mid D,\alpha)}_{\text{학습}}
\Rightarrow
\underbrace{p(y_*\mid x_*,D,\alpha)}_{\text{예측}}
\Rightarrow
\underbrace{\arg\min_a\mathbb E[L(a,y_*)]}_{\text{결정}}
}
$$

Week 3에서 가장 먼저 체화해야 할 것은 개별 분포 공식을 외우는 것이 아니라, 지금 계산하는 값이 이 구조의 어느 층에 있는지를 식별하는 능력이다.
