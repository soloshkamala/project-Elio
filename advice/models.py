from django.db import models
from django.conf import settings


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('advice', 'Порада'),
        ('exercise', 'Вправа'),
    ]
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст")
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='advice',
        verbose_name="Категорія"
    )
    card_color = models.CharField(max_length=7, default='#ff4b2b', verbose_name="Колір картки (HEX)")

    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_articles',
        blank=True
    )

    def __str__(self):
        return self.title