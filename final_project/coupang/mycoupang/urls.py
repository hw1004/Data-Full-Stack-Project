from django.urls import path
from . import views

app_name = 'mycoupang'
urlpatterns = [
    path('mycoupang/', views.mycoupang, name='mypage'),
    path('rating_predict/', views.rating_predict, name='rating_predict'),
    path('rating_predict_ajax/', views.rating_predict_ajax, name='rating_predict_ajax'),
    path('new_review/', views.new_review, name='new_reviews'),
    path('new_review_ajax/', views.new_review_ajax, name='new_review_ajax'),
]
