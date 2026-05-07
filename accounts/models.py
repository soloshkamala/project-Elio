from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random


def user_directory_path(instance, filename):
    return f'user_{instance.id}/{filename}'


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
        ('O', 'Не вказано'),
    ]

    ROLE_CHOICES = (
        ('client', 'Client'),
        ('psychologist', 'Psychologist'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True, verbose_name="Пошта")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефону")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', verbose_name="Стать")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name="Фото профілю")
    core_issues = models.TextField(blank=True, null=True, verbose_name="Що турбує")
    reminders_enabled = models.BooleanField(default=True, verbose_name="Нагадування увімкнені")

    is_psychologist_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    diploma_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    banned_until = models.DateTimeField(null=True, blank=True, verbose_name="Забанений до")
    premium_until = models.DateTimeField(null=True, blank=True, verbose_name="Преміум діє до")

    @property
    def is_premium(self):
        if self.premium_until and self.premium_until > timezone.now():
            return True
        return False

    @property
    def is_banned(self):
        if self.banned_until and self.banned_until > timezone.now():
            return True
        return False

    def __str__(self):
        return self.username


class OTPVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code = str(random.randint(100000, 999999))
        self.save()