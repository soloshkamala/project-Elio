from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        allowed_paths = [
            reverse('home'),
            reverse('login'),
            reverse('register'),
            reverse('verify_otp'),
        ]

        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('home')

        if request.user.is_authenticated:

            if getattr(request.user, 'is_banned', False):
                if request.path != reverse('logout'):
                    logout(request)
                    messages.error(request,
                                   "Ваш акаунт тимчасово заблоковано адміністратором. Ви не можете користуватися сервісом.")
                    return redirect('home')

            if getattr(request.user, 'role', '') == 'psychologist' and not getattr(request.user,
                                                                                   'is_psychologist_verified', False):
                allowed_pending_paths = [
                    reverse('psychologist_pending'),
                    reverse('logout'),
                ]
                if request.path not in allowed_pending_paths:
                    return redirect('psychologist_pending')

        return self.get_response(request)