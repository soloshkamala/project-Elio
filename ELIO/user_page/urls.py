from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_user_page, name='user_home'),
    path('add/', views.add_mood_view, name='add_mood'),
]