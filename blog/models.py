from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Ссылка')
    description = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
