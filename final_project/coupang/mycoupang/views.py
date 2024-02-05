# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_http_methods, require_POST, require_safe
# from django.contrib.auth.decorators import login_required

# # Create your views here.
# @login_required
# def mycoupang(request):
#     return render(request, 'mycoupang/mycoupang.html')

# @require_safe
# def rating_predict(request):
#     return render(request, 'mycoupang/rating_predict.html') 

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, PredictForm
from .models import ReviewsTable, NewReview
import pandas as pd
from mycoupang.KobertModule.classifier import predict
from django.http import JsonResponse
import csv
import os
# from .modules.data_anal import predict


# Create your views here.
@login_required
def mycoupang(request):
    reviews_queryset = ReviewsTable.objects.all()
    reviews_df = pd.DataFrame.from_records(reviews_queryset.values())
    # 새로 생성된 리뷰
    new_reviews_queryset = NewReview.objects.all()
    new_review = pd.DataFrame.from_records(new_reviews_queryset.values())
    
    personalized = []

   
    for idx, review in reviews_df.iterrows():
        if review['userid'] == str(request.user):
            personalized.append(review)
    for idx, review in new_review.iterrows():
        if review['userid'] == str(request.user):
            personalized.append(review)
    print(personalized)
    return render(request, 'mycoupang/mycoupang.html', {'personalized': personalized})

@require_http_methods(["GET", "POST"])
def rating_predict(request):
    if request.method == 'GET':
        form = PredictForm()  # input tag 대신 생성
    
    elif request.method == 'POST':
        form = PredictForm(data=request.POST)

    return render(request, 'mycoupang/rating_predict.html', {
        'form': form,
    })

@require_http_methods(["GET", "POST"])
def rating_predict_ajax(request):
    if request.method == 'POST':
        form = PredictForm(request.POST)
        content = request.POST['review_contents']
        
        predict_result = predict(content)
        # predict_result = json.dumps(predict_result, ensure_ascii = False)
        print(predict_result)
        return JsonResponse({"predict_result" :predict_result})
    
    else:    
        return render(request, 'mycoupang/rating_predict.html', {"predict_result" : None}, {'form': form})    

@login_required
def new_review(request):
    if request.method == 'POST':
        form = ArticleForm()  # input tag 대신 생성
            
    return render(request, 'mycoupang/new_review.html', {
        'form': form,
    })
    
@login_required
@require_http_methods(["GET", "POST"])
def new_review_ajax(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST)
        reviews_queryset = ReviewsTable.objects.all()
        data = pd.DataFrame.from_records(reviews_queryset.values())
        product_name = request.POST['제품']
        new = []
        for idx, review in data.iterrows():
            if review['product_name'] == product_name:
                new.append(review['category1'])
                new.append(review['category2'])
                new.append(review['product_name'])
                new.append(review['product_id'])
        category1 = new[0]
        category2 = new[1]
        product_name = new[2]
        product_id = new[3]
        content = request.POST['review_contents']
        predict_result = predict(content)
        
        userid = request.user
        print(new[0], new[1], content, len(predict_result), userid, product_name)

        # Save the review data to CSV
        review_data = {
            'reviewer_name': userid,
            'userid': userid,
            'review_contents': content,
            'ratings': len(predict_result),
            'product_name': product_name,
            'category1': category1,
            'category2': category2,
            'product_id': product_id,
            
        }
        save_review_to_csv(review_data)

        return JsonResponse({'predict_result': predict_result})

    else:
        form = ArticleForm()

    return render(request, 'mycoupang/new_review.html', {'form': form})

def save_review_to_csv(review_data):
    # Define the CSV file path
    csv_file_path = '/home/lab04/note/data/new_review.csv'

    # Open the CSV file in 'append' mode
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = [
                'reviewer_name',
                'userid',
                'review_contents',
                'ratings',
                'product_name',
                'category1',
                'category2',
                'product_id',
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Append the new review data to the CSV file
    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = [
            'reviewer_name',
            'userid',
            'review_contents',
            'ratings',
            'product_name',
            'category1',
            'category2',
            'product_id',
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({
            'reviewer_name': review_data['userid'],
            'userid': review_data['userid'],
            'review_contents': review_data['review_contents'],
            'ratings': review_data['ratings'],
            'product_name': review_data['product_name'],
            'category1': review_data['category1'],
            'category2': review_data['category2'],
            'product_id': review_data['product_id'],
        })


@require_POST
def get_categories(request):
    target = request.POST.get('target')
    selected_category = request.POST.get('selected_category', '')

    if target == 'category1':
        categories = ReviewsTable.objects.values_list('category1', flat=True).distinct()
    elif target == 'category2':
        categories = ReviewsTable.objects.filter(category1=selected_category).values_list('category2', flat=True).distinct()

    categories = list(categories)
    return JsonResponse(categories, safe=False)


@require_POST
def get_products(request):
    selected_category2 = request.POST.get('selected_category2', '')
    products = ReviewsTable.objects.filter(category2=selected_category2).values_list('제품', flat=True).distinct()
    
    products = list(products)
    return JsonResponse(products, safe=False)