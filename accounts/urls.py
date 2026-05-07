from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('pending/', views.psychologist_pending, name='psychologist_pending'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('psychologist/dashboard/', views.psychologist_dashboard, name='psychologist_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/approve/<int:user_id>/', views.approve_psychologist, name='approve_psychologist'),
    path('admin-panel/action/<int:user_id>/', views.admin_user_action, name='admin_user_action'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]