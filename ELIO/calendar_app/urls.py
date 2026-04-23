from django.urls import path
from . import views

urlpatterns = [
    # Має бути views.calendar_view
    path('', views.calendar_view, name='calendar_view'),
]