from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .models import MoodEntry, UserProfile

@login_required
def show_user_page(request):
    months_ukr = {1: "січня", 2: "лютого", 3: "березня", 4: "квітня", 5: "травня", 6: "червня",
                  7: "липня", 8: "серпня", 9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня"}
    now = datetime.now()
    current_date_str = f"{now.day} {months_ukr[now.month]}"

    unique_days = MoodEntry.objects.annotate(date_only=TruncDate('date_time')).values('date_only').distinct().count()

    total_entries = MoodEntry.objects.count()
    if total_entries > 0:
        panic_free_count = MoodEntry.objects.filter(had_panic_attack=False).count()
        peace_percentage = int((panic_free_count / total_entries) * 100)
    else:
        peace_percentage = 0

    chart_data = []
    today = now.date()

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_avg = MoodEntry.objects.filter(date_time__date=day).aggregate(Avg('mood_level'))['mood_level__avg']
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
        MoodEntry.objects.create(
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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.first_name = request.POST.get('first_name', '')
        profile.last_name = request.POST.get('last_name', '')
        profile.gender = request.POST.get('gender', '')
        birth_date = request.POST.get('birth_date')
        if birth_date:
            profile.birth_date = birth_date
        profile.save()
        return redirect('my_profile')
    return render(request, 'user_page/my_profile.html', {'profile': profile})

@login_required
def charts_reports_view(request):
    return render(request, 'user_page/charts_reports.html')

@login_required
def reminders_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.reminders_enabled = request.POST.get('reminders_enabled') == 'on'
        profile.save()
        return redirect('reminders')
    return render(request, 'user_page/reminders.html', {'profile': profile})

@login_required
def premium_view(request):
    return render(request, 'user_page/premium.html')

@login_required
def checkout_view(request):
    return render(request, 'user_page/checkout.html')