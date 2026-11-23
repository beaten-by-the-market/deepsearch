## 계정 단위: 재작성된 계정에서 DeepSearch가 고른 값

| group        |   DS 값 없음 |   둘 다 아님 |   원래값 |   재작성값 |   재작성값 아님 |   합계 |
|:-------------|-------------:|-------------:|---------:|-----------:|----------------:|-------:|
| fixed        |            0 |            0 |        0 |          2 |               0 |      2 |
| ifrs17       |            3 |            0 |        0 |         23 |              57 |     83 |
| restated_cfs |            7 |           14 |      211 |        668 |               0 |    900 |
| restated_ofs |            0 |            1 |      198 |        139 |               0 |    338 |
| 합계         |           10 |           15 |      409 |        832 |              57 |   1323 | 

## 회사·연도 단위 판정

| group        |   원래값 |   재작성값 |   재작성값 아님 |   판정 불가 |   혼합 |   합계 |
|:-------------|---------:|-----------:|----------------:|------------:|-------:|-------:|
| fixed        |        0 |          1 |               0 |           0 |      0 |      1 |
| ifrs17       |        0 |          5 |              13 |           0 |      2 |     20 |
| restated_cfs |       57 |        252 |               0 |           2 |      4 |    315 |
| restated_ofs |       47 |         42 |               0 |           0 |      1 |     90 |
| 합계         |      104 |        300 |              13 |           2 |      7 |    426 | 

### 연도별 (restated_cfs + restated_ofs)

| year   |   원래값 |   재작성값 |   판정 불가 |   혼합 |   합계 |
|:-------|---------:|-----------:|------------:|-------:|-------:|
| 2015   |        6 |         39 |           0 |      0 |     45 |
| 2016   |        6 |         39 |           0 |      0 |     45 |
| 2017   |        6 |         37 |           0 |      2 |     45 |
| 2018   |        5 |         39 |           0 |      1 |     45 |
| 2019   |       13 |         31 |           0 |      1 |     45 |
| 2020   |       16 |         28 |           0 |      1 |     45 |
| 2021   |       17 |         27 |           1 |      0 |     45 |
| 2022   |       13 |         32 |           0 |      0 |     45 |
| 2023   |       22 |         22 |           1 |      0 |     45 |
| 합계   |      104 |        294 |           2 |      5 |    405 | 

### 바뀐 계정 종류별 (원래값/재작성값으로 판정된 회사·연도)

|                            |   원래값 |   재작성값 |   합계 |
|:---------------------------|---------:|-----------:|-------:|
| ('손익만', 'CFS')          |       13 |        163 |    176 |
| ('손익만', 'OFS')          |       10 |         19 |     29 |
| ('재무상태표 포함', 'CFS') |       44 |         89 |    133 |
| ('재무상태표 포함', 'OFS') |       37 |         23 |     60 |
| ('합계', '')               |      104 |        294 |    398 | 

### 연도 × 바뀐 계정 종류

|   year |   ('손익만', '원래값') |   ('손익만', '재작성값') |   ('재무상태표 포함', '원래값') |   ('재무상태표 포함', '재작성값') |
|-------:|-----------------------:|-------------------------:|--------------------------------:|----------------------------------:|
|   2015 |                      3 |                       33 |                               3 |                                 6 |
|   2016 |                      0 |                       26 |                               6 |                                13 |
|   2017 |                      1 |                       18 |                               5 |                                19 |
|   2018 |                      1 |                       23 |                               4 |                                16 |
|   2019 |                      0 |                       16 |                              13 |                                15 |
|   2020 |                      7 |                       13 |                               9 |                                15 |
|   2021 |                      5 |                       16 |                              12 |                                11 |
|   2022 |                      1 |                       21 |                              12 |                                11 |
|   2023 |                      5 |                       16 |                              17 |                                 6 | 

### 계정별 (재작성된 계정만, 일반기업)

| account    |   DS 값 없음 |   둘 다 아님 |   원래값 |   재작성값 |   합계 |
|:-----------|-------------:|-------------:|---------:|-----------:|-------:|
| 당기순이익 |            1 |            4 |       87 |         98 |    190 |
| 매출액     |            1 |            1 |       48 |        189 |    239 |
| 부채총계   |            1 |            2 |       59 |         79 |    141 |
| 영업이익   |            2 |            2 |       66 |        245 |    315 |
| 자본총계   |            1 |            4 |       74 |         99 |    178 |
| 자산총계   |            1 |            2 |       75 |         99 |    177 |
| 합계       |            7 |           15 |      409 |        809 |   1240 | 

## 대조군: 재작성 없는 계정에서 DeepSearch = DART 인가

| account    |   같음 |   둘 다 아님 |   합계 |
|:-----------|-------:|-------------:|-------:|
| 당기순이익 |     89 |            0 |     89 |
| 매출액     |     88 |            1 |     89 |
| 부채총계   |     90 |            0 |     90 |
| 영업이익   |     88 |            1 |     89 |
| 자본총계   |     90 |            0 |     90 |
| 자산총계   |     90 |            0 |     90 |
| 합계       |    535 |            2 |    537 | 

## IFRS17 금융사 2022 (원래값은 OpenDART에 없음)

|                               | 당기순이익   | 부채총계     | 영업이익   | 자본총계     | 자산총계     |
|:------------------------------|:-------------|:-------------|:-----------|:-------------|:-------------|
| ('BNK금융지주', 'CFS')        | not_restated | restated     |            | not_restated | restated     |
| ('DB손해보험', 'CFS')         | not_restated | not_restated |            | not_restated | not_restated |
| ('JB금융지주', 'CFS')         | restated     | restated     |            | restated     | restated     |
| ('KB손해보험', 'CFS')         | not_restated | not_restated | ds_missing | not_restated | not_restated |
| ('iM금융지주', 'CFS')         | not_restated | not_restated |            | not_restated | not_restated |
| ('동양생명보험', 'CFS')       | restated     | restated     |            | restated     | restated     |
| ('롯데손해보험', 'OFS')       | not_restated | not_restated |            | not_restated | not_restated |
| ('메리츠금융지주', 'CFS')     | not_restated | not_restated |            | not_restated | not_restated |
| ('메리츠화재해상보험', 'CFS') | not_restated | not_restated | ds_missing | not_restated | not_restated |
| ('미래에셋생명', 'CFS')       | not_restated | not_restated |            | not_restated | not_restated |
| ('삼성생명', 'CFS')           | not_restated | not_restated |            | not_restated | not_restated |
| ('삼성화재해상보험', 'CFS')   | not_restated | not_restated | ds_missing | not_restated | not_restated |
| ('신한지주', 'CFS')           | not_restated | not_restated |            | not_restated | not_restated |
| ('우리금융지주', 'CFS')       | restated     | restated     |            | restated     | restated     |
| ('하나금융지주', 'CFS')       | not_restated | not_restated |            | not_restated | restated     |
| ('한국금융지주', 'CFS')       | restated     | restated     |            | restated     | restated     |
| ('한화생명', 'CFS')           | not_restated | not_restated |            | not_restated | not_restated |
| ('한화손해보험', 'CFS')       | not_restated | not_restated |            | not_restated | not_restated |
| ('현대해상', 'CFS')           | not_restated | not_restated |            | not_restated | not_restated |
| ('흥국화재', 'OFS')           | restated     | restated     |            | restated     | restated     | 

