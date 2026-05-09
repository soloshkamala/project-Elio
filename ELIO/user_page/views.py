from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .models import MoodEntry
from django.contrib import messages
from django.utils import timezone

# Додаємо імпорт CustomUser з додатку accounts для сторінки психологів
from accounts.models import CustomUser


@login_required
def show_user_page(request):
    months_ukr = {1: "січня", 2: "лютого", 3: "березня", 4: "квітня", 5: "травня", 6: "червня",
                  7: "липня", 8: "серпня", 9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня"}
    now = datetime.now()
    current_date_str = f"{now.day} {months_ukr[now.month]}"

    # БЕРЕМО ДАНІ ТІЛЬКИ ПОТОЧНОГО ЮЗЕРА (Раніше брало всіх підряд)
    user_entries = MoodEntry.objects.filter(user=request.user)

    unique_days = user_entries.annotate(date_only=TruncDate('date_time')).values('date_only').distinct().count()

    total_entries = user_entries.count()
    if total_entries > 0:
        panic_free_count = user_entries.filter(had_panic_attack=False).count()
        peace_percentage = int((panic_free_count / total_entries) * 100)
    else:
        peace_percentage = 0

    chart_data = []
    today = now.date()

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_avg = user_entries.filter(date_time__date=day).aggregate(Avg('mood_level'))['mood_level__avg']
        if day_avg:
            chart_data.append(int(day_avg * 20))
        else:
            chart_data.append(0)

    context = {
        'current_date': current_date_str,
        'days_count': unique_days,
        'peace_percentage': peace_percentage,
        'chart_data': chart_data
    }
    return render(request, 'user_page/index.html', context)


@login_required
def add_mood_view(request):
    if request.method == "POST":
        mood_level = request.POST.get('mood_level')
        note = request.POST.get('note')
        panic = request.POST.get('had_panic_attack') == 'on'

        # ПРИВ'ЯЗУЄМО НАСТРІЙ ДО ЮЗЕРА
        MoodEntry.objects.create(
            user=request.user,
            mood_level=int(mood_level),
            note=note,
            had_panic_attack=panic
        )
    return redirect('user_home')


@login_required
def settings_view(request):
    return render(request, 'user_page/settings.html')


@login_required
def my_profile_view(request):
    # ЗБЕРІГАЄМО ДАНІ ПРЯМО В CUSTOM USER
    if request.method == "POST":
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.phone_number = request.POST.get('phone_number', '')
        request.user.gender = request.POST.get('gender', 'O')
        request.user.core_issues = request.POST.get('core_issues', '')

        birth_date = request.POST.get('birth_date')
        if birth_date:
            request.user.birth_date = birth_date

        # Якщо юзер завантажив фотку
        if 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']

        # Якщо психолог завантажив диплом через профіль
        if 'diploma_file' in request.FILES:
            request.user.diploma_file = request.FILES['diploma_file']

        request.user.save()
        return redirect('my_profile')

    return render(request, 'user_page/my_profile.html')


@login_required
def charts_reports_view(request):
    return render(request, 'user_page/charts_reports.html')


@login_required
def reminders_view(request):
    # НАЛАШТУВАННЯ ТЕЖ В CUSTOM USER
    if request.method == "POST":
        request.user.reminders_enabled = request.POST.get('reminders_enabled') == 'on'
        request.user.save()
        return redirect('reminders')
    return render(request, 'user_page/reminders.html')


@login_required
def checkout_view(request):
    if request.method == "POST":
        user = request.user
        user.premium_until = timezone.now() + timedelta(days=30)
        user.save()

        messages.success(request, "Premium активовано! Тепер тобі доступні всі функції аналітики.")

        return redirect('premium')

    return render(request, 'user_page/checkout.html')


@login_required
def premium_view(request):
    return render(request, 'user_page/premium.html')


# ==========================================
# НОВІ ФУНКЦІЇ ДЛЯ СТОРІНКИ ПСИХОЛОГІВ
# ==========================================

@login_required
def specialists_list(request):
    # Беремо всіх користувачів, у яких роль 'psychologist'
    psychologists = CustomUser.objects.filter(role='psychologist')
    return render(request, 'user_page/specialists.html', {'psychologists': psychologists})

@login_required
def contact_specialist(request, psy_id):
    # Шукаємо конкретного психолога за його ID
    psychologist = get_object_or_404(CustomUser, id=psy_id, role='psychologist')
    return render(request, 'user_page/contact_specialist.html', {'psychologist': psychologist})