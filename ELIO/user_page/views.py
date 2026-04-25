from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import MoodEntry
from django.db.models.functions import TruncDate
from django.db.models import Avg, Count


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
    return redirect('/profile/')