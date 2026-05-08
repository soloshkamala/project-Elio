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
            return redirect('user_home')

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
                    return redirect('user_home')

    return render(request, 'accounts/verify_otp.html', {'email': email})


@login_required
def psychologist_pending(request):
    if request.user.role == 'client':
        return redirect('user_home')

    if request.user.role == 'psychologist' and request.user.is_psychologist_verified:
        return redirect('psychologist_dashboard')

    if request.method == 'POST':
        bio = request.POST.get('bio')
        diploma = request.FILES.get('diploma_file')

        if bio and diploma:
            request.user.bio = bio
            request.user.diploma_file = diploma
            request.user.save()
            messages.success(request, "Документи успішно завантажено! Очікуйте на перевірку.")
            return redirect('psychologist_pending')
        else:
            messages.error(request, "Будь ласка, заповніть біографію та додайте файл.")

    return render(request, 'accounts/psychologist_pending.html')


@login_required
def psychologist_dashboard(request):
    if request.user.role != 'psychologist':
        return redirect('user_home')
    if not request.user.is_psychologist_verified:
        return redirect('psychologist_pending')

    # В майбутньому тут буде запит до бази: наприклад, кількість його клієнтів
    context = {
        'user': request.user,
        'today': timezone.now(),
    }
    return render(request, 'accounts/psychologist_dashboard.html', context)


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('user_home')

    # АДМІНКА: Показуємо тільки тих, хто реально завантажив диплом
    pending_psychologists = CustomUser.objects.filter(
        role='psychologist',
        is_psychologist_verified=False
    ).exclude(diploma_file='')

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
        return redirect('user_home')

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



def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            # Видаляємо старі коди, якщо були
            OTPVerification.objects.filter(user=user).delete()
            otp = OTPVerification.objects.create(user=user)
            otp.generate_code()

            send_mail(
                'Відновлення паролю ELIO',
                f'Ваш 6-значний код для відновлення: {otp.code}',
                'noreply@elio.com',
                [user.email],
                fail_silently=False,
            )
            request.session['reset_email'] = user.email
            return redirect('password_reset_verify')
        else:
            messages.error(request, "Користувача з такою поштою не знайдено.")
    return render(request, 'accounts/password_reset_request.html')


def password_reset_verify(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('password_reset_request')

    if request.method == 'POST':
        code = request.POST.get('code')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            otp = OTPVerification.objects.filter(user=user).first()
            if otp and otp.code == code:
                otp.delete()
                request.session['reset_verified'] = True  # Прапорець, що код вірний
                return redirect('password_reset_new_password')
            else:
                messages.error(request, "Невірний код. Спробуйте ще раз.")
        # в кінці функції password_reset_verify:
    return render(request, 'accounts/verify_otp.html', {
            'email': email,
            'is_reset': True
        })


def password_reset_new_password(request):
    email = request.session.get('reset_email')
    if not email or not request.session.get('reset_verified'):
        return redirect('password_reset_request')

    if request.method == 'POST':
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password_confirm')

        if pass1 and pass1 == pass2:
            user = CustomUser.objects.filter(email=email).first()
            user.set_password(pass1)
            user.save()

            if 'reset_email' in request.session:
                del request.session['reset_email']
            if 'reset_verified' in request.session:
                del request.session['reset_verified']

            messages.success(request, "Пароль успішно змінено! Тепер ви можете увійти.")
            return redirect('login')
        else:
            messages.error(request, "Паролі не співпадають.")

    return render(request, 'accounts/password_reset_new_password.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)