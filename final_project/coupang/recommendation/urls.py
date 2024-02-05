from django.urls import path
from . import views

app_name = 'recommendation'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('recommendation/', views.index, name='index'),
    path('recommendation_new/', views.index_no_login, name='index_no_login'),
    path('category/', views.category, name='category'),

]
