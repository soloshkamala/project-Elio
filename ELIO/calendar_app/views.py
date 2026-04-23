import calendar
from datetime import datetime
from django.shortcuts import render


def calendar_view(request):
    today = datetime.now()
    months_to_show = []

    # Створюємо список з 3 місяців (поточний + 2 наступні)
    for i in range(3):
        # Розраховуємо місяць і рік (щоб після грудня правильно йшов січень)
        month = (today.month + i - 1) % 12 + 1
        year = today.year + (today.month + i - 1) // 12

        cal = calendar.monthcalendar(year, month)

        months_to_show.append({
            'name': calendar.month_name[month],
            'year': year,
            'weeks': cal
        })

    context = {
        'months': months_to_show,
    }
    return render(request, 'calendar_app/calendar.html', context)