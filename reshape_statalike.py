# reshape_wide


def reshape_wide(df,stubnames,i,j):
    """

    Author
    --------
    김완석

    version : 1.0.1
    --------

    version history
    --------
    1.0.0 : 최초 배포(2025.12.14)
    1.0.1 : 파이썬 코드 수정(commented from chatgpt)(2025.12.19)

    Description
    --------

    long->wide로 바꿔주는 함수,
    Stata의 reshape wide 명령어를 토대로 만듦

    Parameters
    ----------
    df : DataFrame
        long form의 데이터
    stubnames : str or list
        Stata의 stubname(조각이름)에 해당.
    i : str or list
        wide로 바꿈에 있어서 축이되는 컬럼(들)에 해당.
    j : str
        wide로 바뀔 때 stubname 뒤에 붙여뒤게 될 값들이 있는 컬럼
        즉 j옵션에 들어가는 컬럼은 wide으로 바뀔 때 사라지게 되는 컬럼임


    Returns
    -------
    wide form의 DataFrame
    
    Warning
    -------
    i 옵션에 들어갈 컬럼들과 j 옵션에 들어가는 컬럼에 중복값이 없어야 됩니다.(가장중요)
    i,j stubnames 이외의 컬럼의 경우 i컬럼(들) 내에 unique해야 합니다.(예제 참조)

    See Also
    --------
    reshape_long 함수
    Stata의 reshape 명령어

    Examples
    --------

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
    
    

    """
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')

    # i옵션과 stubnames list로 바꿔주기

    if type(i)==str:
        i=[i]
    if type(stubnames)==str:
        stubnames=[stubnames]

    # 유효성 검사

    if not(list(df.duplicated(subset=i+[j]).unique()) == [False]):
        raise ValueError(f"i={i+[j]} 컬럼에 중복값이 있습니다. 체크해주세요")

    col_others=list(df.columns).copy()
    for rm in stubnames+[j]:
        col_others.remove(rm)

    temp1=df[col_others].drop_duplicates()
    if not (list(temp1.duplicated(subset=i).unique())==[False]):
        raise ValueError(f"i={i},j={j},stubname={stubnames} 이외의 다른 컬럼(들){[e for e in col_others if not( e in i)]}이 {i} 컬럼 내에서 unique하지 않습니다. 체크해주세요")

    # 시작

    temp2 = (
        df.set_index(i + [j])[stubnames]
        .unstack(j)
    )

    temp2.columns = [f"{stub}{jval}" for stub, jval in temp2.columns]
    temp2 = temp2.reset_index()

    temp2=temp2.merge(temp1,on=i,how='outer') # i옵션에 들어간 컬럼들에 대해 일대일 대응하는 다른 컬럼들을 merge하기
    df_wide=temp2.copy()
    df_wide=df_wide.sort_values(i)
    df_wide=df_wide.reset_index(drop=True)

    return df_wide



# reshape_long


def reshape_long(df,stubnames,i,j):
    """
    Author
    --------
    김완석

    version : 1.0.2
    --------

    version history
    --------
    1.0.0 : 최초 배포(2025.12.14)
    1.0.1 : 파이썬 코드 수정(commented from chatgpt)(2025.12.19)
    1.0.2 : 참고 메시지 디테일하게 수정(2025.12.20)

    Description
    --------
    wide->long로 바꿔주는 함수,
    Stata의 reshape wide 명령어를 토대로 만듦

    Parameters
    ----------
    df : DataFrame
         wide form의 데이터
    stubnames : str or list
        Stata의 stubname(조각이름)에 해당.
    i : str or list
        long으로 바꿈에 있어서 축이되는 컬럼(들)에 해당.
    j : str
        long로 바뀔 때 stubname 뒤에 붙어있는 값들이 새롭게 들어가게 될 컬럼.
        즉 j옵션에 들어가는 값은 long으로 바뀔 때 새롭게 만들어지는 컬럼임


    Returns
    -------
    long form의 DataFrame

    Warning
    -------
    i 옵션에 들어갈 컬럼들에 중복값이 없어야 됩니다.(가장중요)
    i,j stubnames 이외의 컬럼의 경우 i컬럼(들) 내에 unique해야 합니다.(예제 참조)

    See Also
    --------
    reshape_wide 함수
    Stata의 reshape 명령어

    Examples
    --------

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

    """


    import pandas as pd
    import warnings
    import functools
    warnings.filterwarnings('ignore')

    # i옵션과 stubnames list로 바꿔주기
    if type(i)==str:
        i=[i]

    if type(stubnames)==str:
        stubnames=[stubnames]

    # 유효성 검사(체크해서 조건이 안맞으면 빠구시키기)

    if not(list(df.duplicated(subset=i).unique()) == [False]):
        raise ValueError(f"i={i} 컬럼에 중복값이 있습니다. 체크해주세요")

    col_others=list(df.columns).copy()
    for stub in stubnames:
        for col in df.columns:
            if (col not in i) and col.startswith(stub):
                col_others.remove(col)
    temp1=df[col_others]
    if not (list(temp1.duplicated(subset=i).unique())==[False]):
        raise ValueError(f"i={i},stubname={stubnames} 이외의 다른 컬럼(들){[e for e in col_others if not( e in i)]}이 {i} 컬럼 내에서 unique하지 않습니다. 체크해주세요")

    suffix_set = set()
    temp2=df.drop(columns=i) # stubname뒤에 딸려오는 것들 뽑기위해 만든 임시 df

    for col in temp2.columns:
        for stub in stubnames:
            prefix = f"{stub}"
            if col.startswith(prefix):
                suffix = col[len(prefix):]
                suffix_set.add(suffix)

    if not suffix_set:
        raise ValueError("stubnames에 해당하는 컬럼을 찾을 수 없습니다.")

    # 본격적 시작

    dfs = []
    for stub in stubnames:
        temp = (
            df.set_index(i)
                .filter(regex=f"^{stub}")
                .rename(columns=lambda x: x.replace(stub, ""))
                .stack()
                .reset_index()
                .rename(columns={f"level_{len(i)}": j, 0: stub})
        )
        dfs.append(temp)
        dict_col_type={ y: str(df[y].dtypes) for y in df.filter(regex=f'^{stub}')} # stub으로 시작하는 컬럼들의 컬럼명들과 그 컬럼의 type을 딕셔너리로 저장
        if 'object' in dict_col_type.values(): # stub 컬럼들 중에 object 속성이 있다면
            object_cols=[key for key, val in dict_col_type.items() if val == 'object'] # object인 컬럼들의 이름만 뽑기
            print(f"참고: {', '.join(object_cols)} 컬럼은 다른 {stub} 컬럼들과 달리 object type입니다. => '{stub}' 컬럼의 type : object")

    long = functools.reduce(
        lambda l, r: pd.merge(l, r, on=i+[j], how='outer'),
        dfs
    )


    long=long.sort_values(i+[j])
    try : long=long.astype({j:'float'}) # j컬럼의 값들은 대개 숫자인 경우가 많다보니 숫자로 바꿔주기 시도
    except :None # 숫자값이 없으면 안바꾸고 넘어감

    long=long.merge(temp1,on=i,how='outer') # i옵션에 들어간 컬럼들에 대해 일대일 매칭되는 컬럼들을 merge하기
    long=long.reset_index(drop=True)
    long_df=long.copy()
    return long_df

