from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/secret-admin-elio/') or request.path.startswith('/media/') or request.path.startswith('/static/'):
            return self.get_response(request)

        allowed_paths = [
            reverse('home'),
            reverse('login'),
            reverse('register'),
            reverse('verify_otp'),
            reverse('password_reset_request'),
            reverse('password_reset_verify'),
            reverse('password_reset_new_password'),
        ]

        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('home')

        if request.user.is_authenticated:
            if getattr(request.user, 'is_banned', False):
                if request.path != reverse('logout'):
                    local_date = timezone.localtime(request.user.banned_until)
                    ban_date_str = local_date.strftime("%d.%m.%Y %H:%M")

                    messages.error(
                        request,
                        f"Ваш акаунт тимчасово заблоковано адміністратором до {ban_date_str}.",
                        extra_tags='banned_popup'
                    )

                    logout(request)
                    return redirect('home')

            if getattr(request.user, 'role', '') == 'psychologist' and not getattr(request.user, 'is_psychologist_verified', False):
                allowed_pending_paths = [
                    reverse('psychologist_pending'),
                    reverse('logout'),
                ]
                if request.path not in allowed_pending_paths:
                    return redirect('psychologist_pending')

            if getattr(request.user, 'role', '') == 'admin':
                if request.path.startswith('/profile/') or request.path == reverse('home'):
                    if request.path != reverse('logout'):
                        return redirect('admin_dashboard')

        return self.get_response(request)