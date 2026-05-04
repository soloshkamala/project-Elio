from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_user_page, name='user_home'),
    path('add/', views.add_mood_view, name='add_mood'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/my-profile/', views.my_profile_view, name='my_profile'),
    path('settings/charts/', views.charts_reports_view, name='charts_reports'),
    path('settings/reminders/', views.reminders_view, name='reminders'),
    path('settings/premium/', views.premium_view, name='premium'),
path('settings/premium/checkout/', views.checkout_view, name='checkout'),
]