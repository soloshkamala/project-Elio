from django.shortcuts import render
from datetime import datetime


def show_user_page(request):
    months_ukr = {
        1: "січня", 2: "лютого", 3: "березня", 4: "квітня",
        5: "травня", 6: "червня", 7: "липня", 8: "серпня",
        9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня"
    }

    now = datetime.now()
    current_date_str = f"{now.day} {months_ukr[now.month]}"

    context = {
        'current_date': current_date_str,
        'days_count': 0,
        'peace_percentage': 0,
        'chart_data': [0, 0, 0, 0, 0]
    }

    return render(request, 'user_page/index.html', context)