from django.db import models
from django.conf import settings


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (1, '😫 Жахливо'),
        (2, '😔 Погано'),
        (3, '😐 Нормально'),
        (4, '😊 Добре'),
        (5, '🤩 Чудово'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mood_entries'
    )

    date_time = models.DateTimeField(auto_now_add=True)
    mood_level = models.IntegerField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True)
    had_panic_attack = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Настрій: {self.mood_level} ({self.date_time.strftime('%d.%m.%Y %H:%M')})"