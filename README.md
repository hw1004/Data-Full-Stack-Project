# 쿠팡 리뷰데이터를 활용한 리뷰 별점 예측 자동화 시스템 및 쇼핑 카테고리 개인화 추천 시스템 개발

- 프로젝트 소개
- 프로젝트 관련 정보
- 개발 환경


## 프로젝트 소개
> 1. 소비자가 제품을 구매할 때 별점은 구매로 이어지는 큰 고려요소입니다. 하지만 쿠팡과 같은 e-commerce 웹사이트에서 제품에 대한 리뷰를 보았을 때, 리뷰 내용과 별점이 일치가 안되는 리뷰들이 자주 존재합니다. 따라서, 리뷰를 작성하면 그에 따른 별점이 자동으로 예측되게 하는 모델을 리뷰 작성 기능에 추가하여 잘못된 별점이 입력되는 것을 방지합니다.
> 2. 수집한 고객 리뷰 데이터와 상품 데이터를 이용해서 로그이니 시 개인이 작성한 리뷰, 별점을 이용한 개인화 세부 카테고리 추천 및 제품 추천 서비스 또한 제공하는 것이 이 프로젝트의 목표입니다.
> 3. 리뷰에 많이 나타나는 단어 또한 워드클라우드를 통해 나타내었습니다.

## 프로젝트 관련 정보
|프로젝트 주제|기업요구사항 기반 문제해결 프로젝트|
|---|---|
|팀 세부 주제|쿠팡 리뷰데이터를 활용한 리뷰 별점 예측 자동화 시스템 및 쇼핑 카테고리 개인화 추천 시스템 개발|
|프로젝트 기간|2023.12.29 ~ 2024.02.08 (3주)|
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
> 쿠팡 웹사이트에서 Selenium을 통해 웹크롤링 진행
1. 15개의 상위 카테고리, 211개의 하위 카테고리 url 수집
2. 상위 카테고리 > 하위 카테고리 상품 데이터 **약 20만개**의 상품 데이터 수집
3. 쿠팡에서 상품별 리뷰는 별 5개의 리뷰가 대부분. 별점 예측 시스템 개발 시 리뷰 개수의 비율 차이로 성능이 안 좋게 나올 것을 예측하여 아래와 같이 **약 16만개의** 리뷰 데이터를 수집
   1. 기존 별 5점 체제에서 최고(5), 보통(4), 별로(3, 2, 1)로 별 3점 체제로 변형
   2. 별 3개의 리뷰 체제 중 리뷰 개수가 가장 적은 별점을 기준으로 다른 별점들에서도 동일한 수만큼의 리뷰 크롤링 진행
