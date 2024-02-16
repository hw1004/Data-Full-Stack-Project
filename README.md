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
    - [Deep Learning NLP](#deep-learning-nlp)
    - [Django 웹서비스 구현](#django-웹서비스-구현)
    - [결론 및 향후분석 방향성](#결론-및-향후분석-방향성)
      - [1. 결론](#1-결론)
      - [2. 향후 분석](#2-향후-분석)
    - [프로젝트 후기](#프로젝트-후기)


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

### Deep Learning NLP
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

5. 전체적으로 0.7 정도의 정확도를 나타내지만 overfitting이 일어나기 때문에 새로운 모델인 **Ko-Bert** 모델을 적용함
   - 기존 Bert 모델 : 자연어 처리 딥러닝 모델로 Transformer 아키텍처를 기반으로 하고 양방향 학습을 사용하여 이전의 모델들보다 더 좋은 성능을 보임
   - Ko-Bert : 기존 Bert 모델의 한국어 성능 한계 극복을 위해 개발
   - epoch 5회 진행 후, 정확도 0.8838로 가장 좋게 나타남


### Django 웹서비스 구현
1. 메인 페이지
![스크린샷 2024-02-22 191240](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/ab3041f5-105e-47f4-81d8-fedf16f6691b)

2. 로그인, 회원가입 기능
![스크린샷 2024-02-22 191507](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/54b162a9-b631-4be0-8f24-1251e75b8bff)

3. 리뷰 분석 시각화 (로그인, 비로그인 동일하게 보임)
![스크린샷 2024-02-22 191559](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/5be51c8f-1819-434f-9192-2ee15eb337cc)
4. 제품 추천/카테고리 추천
![스크린샷 2024-02-22 192657](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/66b879e6-3a1f-477f-80b9-1b98142c9005)

- 로그인 시 고객이 작성한 리뷰들에 대한 제품 정보를 기반으로 카테고리와 제품을 추천한다. 카테고리별 **리뷰 개수와 평균 별점**으로 가중치를 준다.
- 비로그인 시 전체 데이터에 대한 리뷰 개수, 평점으로 가중치를 주어 추천을 진행한다.

5. 리뷰 별점 예측 시스템
- 비로그인 고객은 마이쿠팡 메뉴가 아닌 리뷰 별점 예측 메뉴가 보인다. 리뷰를 입력했을 때 그에 대한 예측 별점을 확인해볼 수 있는 기능을 로그인 하지 않아도 사용할 수 있게 기획하였다.

![스크린샷 2024-02-22 192947](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/f6fbf048-281e-4087-af2c-c05af8489ec7)

- 로그인을 한 고객은 마이쿠팡 메뉴가 보인다. 자신이 작성한 리뷰를 마이쿠팡 페이지에서 확인할 수 있다.

![스크린샷 2024-02-22 193038](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/73714878-f294-457f-b073-2f10577bca67)

- 마이쿠팡 페이지에서 새 리뷰 작성 버튼 클릭 시 제품을 선택하고 리뷰를 작성할 수 있다. 이 때, 별점을 따로 고객이 입력하지 않아도 작성한 리뷰를 바탕으로 저장이 되며 저장된 리뷰는 마이쿠팡 페이지에 airflow로 업데이트 된다.

![스크린샷 2024-02-22 193053](https://github.com/hw1004/Data-Full-Stack-Project/assets/109745250/43d2eddf-3b44-4e1a-a953-7f589d7b76c2)

### 결론 및 향후분석 방향성
#### 1. 결론
- 개인이 작성한 리뷰들을 기반으로 맞춤 카테고리와 제품을 제공해 줌으로써 자주, 많이 구매하는 종류의 제품의 구매율을 높일 수 있을 것으로 판단됨.
- 리뷰를 제출하면 자동으로 별점을 예측하는 시스템을 통해 좋은 리뷰를 써 놓고 별점을 잘못 체크해서 1점을 주는 경우를 방지할 수 있을 것으로 예상되며 또한 '거짓 별점'을 걸러내어 다른 소비자에게 더 정확한 리뷰 정보를 전달하여 쇼핑에 도움을 줄 수 있을 것으로 판단됨
- **쿠팡 서비스에서 고객들을 위한 서비스 개선을 목적으로 시나리오를 기획하였고, 찐빵 서비스를 통해 고객들이 더 합리적인 쇼핑을 즐길 수 있을 것이라 판단도딤**

#### 2. 향후 분석
1. 데이터 수집
   - 향후 더 많은 리뷰 데이터를 수집하여 모델에 적용한다면 더 좋은 성능의 모델을 얻을 수 있을 것으로 판단됨.
2. 데이터 파이프라인
   - airflow를 통해 상품 데이터와 리뷰 데이터를 일정 기간에 한번씩 받아오는 스케줄을 추가한다면 더 완성도 있는 파이프라인을 구축할 수 있을 것으로 판단됨.
3. 추천 시스템
   - 향후 전체 리뷰 데이터를 크롤링한 후 시계열 분석을 통해 계절, 이벤트 등에 맞는 제품까지도 추천해줄 수 있을 것으로 판단됨.
4. 데이터 모델링
   - 언어 모델인 transformer, GPT 등도 활용해서 진행해본다면 더 높은 성능을 가진 모델로 서비스를 진행할 수 있을 것으로 판단됨.
### 프로젝트 후기
- 느낀점 : 초기에 프로젝트 주제를 구체화할 때 배운 모든 내용을 적용해보는 것을 목표로 시나리오를 구체화하였다. 시간적으로 촉박하기도 하였고 세미 프로젝트 때보다 시스템적인 오류를 해결해야 하는 시간도 길었지만 결과적으로는 모든 내용을 프로젝트에 녹여내는 것을 성공적으로 해낸 것 같아서 뿌듯하다.
- 아쉬운 점 : 쿠팡 웹사이트가 보안이 잘 되어 있어서 크롤링할 때 여러 문제를 해결해 나가야 했고, API를 사용하지 않고 selenium을 이용해서 크롤링을 하다보니 시간이 많이 걸렸다. 따라서 크롤링 코드를 airflow를 통해 데이터를 계속 업데이트 시키는 부분을 못 해본 것이 아쉽다. 이 부분은 추후에 발전시킬 예정이다.
- 배운 점 : 데이터를 다루는 과정에서 초기 웹서비스 기획이 얼마나 중요한지 알 수 있었다. 어떤 데이터를 수집해야 하고 이를 서비스에 어떻게 적재해야 하는지에 대한 고민을 많이 할 수 있었던 것 같다. 데이터 엔지니어링과 모델링, 웹서비스 구현까지 기술적으로 구현을 하며 배운 부분들도 많지만 결과적으로 하나의 workflow를 따라 서비스를 구현하면서 프로젝트 기획과 관리가 프로젝트를 성공적으로 이끈다는 것을 알 수 있었다.
