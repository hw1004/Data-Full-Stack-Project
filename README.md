# 쿠팡 리뷰데이터를 활용한 리뷰 별점 예측 자동화 시스템 및 쇼핑 카테고리 개인화 추천 시스템 개발

- [쿠팡 리뷰데이터를 활용한 리뷰 별점 예측 자동화 시스템 및 쇼핑 카테고리 개인화 추천 시스템 개발](#쿠팡-리뷰데이터를-활용한-리뷰-별점-예측-자동화-시스템-및-쇼핑-카테고리-개인화-추천-시스템-개발)
  - [프로젝트 소개](#프로젝트-소개)
  - [프로젝트 관련 정보](#프로젝트-관련-정보)
  - [개발 환경](#개발-환경)
  - [진행 과정](#진행-과정)
    - [Workflow](#workflow)
    - [Data Engineering](#data-engineering)
      - [1. Web crawling](#1-web-crawling)
      - [2. Data Pipeline](#2-data-pipeline)
    - [NLP (DL models)](#nlp-dl-models)


## 프로젝트 소개
> 1. 소비자가 제품을 구매할 때 별점은 구매로 이어지는 큰 고려요소입니다. 하지만 쿠팡과 같은 e-commerce 웹사이트에서 제품에 대한 리뷰를 보았을 때, 리뷰 내용과 별점이 일치가 안되는 리뷰들이 자주 존재합니다. 따라서, 리뷰를 작성하면 그에 따른 별점이 자동으로 예측되게 하는 모델을 리뷰 작성 기능에 추가하여 잘못된 별점이 입력되는 것을 방지합니다.
> 2. 수집한 고객 리뷰 데이터와 상품 데이터를 이용해서 로그이니 시 개인이 작성한 리뷰, 별점을 이용한 개인화 세부 카테고리 추천 및 제품 추천 서비스 또한 제공하는 것이 이 프로젝트의 목표입니다.
> 3. 리뷰에 많이 나타나는 단어 또한 워드클라우드를 통해 나타내었습니다.

## 프로젝트 관련 정보
|프로젝트 주제|기업요구사항 기반 문제해결 프로젝트|
|---|---|
|팀 세부 주제|쿠팡 리뷰데이터를 활용한 리뷰 별점 예측 자동화 시스템 및 쇼핑 카테고리 개인화 추천 시스템 개발|
|프로젝트 기간|2023.12.29 ~ 2024.02.08 (6주)|
|팀원 구성|박건원(조장), 정혜원(부조장), 황서진, 김창현|

## 개발 환경
|||
|---|---|
|Communication|google drive, slack, kakaotalk|
|Languages|python, html5, css3, javascript|
|Frameworks, Servers, and Libraries|django, bootstrap, apache hadoop, apache spark, apache airflow|
|IDEs/Editors|jupyter notebook, visual studio code, google colab|
|Hosting|aws ec2|
|Modeling|tensorflow, keras, pytorch, mxnet, cuda, cudnn|
|Database|MySQL|

## 진행 과정
### Workflow
![workflow (3)](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/ab0eb93f-f6b8-4939-97fc-0ad17f1bb5d3)
### Data Engineering
#### 1. Web crawling
> 쿠팡 웹사이트에서 Selenium을 통해 웹크롤링 진행
1. 15개의 상위 카테고리, 211개의 하위 카테고리 url 수집
2. 상위 카테고리 > 하위 카테고리 상품 데이터 **약 20만개**의 상품 데이터 수집
3. 쿠팡에서 상품별 리뷰는 별 5개의 리뷰가 대부분. 별점 예측 시스템 개발 시 리뷰 개수의 비율 차이로 성능이 안 좋게 나올 것을 예측하여 아래와 같이 **약 16만개의** 리뷰 데이터를 수집
   1. 기존 별 5점 체제에서 최고(5), 보통(4), 별로(3, 2, 1)로 별 3점 체제로 변형
   2. 별 3개의 리뷰 체제 중 리뷰 개수가 가장 적은 별점을 기준으로 다른 별점들에서도 동일한 수만큼의 리뷰 크롤링 진행
#### 2. Data Pipeline
1. **Data Source** : web crawling한 쿠팡 제품, 리뷰 데이터 CSV 파일
2. **Data Lake** : Data source의 CSV 파일을 불러온다.
3. **Data Warehouse** : Pyspark로 transform을 진행하여 DL의 CSV파일을 두개의 table로 변형한다.
   - 제품 데이터에 해당하는 컬럼만 추출한 테이블
   - 리뷰 컬럼을 dataframe 형태로 펼친 테이블
4.  **Data Mart** : 서비스에 사용될 형태로 테이블을 생성하고 테이블들을 Foreign Key로 연결하고 조인을 진행한다.
   - 상품별리뷰 요약
   - 상품 정보
   - 상품 리뷰
5. **Airflow** : 서비스에서 새로 작성된 리뷰를 DL, DW, DM을 거쳐 마이 쿠팡 페이지에 새롭게 보일 수 있도록 airflow를 이용하였다. 각각의 과정을 스케줄로 등록하여 총 3개의 스케줄을 등록하였다.
   - `new_review_hdfs`: hdfs에 새 리뷰가 입력되는 local csv 파일을 넣는 작업
   - `new_review_dw`: hdfs에 있는 new_review 파일을 DW에 적재
   - `new_review_dm`: dw의 new_review table에 id를 PK로 추가하여 DM에 적재

### NLP (DL models)
1. 데이터 전처리 진행 (결측치, 특수문자, 불용어 등 고려)
   - 토근화하고 불용어(stopwords) 제거
   - 토큰화된 학습 데이터를 활용해 단어사전 생성
   - 샘플 길이 맞춘 후 패딩 진행 
2. CNN, RNN, LSTM, BI-LSTM early stopping 걸어서 테스트 진행
   - 최적화 알고리즘: adam
   - 손실 함수: sparse_categorical_crossentropy
   - 평가지표: 정확도
   - 전체적으로 과대적합이 일어남
   - CNN > BI-LSTM > LSTM > RNN 순으로 성능이 좋게 나옴
3. 동일한 조건에서 early stopping을 걸지 않고 테스트 진행
   - 동일하게 전체적으로 과대적합이 일어남
   - CNN > LSTM > BI-LSTM > RNN 순으로 성능이 좋게 나옴
   - early stopping을 설정했을 때보다 성능이 떨어짐
4. 불용어 사전을 한번 더 정리한 후 성능 테스트 진행
   - 전체적으로 성능이 더 떨어짐

||CNN|LSTM|RNN|BI-LSTM|
|---|---|---|---|---|
|es 설정|0.7184|0.7000|0.6884|0.7081|
|es 미설정|0.7098|0.6863|0.6692|0.6805|
|불용어 처리 후 es 설정|0.6872|0.6875|0.6738|0.6810|
|불용어 처리 후 es 미설정|0.6851|0.6725|0.6555|0.6745|

5. 전체적으로 0.7 정도의 정확도를 나타내지만 overfitting이 일어나기 때문에 새로운 모델인 Ko-Bert 모델을 적용함
   - 기존 Bert 모델 : 자연어 처리 딥러닝 모델로 Transformer 아키텍처를 기반으로 하고 양방향 학습을 사용하여 이전의 모델들보다 더 좋은 성능을 보임
   - Ko-Bert : 기존 Bert 모델의 한국어 성능 한계 극복을 위해 개발
   - epoch 5회 진행 후, 정확도 0.8838로 가장 좋게 나타남




