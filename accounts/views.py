from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser, OTPVerification
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'psychologist':
            if request.user.is_psychologist_verified:
                return redirect('psychologist_dashboard')
            return redirect('psychologist_pending')
        else:
            return redirect('user_home')  # ПОВЕРНУЛИ СЮДИ user_home

    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        ghost_user = CustomUser.objects.filter(
            Q(username=username) | Q(email=email),
            is_active=False
        ).first()

        if ghost_user:
            ghost_user.delete()

        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            if request.POST.get('is_psychologist') == 'on':
                user.role = 'psychologist'
                user.is_psychologist_verified = False
            else:
                user.role = 'client'

            user.is_active = False
            user.save()

            otp = OTPVerification.objects.create(user=user)
            otp.generate_code()

            send_mail(
                'Код підтвердження ELIO',
                f'Ваш код підтвердження: {otp.code}',
                'noreply@elio.com',
                [user.email],
                fail_silently=False,
            )

            request.session['verify_email'] = user.email
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_otp(request):
    email = request.session.get('verify_email')
    if not email:
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            otp = OTPVerification.objects.filter(user=user).first()

            if otp and otp.code == code:
                user.is_active = True
                user.save()
                otp.delete()

                if 'verify_email' in request.session:
                    del request.session['verify_email']

                login(request, user, backend='accounts.backends.EmailOrUsernameModelBackend')

                if user.role == 'psychologist':
                    if user.is_psychologist_verified:
                        return redirect('psychologist_dashboard')
                    return redirect('psychologist_pending')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_home')  # ПОВЕРНУЛИ СЮДИ user_home

    return render(request, 'accounts/verify_otp.html', {'email': email})


@login_required
def psychologist_pending(request):
    if request.user.role == 'client':
        return redirect('user_home')  # ПОВЕРНУЛИ СЮДИ user_home

    if request.user.role == 'psychologist' and request.user.is_psychologist_verified:
        return redirect('psychologist_dashboard')

    return render(request, 'accounts/psychologist_pending.html')


@login_required
def psychologist_dashboard(request):
    if request.user.role != 'psychologist':
        return redirect('user_home')  # ПОВЕРНУЛИ СЮДИ user_home

    if not request.user.is_psychologist_verified:
        return redirect('psychologist_pending')

    return render(request, 'accounts/psychologist_dashboard_placeholder.html')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('user_home')  # ПОВЕРНУЛИ СЮДИ user_home

    pending_psychologists = CustomUser.objects.filter(role='psychologist', is_psychologist_verified=False)

    clients = CustomUser.objects.filter(role='client').order_by('-date_joined')
    psychologists = CustomUser.objects.filter(role='psychologist', is_psychologist_verified=True).order_by(
        '-date_joined')
    admins = CustomUser.objects.filter(role='admin').exclude(id=request.user.id)

    now = timezone.now()

    context = {
        'pending_psychologists': pending_psychologists,
        'clients': clients,
        'psychologists': psychologists,
        'admins': admins,
        'now': now,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def admin_user_action(request, user_id):
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('user_home')  # ПОВЕРНУЛИ СЮДИ user_home

    target_user = get_object_or_404(CustomUser, id=user_id)
    action = request.POST.get('action')

    if action == 'delete':
        username = target_user.username
        target_user.delete()
        messages.success(request, f'Користувача {username} назавжди видалено.')

    elif action == 'ban_1_week':
        target_user.banned_until = timezone.now() + timedelta(days=7)
        target_user.save()
        messages.warning(request, f'Користувача {target_user.username} відправлено в бан на 7 днів.')

    elif action == 'unban':
        target_user.banned_until = None
        target_user.save()
        messages.success(request, f'Користувача {target_user.username} розбанено.')

    elif action == 'toggle_premium':
        if target_user.role == 'client':
            if target_user.is_premium:
                target_user.premium_until = None
                status = "втратив"
            else:
                target_user.premium_until = timezone.now() + timedelta(days=30)
                status = "отримав на 30 днів"

            target_user.save()
            messages.success(request, f'Клієнт {target_user.username} {status} статус Premium.')

    return redirect('admin_dashboard')


@login_required
def approve_psychologist(request, user_id):
    if request.user.role == 'admin' and request.method == 'POST':
        user_to_approve = get_object_or_404(CustomUser, id=user_id)
        user_to_approve.is_psychologist_verified = True
        user_to_approve.save()
        messages.success(request, f'Спеціаліста {user_to_approve.username} успішно схвалено!')
    return redirect('admin_dashboard')


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)