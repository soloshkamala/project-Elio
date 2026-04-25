from django.db import models
from django.utils import timezone


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (1, '😫 Жахливо'),
        (2, '😔 Погано'),
        (3, '😐 Нормально'),
        (4, '😊 Добре'),
        (5, '🤩 Чудово'),
    ]
    date_time = models.DateTimeField(auto_now_add=True)
    mood_level = models.IntegerField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True)
    had_panic_attack = models.BooleanField(default=False)