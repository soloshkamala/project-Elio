from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
        ('O', 'Не вказано'),
    ]


    email = models.EmailField(unique=True, verbose_name="Пошта")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефону")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', verbose_name="Стать")

    def __str__(self):
        return self.username