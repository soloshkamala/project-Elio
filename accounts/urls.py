from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Авторизація та адміністрування
    path('register/', views.register, name='register'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('pending/', views.psychologist_pending, name='psychologist_pending'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('psychologist/dashboard/', views.psychologist_dashboard, name='psychologist_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/approve/<int:user_id>/', views.approve_psychologist, name='approve_psychologist'),
    path('admin-panel/action/<int:user_id>/', views.admin_user_action, name='admin_user_action'),

    # Зміна пароля (зсередини профілю)
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='user_page/password_change.html',
        success_url='/profile/settings/my-profile/'
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='user_page/my_profile.html'
    ), name='password_change_done'),

    # Відновлення пароля по 6-значному коду (Забув пароль)
    path('reset/', views.password_reset_request, name='password_reset_request'),
    path('reset/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('reset/new-password/', views.password_reset_new_password, name='password_reset_new_password'),
]