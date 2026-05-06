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
    # Твій код без змін
    date_time = models.DateTimeField(auto_now_add=True)
    mood_level = models.IntegerField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True)
    had_panic_attack = models.BooleanField(default=False)

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    reminders_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Профіль {self.user.username}"