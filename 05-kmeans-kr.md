---
layout: page
title: 고급 넘파이
subtitle: "사례 K-평균"
minutes: 45
---

> ## 학습목표 {.objectives}
>
> 학습을 한 후에 다음 기능이 학습자에게 장착됩니다:
>
> * 단순한 군집 알고리듬을 구현하는데 축기반 축약기능, 브로드캐스팅, 인덱스 기능을 조합할 수 있게 된다.
> * 벡터화의 장점이 무엇인지 이해하고, 언제 사용할지 언제 사용하지 말지도 이해하게 된다.


K-평균 알고리즘은 데이터를 군집화하는 단순한 알고리즘이다 -- 즉, 객체의 속성에만 기반해서 유사한 객체집단을 식별해낸다.
다음 그래프를 통해 알고리즘을 가장 잘 도식화할 수 있다.

![](fig/kmeans/kmeans_illustration.png)


### 데이터 적재

먼저 표본데이터를 적재한다. 표본데이터가 없다면, [여기에서](data/kmeans_data.csv) 데이터를 다운로드 받는다.

```
>>> data = np.loadtxt('kmeans_data.csv')
>>> data.shape
(30, 2)
```

데이터를 시각화하는데, `matplotlib` 팩키지에서 나온 `scatter` 함수를 사용한다:

```
>>> import matplotlib.pyplot as plt
>>> plt.scatter(data[:, 0], data[:, 1], s=40)
>>> plt.show()
```

![군집 3개를 갖고 있는 표본데이터](fig/kmeans/generating_data.png)

예제 코드를 점진적으로 작성해 나갈 예정이라, 스크립트에 명령어를 담아 저장한다:

```
import numpy as np
import matplotlib.pyplot as plt

# load data
data = np.loadtxt('kmeans_data.csv')

# plot
plt.scatter(data[:, 0], data[:, 1], s=40)
```


### 초기화

알고리듬 첫번째 단계로 군집 중앙을 초기화한다.
임의로 초기화하지만, 일관성 있게 데이터에서 나온 평균과 표준편차를 사용한다:


```python
K = 3
centroids = np.random.randn(K, 2)
```

데이터에 군집 중심점에 중심을 맞추려면, 데이터의 평균과 표준편차에 정규화하는 것이 좋다:

```
centroids = centroids * np.std(data, 0)
centroids = centroids + np.mean(data, 0)
```

데이터와 임의 군집중심을 동일한 그림에 도식화한다:


```python
plt.scatter(data[:, 0], data[:, 1], s=40)
plt.scatter(centroids[:, 0], centroids[:, 1], c=np.arange(3), s=100)
```

![임의로 초기화된 군집 중심 (색상이 칠해진 큰 점)](fig/kmeans/initialisation.png)

이제 스크립트에 작성한 코드를 복사해서 붙여넣는다. ipython 콘솔 `%history` 명령어가 유용하다.


### 배정

> ## 가장 가까운 중앙 찾기 {.challenge}
>
> 모든 점과 중심점 각각 사이에 대한 유클리드 거리를 계산한다.
> 그리고 나서, 가장 가까운 중심점에 대한 색인을 찾아낸다.

이제 각 점을 가장 가까운 중심점에 배정한다.
먼저, 중심점 각각에 대해 점 각각에 대한 유클리드 거리를 계산한다.
이 작업을 위해서 **브로드캐스팅** 을 사용한다:


```python
deltas = data[:, np.newaxis, :] - centroids
distances = np.sqrt(np.sum((deltas) ** 2, 2))
```

각 데이터점에 대해 최소 거리를 갖는 중심점을 식별한다.
**axis argument** 를 갖는 `argmin` 메쏘드를 사용한다:

```python
closest = distances.argmin(1)
```

이제 중심점과 군집이 속한 소속을 반영하여 색칠을 데이터점에 반영하여 도식화한다:

```python
plt.scatter(data[:, 0], data[:, 1], s=40, c=closest)
plt.scatter(centroids[:, 0], centroids[:, 1], c=np.arange(3), s=100)
```

![가장 근접한 군집중앙에 배정된 데이터점들](fig/kmeans/assignment.png)

### 신규 군집 중앙 계산

> ## 군집 중앙 {.challenge}
>
> 군집 배정 배열이 정해지면, `closest` 를 통해 첫번째 군집 좌표중앙을 계산한다.(인덱스 0). 

새로운 군집 중앙을 계산하는데, 해당 군집에 속한 모든 데이터점을 평균낸다.
**부울 마스크(Boolean Mask)** 를 사용한다.
예를 들어, 군집 0에 대한 중심을 계산하는데, 다음 명령어를 사용한다:


```python
data[closest==0, :].mean(0)
```

```
array([ 2.90695091,  2.52099101])
```

모든 군집에 대해 반복하는데, 리스트 Comprehension 혹은 for 루프를 사용한다.
군집 숫자는 보통 데이터 갯수보다 훨씬 적기 때문에, for 루프가 알고리듬 속도에 영향을 주지 못한다:

```python
centroids = np.array([data[closest == i, :].mean(0) for i in range(3)])
```

신규 중심점과 군집에 속한 데이터점을 도식화해서 점검한다.

![군집 중심점 재계산](fig/kmeans/update_centers.png)


### 반복

이제, 데이터점을 군집에 배정하고 군집중앙을 갱신하는 작업절차를 반복하고,
알고리듬 진행과정을 지켜본다.


```python
for iteration in range(5):
   # assign points to clusters
   deltas = data[:, np.newaxis, :] - centroids
   distances = np.sqrt(np.sum((deltas) ** 2, 2))
   closest = distances.argmin(1)

   # calculate new centroids
   centroids = np.array([data[closest == i, :].mean(0) for i in range(3)])
```

> ## 중단 기준 {.challenge}
>
> 각각을 반복한 뒤에, 어떤 점이 군집 소속이 변경되었는지 점검한다.
> 수렴이 이뤄지면 알고리듬을 중단한다. 즉, 수렴은 재배정 단계 작업 뒤에 군집이 변경하지 않는 것으로 정의된다.

> ## 군집이 한개? {.callout}
>
> 종종 알고리듬이 퇴화결과를 만들어내는 경우가 있다 -- 모든 점이 군집 하나에 배정되는 경우 (혹은 최종 군집 갯수가 
> 사전에 정의한 K보다 적은 경우). 이런 것이 임의 초기점을 갖는 K-평균의 단점중 하나다.
> 가능한 해법은 다른 초기값을 갖고 알고리듬을 반복해서 최선의 군집을 찾아내는 것이지만, 더 좋은 해법도 존재한다.

### 모두 한통에 담아 보기

최종 작성된 스크립트는 다음과 같은 모양이 된다:

```python
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('kmeans_data.csv')

# randomly initalize the centroids
K = 3
centroids = np.random.randn(K, 2)
centroids = centroids * np.std(data, 0)
centroids = centroids + np.mean(data, 0)

for iteration in range(5):
   # assign points to clusters
   deltas = data[:, np.newaxis, :] - centroids
   distances = np.sqrt(np.sum((deltas) ** 2, 2))
   closest = distances.argmin(1)

   # calculate new centroids
   centroids = np.array([data[closest == i, :].mean(0) for i in range(3)])

# plot 
plt.scatter(data[:, 0], data[:, 1], s=40, c=closest)
plt.scatter(centroids[:, 0], centroids[:, 1], c=np.arange(3), s=100)

plt.show()
```

> ## K 선택 {.challenge}
>
> 알고리듬이 임의 K에 대해 동작하는지 점검한다. $K>3$을 시도해본다. 그러면 어떤 일이 발생하는가?


> ## 저장공간 혹은 속도 {.challenge}
>
> 새로운 군집을 배정하고 계산하는 작업을 for 루프로 교체한다.
> 어떤 구현 방식이 작은 군집문제(적은 관측점과 적은 차원)에 더 선호되는가?
> 어떤 구현 방식이 큰 군집문제(상당히 많은 관측점과 고차원 차원)에 더 선호되는가?
