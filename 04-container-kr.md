---
layout: page
title: 고급 넘파이 
subtitle: 배열 컨테이너
minutes: 30
---
> ## 학습목표 {.objectives}
>
> 학습을 한 후에 다음 기능이 학습자에게 장착됩니다:
>
> * 배열에 담겨질 수 있는 객체 자료형에 대해 나열할 수 있다.
> * `dtype` 개념을 이해하고, 작업중인 데이터에 가장 적합한 `dtype`을 선택할 수 있다.
> * 객체 배열이 무엇인지 그리고 언제 생성시킬지 알게 된다.
> * 배열에 대한 `ndim`, `shape`, `stride` 특성이 무엇인지 설명할 수 있다.
> * 메모리에 배열의 배치상황을 이해하고, 최적의 배열 성능을 위한 사용법을 익힌다.
> * 포트란과 C기반 순서 차이를 설명할 수 있다. 기본디폴트 설정도 알게 된다.

### 자료형

(리스트 같은) 파이썬에 내장된 컨테이너와 비교하여 넘파이 배열은 사전에 결정된 자료형 원소만 저장할 수 있다. 배열에 
포함된 자료형을 살펴보는데, `dtype` 속성을 사용한다. 다음 예제 두개를 살펴보자:

```
>>> a = np.array([1, 2, 3])
>>> a.dtype
dtype('int64')

>>> b = np.array([1., 2., 3.])
>>> b.dtype
dtype('float64')
```

첫번째 예제는 숫자가 64-비트(8-바이트) 정수형이고, 두번째 사례는 64-비트 부동소수점 실수다.
넘파이가 자동으로 입력되는 자료형을 탐지하는 기능이 있다.
특수한 자료형은 메모리에 데이터를 좀더 빽빽하게 저장할 수 있는 장점이 있지만, 대부분의 경우 간단히 부동소수점 숫자를 갖고 작업한다.

배열에 모든 원소는 같은 자료형이 되어야 함에 주의한다.
다른 원소를 갖는 배열을 생성하게 되면, 모든 원소를 나타내는 "가장 범용(most general)" 자료형으로 **형변환(cast)** 된다.
예를 들어, 실수와 정수로 구성된 배열은 부동소수점 자료형을 갖게 된다:

```
>>> a = np.array([1., 2])
dtype('float64')
```

이조차도 불가능한 경우, 넘파이는 `object` 객체형을 사용하게 되는데 대문자 `'O'`로 표현되고, 임의 파이썬 객체(심지어 함수)를 나타내게 된다:

```
>>> def f(): pass
>>> a = np.array([f, f])
>>> a.dtype
dtype('O')
```

파이썬 기능 일부(예를 들어 원소별로 적용되는 함수 `np.abs`, `np.sqrt` 등, 혹은 축약함수 `np.sum`, `np.max` 등)는 객체 배열에 동작하지 않지만, 익덱스는 여전히 먹힌다.

다른 길이를 갖는 리스트 다수로 구성되는 배열이 생성될 때, `object` 자료형은 흔히 마주치는 자료형이 된다:

```
>>> np.array([[1], [2, 3]])
array([[1], [2, 3]], dtype=object)
```


> ## 정수 혹은 실수? {.challenge}
>
> `x = np.array([0, 1, 2, 255], dtype=np.uint8)` 명령어로 배열을 생성한다. 
> (여기서 `uint8`은 메모리에 1 바이트, 부호없는 0에서 255 사이 정수를 나타낸다)
> $x+1$과 $frac{x}{2}$ 연산작업 후 얻어지는 결과를 설명할 수 있는가? 
> `x.astype(float) + 1`와 `x.astype(float) / 2`도 시도해본다.

> ## 자료형 {.challenge}
>
> 다음 배열에 대한 자료형을 추측해본다. 그리고 나서, 배열을 생성해보고 예측한 것을 검사해보고 `dtype` 속성을 검사한다.
>
> ```
> a = np.array([[1, 2], 
>               [2, 3]])
> b = np.array(['a', 'b', 'c'])
> c = np.array([1, 2, 'a'])
> d = np.array([np.dot, np.array])
> e = np.random.randn(5) > 0
> f = np.arange(5)
> ```

> ## 복합 자료형 {.challenge}
>
> 넘파이 배열로 저장하려고 하는 것이 이름과 성적점수 목록이라고 가정한다.
> 다음이 동작하는 `dtype`을 생성한다. `np.dtype` 문서를 살펴본다.
>
> ```
> dtype = ?
> np.array([('Bartosz', 5), ('Nelle', 4)], dtype=dtype)
> ```

### 메모리 배치

넘파이 배열은 해당 정보내용을 해석하는 방식을 담은 추가 정보를 갖는 메모리 블록에 불과하다. 
메모리는 선형 주소공간만 갖기 때문에, 넘파이 배열에는 다차원으로 블록을 배열하는 방법에 대한 추가정보가 필요하다.
`shape`와 `strides` 속성으로 이런 작업이 수행된다:

![Shape 와 strides](fig/strides.svg)

상기 예제를 재현해보자. 원소 8개를 갖는 1차원 배열을 먼저 생성시킨다:

```
>>> a = np.arange(8, dtype=np.uint8)
>>> a
array([0, 1, 2, 3, 4, 5, 6, 7], dtype=uint8)
>>> a.strides
(1,)
>>> a.shape
(8,)
```

`shape` 와 `strides` 속성은 읽기전용으로 직접적으로 변경할 수는 없다.
하지만, 함수를 넘파이 라이브러리 모듈에서 `as_strided` 함수를 사용할 수 있다:

```
>>> a1 = np.lib.stride_tricks.as_strided(a, strides=(4, 1), shape=(2,4))
>>> a1
array([[0, 1, 2, 3],
       [4, 5, 6, 7]], dtype=uint8)
```

마찬가지로, 두번째 예제를 다음 코드로 재현할 수 있다:

```
>>> a2 = np.lib.stride_tricks.as_strided(a, strides=(2, 1), shape=(3,4))
>>> a2
array([[0, 1, 2, 3],
       [2, 3, 4, 5],
       [4, 5, 6, 7]], dtype=uint8)
```

두번째 경우에, 동일한 데이터가 두번 나타남에 주목한다. 그렇다고 해서 추가 메모리 공간을 소모하지는 않는다 -- 배열 세개 모두 동일한 메모리 블록을 공유한다:

```
>>> a[2] = 100
>>> a1
array([[  0,   1, 100,   3],
       [  4,   5,   6,   7]], dtype=uint8)
>>> a2
array([[  0,   1, 100,   3],
       [100,   3,   4,   5],
       [  4,   5,   6,   7]], dtype=uint8)
```

> ## 전치(Transpose) {.challenge}
>
> 난수를 원소로 갖는 $3 \times 4$ 배열을 생성한다. 
> 배열의 다양한 속성을 살펴본다: ``x.shape``, ``x.ndim``, ``x.dtype``, ``x.strides``. 
> 배열에 관해서 각 속성이 어떤 정보를 제시하고 있는가?
>
> `x.T` strides 속성을 비교하라. `x.T`는 무엇이고 새로운 strides를 설명할 수 있는가?

> ## 가장 빠른 인덱스 {.challenge}
>
> `A = np.random.rand(10, 100000)` 배열 행과 열에 대해 합을 구하는데 소요되는 시간을 비교하라.
> 차이가 나는 것을 어떻게 설명할 수 있는가?
> (*힌트:* 실행시간을 측정하는데, ipython에 있는 `%timeit`을 사용하라)
 
> ## 슬라이딩 윈도우 {.challenge}
>
> `as_strided` 함수를 사용해서 1차원 배열에 대한 슬라이드 윈도우 뷰를 생성한다.
>
> ```
> def sliding_window(arr, size=2):
>     """Produce an array of sliding window views of `arr`
>     
>     Parameters
>     ----------
>     arr : 1D array, shape (N,)
>         The input array.
>     size : int, optional
>         The size of the sliding window.
>         
>     Returns
>     -------
>     arr_slide : 2D array, shape (N - size - 1, size)
>         The sliding windows of size `size` of `arr`.
>         
>     Examples
>     --------
>     >>> a = np.array([0, 1, 2, 3])
>     >>> sliding_window(a, 2)
>     array([[0, 1],
>            [1, 2],
>            [2, 3]])
>     """
>     return arr  # fix this
> ```

> ## 포트란 방식 혹은 C언어 방식 순서? {.challenge}
>
> `numpy` 함수 `order` 키워드를 통해 2차원 혹은 다차원 배열이 메모리에 저장되는 방식을 결정한다.
> 만약 순서차례가 `C`로 지정되면, 배열은 C-인접 순서(last index varies the fastest)가 된다. 
> 만약 순서차례가 `F`로 지정되면,
> 포트란-인접 차례(first index varies the fastest)가 된다. 
> 2차원 배열은 메모리에 어떤 순서로 저장될까? (*힌트:* `np.ravel(x, order='A')`을 사용해서 검사한다).

> ## 브로드캐스팅 재방문 {.challenge}
>
> 아래 예제를 사용해서 브로드캐스팅이 내부적으로 동작하는 방식을 설명한다.
> 브로드캐스팅 다음에 `x`와 `y` shape와 stride는 어떻게 되는가?
> 다음 예제에 `np.broadcast_arrays`을 사용해서 검증한다. 두 배열에 대해 
> `strides` 와 `shape` 속성을 살펴본다.
>
> ```
> x = np.random.rand(5, 10)
> y = np.random.rand(10)
> z = x + y
>
> xb, yb = np.broadcast_arrays(x, y)
> ```
