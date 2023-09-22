from django.db import models

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(max_length=100, verbose_name="Электронная почта")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    def __str__(self):
        return f'{self.username} ({self.email})'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Message(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.ForeignKey('email_distribution.Message', on_delete=models.CASCADE, verbose_name='Сообщение')

    def __str__(self):
        return f'{self.user} - {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
