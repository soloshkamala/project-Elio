from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_user_page, name='user_home'),
]