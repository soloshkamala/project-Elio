from django.urls import path
from . import views

urlpatterns = [
    path('', views.advice_list, name='advice_list'),
path('favorites/', views.favorite_list, name='favorite_list'),
path('article/<int:pk>/', views.article_detail, name='article_detail'),
]