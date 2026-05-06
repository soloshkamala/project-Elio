from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('pending/', views.psychologist_pending, name='psychologist_pending'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('psychologist/dashboard/', views.psychologist_dashboard, name='psychologist_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/approve/<int:user_id>/', views.approve_psychologist, name='approve_psychologist'),
    path('admin-panel/action/<int:user_id>/', views.admin_user_action, name='admin_user_action'),
    # path('profile/', views.profile, name='profile'), # додам пізніше
]