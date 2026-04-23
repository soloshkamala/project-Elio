from django.db import models

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

    card_color = models.CharField(max_length=7, default='#FCE4EC', verbose_name="Колір картки (HEX)")
    is_favorite = models.BooleanField(default=False, verbose_name="В обраному")
    def __str__(self):
        return self.title