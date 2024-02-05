from django.shortcuts import render
import pandas as pd
from django.contrib.auth.decorators import login_required
from wordcloud import WordCloud # 워드클라우드 제작 라이브러리
import matplotlib.pyplot as plt # 워드클라우드 시각화 라이브러리
import recommendation.test as test

from .models import LoginRecommend, Reviews, ProductsTable, NoLoginRecommend, New_Review
# Create your views here.
def mainpage(request):
    return render(request, 'recommendation/mainpage.html')
    
def category(request):
    return render(request, 'recommendation/category.html')


# 로그인한 경우_카테고리
def category_recommendation(data):
    products = ProductsTable.objects.all()
    products = pd.DataFrame.from_records(products.values())
    products = products[['category1', 'category2', 'product_name', 'review_count', 'product_rating']]
    print(products)

    products_sample = products
    for idx, row in products_sample.iterrows():
        products_sample.loc[idx, 'product_name'] = row['product_name'].split(',')[0]
    
    products = products_sample.drop_duplicates(subset='product_name', keep='first')
    
    second = products['category2'].unique()
    second = [i.replace(' ', '') for i in second]
    print(second)
    data = data[data['category2'].isin(second)]
    data = data.reset_index()
    print(data)
    data = data[['ratings', 'category1', 'category2']]
    
    data_count = data[['ratings', 'category1', 'category2']]
    data_count.rename(columns = {'ratings': '리뷰 개수'}, inplace=True)
    print(data_count)
    rating = data.groupby(['category1', 'category2']).mean().sort_values(by=['ratings'], ascending=False)
    print(rating)
    counts = data_count.groupby(['category1', 'category2']).count().sort_values(by=['리뷰 개수'], ascending=False)
    print(counts)
    rating_count = pd.concat([rating, counts], axis=1).sort_values(by=['리뷰 개수'], ascending=False)
    print(rating_count)
    
    rating_count['가중 평점'] = rating_count['리뷰 개수'] * rating_count['ratings'] + rating_count['ratings']
    rating_count = rating_count.sort_values(by=['가중 평점'], ascending=False)
    rating_count = rating_count.reset_index()
    print(rating_count)
    top10_category = rating_count.loc[:9]

    return top10_category

# 로그인한 경우, 로그인 안한 경우_상품
def product_recommendation(category1, category2):
    category2 = category2 + " "
    products = NoLoginRecommend.objects.all()
    products = pd.DataFrame.from_records(products.values())
    products = products[(products['category1'] == category1) & (products['category2'] == category2)]
    
    products = products[['category1', 'category2', 'product_name', 'product_rating', 'review_count', 'product_url']]
    
    products_sample = products
    for idx, row in products_sample.iterrows():
        products_sample.loc[idx, 'product_name'] = row['product_name'].split(',')[0]

        products = products_sample.drop_duplicates(subset='product_name', keep='first')
    
    product_df = products

    # average_rating = product_df['product_rating'].mean()
    product_df = product_df.copy()
    product_df['review_count'] = pd.to_numeric(product_df['review_count'], errors='coerce')
    product_df['product_rating'] = pd.to_numeric(product_df['product_rating'], errors='coerce')
    product_df['가중 평점'] = product_df['review_count'] * product_df['product_rating'] + product_df['product_rating']

    product_df = product_df.sort_values(by=['가중 평점'], ascending=False)
    product_df = product_df.reset_index()

    top2_product = product_df.loc[:1]
    return top2_product

# 로그인 안한 경우_카테고리
def no_login_category_recommendation(data):
    products = pd.read_csv('recommendation/data/total.csv')
    
    products_sample = products
    for idx, row in products_sample.iterrows():
        products_sample.loc[idx, '제품명'] = row['제품명'].split(',')[0]
        products = products_sample.drop_duplicates(subset='제품명', keep='first')
        second = products['카테고리2'].unique()
    second = [i.replace(' ', '') for i in second]

    data = products_sample.copy()
    data = data.reset_index()
    
    data = data[['상품 별점', '카테고리1', '카테고리2']]
    
    data_count = data[['상품 별점', '카테고리1', '카테고리2']]
    data_count.rename(columns = {'상품 별점': '리뷰 개수'}, inplace=True)
        
    rating = data.groupby(['카테고리1', '카테고리2']).mean().sort_values(by=['상품 별점'], ascending=False)
        
    counts = data_count.groupby(['카테고리1', '카테고리2']).count().sort_values(by=['리뷰 개수'], ascending=False)
        
    rating_count = pd.concat([rating, counts], axis=1).sort_values(by=['리뷰 개수'], ascending=False)
        
    average_rating = rating_count['상품 별점'].mean()
    rating_count['가중 평점'] = rating_count['리뷰 개수'] * rating_count['상품 별점'] + rating_count['상품 별점'] * average_rating
    rating_count = rating_count.sort_values(by=['가중 평점'], ascending=False)
    rating_count = rating_count.reset_index()
    
    top10_category = rating_count.loc[:9]

    return top10_category


# 로그인 안한 경우
def index_no_login(request):
    data = pd.read_csv('recommendation/data/products_total.csv')
    top10_category = no_login_category_recommendation(data)
    top10 = []
    for i in range(len(top10_category)):
        top10_category.loc[i, '카테고리2'] = top10_category.loc[i, '카테고리2'].strip()
    for i in range(10):
        top10.append([top10_category.loc[i]['카테고리1'], top10_category.loc[i]['카테고리2']])
    
    top2 = []
    for i in range(10):
        category1 = top10[i][0]
        category2 = top10[i][1]
        products = product_recommendation(category1, category2)

        for j in products.index:
            top2.append([products.loc[j]['category1'], products.loc[j]['category2'], products.loc[j]['product_name'], products.loc[j]['product_url'], products.loc[j]['product_rating'], products.loc[j]['review_count']])

    return render(request, 'recommendation/index_no_login.html',{'top10':top10, 'top2':top2})

@login_required
def index(request):
    reviews_queryset = Reviews.objects.all()
    data = pd.DataFrame.from_records(reviews_queryset.values())
    data.loc[data['category2'] == '데코/포장용품', 'category1'] = '문구/오피스'
    data.loc[data['category2'] == '공구/철물/DIY', 'category1'] = '홈인테리어'      
    new_reviews_queryset = New_Review.objects.all()
    data_new = pd.DataFrame.from_records(new_reviews_queryset.values())
    personalized = []
    # reviews_queryset.rename(columns={'리뷰 제목': '제목', '리뷰 내용': '내용'}, inplace=True)
    
    for idx, review in data.iterrows():
        if review['userid'] == str(request.user):
            personalized.append(review)
    for idx, review in data_new.iterrows():
        if review['userid'] == str(request.user):
            personalized.append(review)
    data = pd.DataFrame(personalized)
    
    if (len(data) == 0):
        data1 = pd.read_csv('recommendation/data/products_total.csv')
        top10_category = no_login_category_recommendation(data1)
        top10 = []
        for i in range(len(top10_category)):
            top10_category.loc[i, '카테고리2'] = top10_category.loc[i, '카테고리2'].strip()
        for i in range(10):
            top10.append([top10_category.loc[i]['카테고리1'], top10_category.loc[i]['카테고리2']])
    elif (len(data['category2'].value_counts()) > 10):
        top10_category = category_recommendation(data)
        top10 = []
        for i in range(10):
            top10.append([top10_category.loc[i]['category1'], top10_category.loc[i]['category2']])
        
        
    else:
        data1 = pd.read_csv('recommendation/data/products_total.csv')
        top10_category = no_login_category_recommendation(data1)
        top10 = []
        for i in range(len(top10_category)):
            top10_category.loc[i, '카테고리2'] = top10_category.loc[i, '카테고리2'].strip()
        for i in range(10):
            top10.append([top10_category.loc[i]['카테고리1'], top10_category.loc[i]['카테고리2']])
        
    top2 = []
    for i in range(10):
        category1 = top10[i][0]
        category2 = top10[i][1]
        products = product_recommendation(category1, category2)

        for j in products.index:
            top2.append([products.loc[j]['category1'], products.loc[j]['category2'], products.loc[j]['product_name'],products.loc[j]['product_url'],products.loc[j]['product_rating'],products.loc[j]['review_count'] ])
    print(top2)
    return render(request, 'recommendation/index.html',{'top10':top10, 'top2':top2})

# 워드클라우드
def category(request):
    wordcloud_plt = None
    category1 = ''
    category2 = ''

    if request.method == 'POST':
        # 사용자 입력
        category1 = request.POST.get('topSelect')
        category2 = request.POST.get('bottomSelect') 
        
        wordcloud_plt = test.wordcloud(category1, category2)
        print(wordcloud_plt)
    return render(request, 'recommendation/category.html', {'wordcloud_plt':wordcloud_plt, 'category1':category1, 'category2':category2})