---
layout: page
title: 고급 넘파이
subtitle: 브로드캐스팅(Broadcasting)
minutes: 40
---
> ## 학습목표 {.objectives}
>
> 학습을 한 후에 다음 기능이 학습자에게 장착됩니다:
>
> * 배열에 속한 모든 원소에 스칼라값을 추가하는 방법을 알게 됩니다.
> * 행렬 덧셈과 행 혹은 열 벡터 덧셈 결과를 예측할 수 있게 됩니다.
> * 루프를 사용하는 것보다 브로드케스팅을 사용하는 것이 왜 더 좋은지 설명할 수 있게 됩니다.
> * 브로드케스팅 규칙을 이해하고, 브로드케시팅된 배열형태에 대해 예측이 가능합니다.
> * `np.newaxis` 객체를 사용해서 브로드케스팅을 제어하는 방법을 알게 됩니다.

다른 크기를 갖는 배열에 연산작업을 수행하는 것이 가능합니다.
일부 경우에, 넘파이는 배열을 자동적으로 변환시켜서 모든 배열이 동일한 크기를 갖도록 만듦니다: 이런 변환작업을 **브로드캐스팅(broadcasting)** 이라고 부릅니다.

![numpy broadcasting in 2D](fig/numpy_broadcasting.png "2차원 넘파이 브로드케시틍")

상기 다이어그램을 재현해보자. 먼저 1차원 배열 두개를 생성한다:

```
>>> a = np.arange(4) * 10
>>> b = np.arange(3)
>>> a
array([ 0, 10, 20, 30])
>>> b
array([0, 1, 2])
```

`np.tile` 함수를 사용해서 2차원으로 타일을 붙이듯 생성한다:

```
>>> b2 = np.tile(b, (4, 1))
>>> b2
array([[0, 1, 2],
       [0, 1, 2],
       [0, 1, 2],
       [0, 1, 2]])
```

두번째 배열도 동일한 방식으로 작업하지만, 
행렬을 전치(transpose, 열과 행을 바꿈) 행렬을 생성시킨다:

```
>>> a2 = np.tile(a, (3, 1))
>>> a2 = a2.T
>>> a2
array([[ 0,  0,  0],
       [10, 10, 10],
       [20, 20, 20],
       [30, 30, 30]])
```

`np.tile` 함수가 새로운 배열을 생성시키고 데이터를 복사했다. 이제 두 배열을 원소별로 더하기 할 수 있다:

```
>>> a2 + b2
array([[ 0,  1,  2],
       [10, 11, 12],
       [20, 21, 22],
       [30, 31, 32]])
```

두번째 예제로, 1차원 배열과 2차원 배열을 더한다.
넘파이는 자동으로 1차원 배열을 누락된 방향으로 "타일을 붙이듯" 매워넣는다:

```
>>> a2 + b
array([[ 0,  1,  2],
       [10, 11, 12],
       [20, 21, 22],
       [30, 31, 32]])
```

하지만, 이번 경우에 `b` 배열 어떤 사본도 관여하고 있지 않다.
대신에 넘파이가 `a` 각 행에 대해 `b` 배열에 있는 동일한 데이터를 사용했다 -- 이번 학습 말미에 작동 메커니즘에 대해 다룰 예정이다.

세번째 예제로, 단일 칼럼과 단일 벡터를 더했다.
1차원 배열에서 칼럼 배열을 얻으려면, 행이 4개이며 열이 1개인 2차원 배열로 변환시킨다.
넘파이에서 특수 객체 `np.newaxis`를 통해 크기가 1차원인 특이차원(Singular dimension)을 추가시킬 수 있다:

```
>>> a.shape
(4,)
>>> a_column = a[:, np.newaxis]
>>> a_column.shape
(4, 1)
>>> a_column
array([[ 0],
       [10],
       [20],
       [30]])
```

칼럼 벡터를 1차원 배열과 더한다:

```
>>> a_column + b
array([[ 0,  1,  2],
       [10, 11, 12],
       [20, 21, 22],
       [30, 31, 32]])
```

이 결과는 행벡터와 열벡터를 더한 것과 동일하다:

```
>>> b_row = b[np.newaxis, :]
>>> b_row
array([[0, 1, 2]])
>>> b_row.shape
(1, 3)
>>> a_column + b_row
array([[ 0,  1,  2],
       [10, 11, 12],
       [20, 21, 22],
       [30, 31, 32]])
```

> ## 데이터 정규화 {.challenge}
>
> 다음 배열이 주어졌다고 가정한다:
>
> ```
> a = np.random.rand(10, 100) 
> ```
> 
> 배열 `a` 각 칼럼에 대해 평균을 뺀다. 그리고 나서 행에 대해서도 동일한 작업을 수행한다.

브로드캐스팅이 다소 마술처럼 보이지만, 실제로 이 방법을 사용하는 것이 훨씬 자연스럽다. 입력 데이터보다 출력 데이터가 
더 많은 차원을 갖는 배열인 문제를 해결할 때 특히 그렇다.
브로드캐스팅의 유효성과 브로드캐스트된 배열 형태를 판단하는 간단한 규칙이 있다:

> 브로드캐스트하기 위해서, 연산작업에 사용되는 두 배열에 대해 끝부분 축의 크기가 동일하거나, 축 중에 하나는 1이 되어야만 한다.

사실 다음에 나와 있는 것이 앞에서 나온 그림에 대한 세가지 더하기 대해 동작하는 메커니즘을 보여주고 있다.

```
a:      4 x 3 
b:      4 x 3
결과: 4 x 3

a:      4 x 3
b:          3
결과: 4 x 3

a:      4 x 1
b:          3
결과: 4 x 3
```

두가지 예제를 더 살펴보자:

```
이미지  (3차원 배열): 256 x 256 x 3
스케일  (1차원 배열):             3
결과   (3차원 배열): 256 x 256 x 3

A      (4차원 배열):  8 x 1 x 6 x 1
B      (3차원 배열):      7 x 1 x 5
결과    (4차원 배열):  8 x 7 x 6 x 5
```

> ## 브로드케스팅 규칙 {.challenge}
> 
> 배열이 다음과 같이 주어졌다고 가정한다:
>
> ```
> X = np.random.rand(10,3)
> Y = np.random.rand(3)
> ```
> 
> 다음 중 어떤 것이 오류를 발생시키지 *않는가?*
> 
> a) `X + Y`
> 
> b) `X[np.newaxis, :] + Y`
> 
> c) `X + Y[:, np.newaxis]`
> 
> d) `X[:, np.newaxis] + Y`
> 
> e) `X + Y[np.newaxis, :]`
>
> f) `X[:, np.newaxis, :] + Y`
> 
> 최종 브로드캐스트된 배열 형태는 어떻게 되는가? 추측해보고 나서 점검해 본다.

> ## 3차원 브로드캐스팅 {.challenge}
>
> 아래 코드를 보고, `x` 배열의 모든 원소와 `y` 배열 모든 원소를 합한 결과를 포함한 배열을 생성해 보세요.
>
> ```python
> x = np.random.rand(3, 5)
> y = np.random.randint(10, size=8)
> z = x # FIX THIS
> ```

> ## 브로드케스팅 인덱스 {.challenge}
>
> `y` 형태를 예측하고 검증해 보세요:
> 
> ```python
> x = np.empty((10, 8, 6))
> 
> idx0 = np.zeros((3, 8)).astype(int)
> idx1 = np.zeros((3, 1)).astype(int)
> idx2 = np.zeros((1, 1)).astype(int)
> 
> y = x[idx0, idx1, idx2]
> ```

상당히 많은 격자 혹은 네트워크 기반 문제도 브로드캐스팅을 사용할 수 있다.
예를 들어 $10 \times 10$ 격자에 원점에서 거리를 계산하려고 하면, 다음과 같이 코드를 작성해서 작업을 수행할 수 있다.

```
>>> x = np.arange(5)
>>> y = np.arange(5)[:, np.newaxis]
>>> distance = np.sqrt(x ** 2 + y ** 2)
>>> distance
array([[ 0.        ,  1.        ,  2.        ,  3.        ,  4.        ],
       [ 1.        ,  1.41421356,  2.23606798,  3.16227766,  4.12310563],
       [ 2.        ,  2.23606798,  2.82842712,  3.60555128,  4.47213595],
       [ 3.        ,  3.16227766,  3.60555128,  4.24264069,  5.        ],
       [ 4.        ,  4.12310563,  4.47213595,  5.        ,  5.65685425]])
```

> ## 2차원 격자 생성 {.challenge}
> 
> 다음 두가지 경우에 `x`, `y`, `z` 차원은 각각 어떻게 될까?
>
> ```
> x, y = np.mgrid[:10, :5]
> z = x + y
> ```
> 
> 그리고,
> 
> ```
> x, y = np.ogrid[:10, :5]
> z = x + y
> ```
> 
> `np.mgrid`와 비교하여 `np.orgid`을 사용하는 장점은 무엇인가?

> ## 66번 도로 -- 실전 예제 {.callout}
>
> 66번 도로를 따라 위치한 도시 사이 거리를 배열로 생성해보자: Chicago, Springfield, Saint-Louis, Tulsa, Oklahoma City, Amarillo, Santa Fe, Albuquerque, Flagstaff and Los Angeles.
> ```
> >>> mileposts = np.array([0, 198, 303, 736, 871, 1175, 1475, 1544,
> ...        1913, 2448])
> >>> distance_array = np.abs(mileposts - mileposts[:, np.newaxis])
> >>> distance_array
> array([[   0,  198,  303,  736,  871, 1175, 1475, 1544, 1913, 2448],
>        [ 198,    0,  105,  538,  673,  977, 1277, 1346, 1715, 2250],
>        [ 303,  105,    0,  433,  568,  872, 1172, 1241, 1610, 2145],
>        [ 736,  538,  433,    0,  135,  439,  739,  808, 1177, 1712],
>        [ 871,  673,  568,  135,    0,  304,  604,  673, 1042, 1577],
>        [1175,  977,  872,  439,  304,    0,  300,  369,  738, 1273],
>        [1475, 1277, 1172,  739,  604,  300,    0,   69,  438,  973],
>        [1544, 1346, 1241,  808,  673,  369,   69,    0,  369,  904],
>        [1913, 1715, 1610, 1177, 1042,  738,  438,  369,    0,  535],
>        [2448, 2250, 2145, 1712, 1577, 1273,  973,  904,  535,    0]])
>```
> ![Distances on Route 66](fig/route66.png)

> ## 거리 {.challenge}
> 
> 유럽 주요국가 수도가 위도와 경도 배열로 주어졌을 때, 각 수도 사이 거리를 계산하시오. 근사적으로 거리를 구하는 공식으로
> 다음 수식을 사용한다:
>
> $$D=6371.009\sqrt{(\Delta\phi)^2 + (\Delta\lambda)^2}\qquad \text{(in kilometers)},$$
>
> 여기서, $\Delta\phi=\phi_1-\phi_2$ 와 $\Delta\lambda=\lambda_1-\lambda_2$는
> 라디안으로 두 도시간에 위도와 경도 차이를 표기한다. (*힌트:* 각도를 라디언으로 변환하려면, 각도에 $\pi/180$을 곱한다).
>
> ```
> coords = np.array([
>                   [ 23.71666667,  37.96666667], # Athens
>                   [ 13.38333333,  52.51666667], # Berlin
>                   [ -0.1275    ,  51.50722222], # London
>                   [ -3.71666667,  40.38333333], # Madrid
>                   [  2.3508    ,  48.8567    ], # Paris
>                   [ 12.5       ,  41.9       ]  # Rome
                    ]) 
> ```
> 계산을 하고 나서, 좀더 [정밀한 공식](https://en.wikipedia.org/wiki/Geographical_distance#Spherical_Earth_projected_to_a_plane)을 갖고 결과값과 비교해본다.
>
> $$D=6371.009\sqrt{(\Delta\phi)^2 + (\cos(\phi_m)\Delta\lambda)^2}$$
>
> 여기서 $\phi_m = (\phi_1+\phi_2) / 2$ 는 평균 위도다.



