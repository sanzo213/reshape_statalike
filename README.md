# reshape_statalike
Stata의 reshape 명령어를 python pandas로 구현함
pandas의 `melt` / `pivot`가 너무 불편하고 공수가 들어서 만들었으며 Sata와 같은 reshape 작업(엑셀의 pivot에 해당)을 가능하게 해줌

Stata-style `reshape` implementation for pandas.

Many Stata users find pandas `melt` / `pivot` unintuitive.
This package provides a Stata-like reshape interface in Python.

## 주된 함수
1. reshape_wide
2. reshape_long

### 1. reshape_wide
#### version : 1.0.1
#### version history
    1.0.0 : 최초 배포(2025.12.14)
    1.0.1 : 파이썬 코드 수정(commented from chatgpt)(2025.12.19)
    
#### Description
    long->wide로 바꿔주는 함수,
    Stata의 reshape wide 명령어를 토대로 만듦

#### Parameters
    df : DataFrame
        long form의 데이터
    stubnames : str or list
        Stata의 stubname(조각이름)에 해당.
    i : str or list
        wide로 바꿈에 있어서 축이되는 컬럼(들)에 해당.
    j : str
        wide로 바뀔 때 stubname 뒤에 붙여뒤게 될 값들이 있는 컬럼
        즉 j옵션에 들어가는 컬럼은 wide으로 바뀔 때 사라지게 되는 컬럼임
#### Returns
    wide form의 DataFrame

#### Warning
    i 옵션에 들어갈 컬럼들과 j 옵션에 들어가는 컬럼에 중복값이 없어야 됩니다.(가장중요)
    i,j stubnames 이외의 컬럼의 경우 i컬럼(들) 내에 unique해야 합니다.(예제 참조)

#### See Also
    reshape_long 함수
    Stata의 reshape 명령어

#### Examples

    >>> lst=[['김철수', 1, 20.0, 83.0, 'A'],
            ['김철수', 3, 21.0, 80.0, 'A'],
            ['사마천', 1, 33.0, 67.0, 'B'],
            ['사마천', 2, 50.0, 73.0, 'B'],
            ['사마천', 3, 54.0, 59.0, 'B'],
            ['이형희', 1, 35.0, 56.0, 'B'],
            ['이형희', 2, 36.0, 46.0, 'B'],
            ['이형희', 3, 33.0, 48.0, 'B'],
            ['제갈량', 1, 45.0, 62.0, 'B'],
            ['제갈량', 2, 46.0, 63.0, 'B'],
            ['제갈량', 3, 38.0, 66.0, 'B'],
            ['조두식', 1, 27.0, 62.0, 'A'],
            ['조두식', 2, 29.0, 70.0, 'A']]

    >>> df=pd.DataFrame(lst,columns=['이름', '일차', '제기차기', '팔굽혀펴기', '조'])
    >>> df
             이름  일차  제기차기  팔굽혀펴기  조
    0   김철수   1  20.0   83.0  A
    1   김철수   3  21.0   80.0  A
    2   사마천   1  33.0   67.0  B
    3   사마천   2  50.0   73.0  B
    4   사마천   3  54.0   59.0  B
    5   이형희   1  35.0   56.0  B
    6   이형희   2  36.0   46.0  B
    7   이형희   3  33.0   48.0  B
    8   제갈량   1  45.0   62.0  B
    9   제갈량   2  46.0   63.0  B
    10  제갈량   3  38.0   66.0  B
    11  조두식   1  27.0   62.0  A
    12  조두식   2  29.0   70.0  A
    
    >>> reshape_wide(df,i='이름',j='일차',stubnames=['제기차기', '팔굽혀펴기'])
            이름  제기차기1  팔굽혀펴기1  제기차기2  팔굽혀펴기2  제기차기3  팔굽혀펴기3  조
    0  김철수   20.0    83.0    NaN     NaN   21.0    80.0  A
    1  사마천   33.0    67.0   50.0    73.0   54.0    59.0  B
    2  이형희   35.0    56.0   36.0    46.0   33.0    48.0  B
    3  제갈량   45.0    62.0   46.0    63.0   38.0    66.0  B
    4  조두식   27.0    62.0   29.0    70.0    NaN     NaN  A

### 2. reshape_long
#### version : 1.0.2

#### version history
    1.0.0 : 최초 배포(2025.12.14)
    1.0.1 : 파이썬 코드 수정(commented from chatgpt)(2025.12.19)
    1.0.2 : 참고 메시지 디테일하게 수정(2025.12.20)

#### Description
    wide->long로 바꿔주는 함수,
    Stata의 reshape wide 명령어를 토대로 만듦

#### Parameters
    df : DataFrame
         wide form의 데이터
    stubnames : str or list
        Stata의 stubname(조각이름)에 해당.
    i : str or list
        long으로 바꿈에 있어서 축이되는 컬럼(들)에 해당.
    j : str
        long로 바뀔 때 stubname 뒤에 붙어있는 값들이 새롭게 들어가게 될 컬럼.
        즉 j옵션에 들어가는 값은 long으로 바뀔 때 새롭게 만들어지는 컬럼임


#### Returns
    long form의 DataFrame

#### Warning
    i 옵션에 들어갈 컬럼들에 중복값이 없어야 됩니다.(가장중요)
    i,j stubnames 이외의 컬럼의 경우 i컬럼(들) 내에 unique해야 합니다.(예제 참조)

#### See Also
    reshape_wide 함수
    Stata의 reshape 명령어

#### Examples
    >>> lst=[['김철수', 20.0, 83.0, None, None, 21.0, 80.0, 'A'],
       ['사마천', 33.0, 67.0, 50.0, 73.0, 54.0, 59.0, 'B'],
       ['이형희', 35.0, 56.0, 36.0, 46.0, 33.0, 48.0, 'B'],
       ['제갈량', 45.0, 62.0, 46.0, 63.0, 38.0, 66.0, 'B'],
       ['조두식', 27.0, 62.0, 29.0, 70.0, None, None, 'A']
        ]

    >>> df=pd.DataFrame(lst,columns=['이름', '제기차기1', '팔굽혀펴기1', '제기차기2', '팔굽혀펴기2', '제기차기3', '팔굽혀펴기3', '조'])
    >>> df
        이름  제기차기1  팔굽혀펴기1  제기차기2  팔굽혀펴기2  제기차기3  팔굽혀펴기3  조
    0  김철수   20.0    83.0    NaN     NaN   21.0    80.0  A
    1  사마천   33.0    67.0   50.0    73.0   54.0    59.0  B
    2  이형희   35.0    56.0   36.0    46.0   33.0    48.0  B
    3  제갈량   45.0    62.0   46.0    63.0   38.0    66.0  B
    4  조두식   27.0    62.0   29.0    70.0    NaN     NaN  A

    >>> reshape_long(df,i='이름',j='day',stubnames=['제기차기','팔굽혀펴기'])
         이름  day  제기차기  팔굽혀펴기  조
    0   김철수  1.0  20.0   83.0  A
    1   김철수  2.0   NaN    NaN  A
    2   김철수  3.0  21.0   80.0  A
    3   사마천  1.0  33.0   67.0  B
    4   사마천  2.0  50.0   73.0  B
    5   사마천  3.0  54.0   59.0  B
    6   이형희  1.0  35.0   56.0  B
    7   이형희  2.0  36.0   46.0  B
    8   이형희  3.0  33.0   48.0  B
    9   제갈량  1.0  45.0   62.0  B
    10  제갈량  2.0  46.0   63.0  B
    11  제갈량  3.0  38.0   66.0  B
    12  조두식  1.0  27.0   62.0  A
    13  조두식  2.0  29.0   70.0  A
    14  조두식  3.0   NaN    NaN  A
