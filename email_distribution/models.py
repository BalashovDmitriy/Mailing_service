from django.db import models

from users.models import User


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Содержание письма')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class EmailDistribution(models.Model):
    emails = models.ManyToManyField('users.User')
    time = models.DateTimeField(verbose_name='Время рассылки')
    period = models.CharField(choices=[('1', 'Раз в день'), ('2', 'Раз в неделю'), ('3', 'Раз в месяц')],
                              default='1', verbose_name='Период рассылки')
    status = models.PositiveSmallIntegerField(default=1, verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', default=None)

    def __str__(self):
        return f'{self.emails} ({self.time})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Logs(models.Model):
    time = models.DateTimeField(verbose_name='Дата и время последней попытки', default=None)
    status = models.ForeignKey(EmailDistribution, on_delete=models.CASCADE, verbose_name='Статус рассылки')
    response = models.BooleanField(default=False, verbose_name='Ответ почтового сервера')
