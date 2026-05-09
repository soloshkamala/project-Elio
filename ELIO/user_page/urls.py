from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.show_user_page, name='user_home'),
    path('add/', views.add_mood_view, name='add_mood'),

    path('settings/', views.settings_view, name='settings'),
    path('settings/my-profile/', views.my_profile_view, name='my_profile'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='user_page/password_change.html',
        success_url=reverse_lazy('my_profile')
    ), name='password_change'),

    path('settings/charts/', views.charts_reports_view, name='charts_reports'),
    path('settings/reminders/', views.reminders_view, name='reminders'),
    path('settings/premium/', views.premium_view, name='premium'),
    path('settings/premium/checkout/', views.checkout_view, name='checkout'),

    # ==========================================
    # НОВІ ШЛЯХИ ДЛЯ ПСИХОЛОГІВ
    # ==========================================
    path('specialists/', views.specialists_list, name='specialists'),
    path('specialists/contact/<int:psy_id>/', views.contact_specialist, name='contact_specialist'),
]