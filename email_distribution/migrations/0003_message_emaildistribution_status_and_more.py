# Generated by Django 4.2.5 on 2023-09-20 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_distribution', '0002_emaildistribution_period'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Тема письма')),
                ('body', models.TextField(verbose_name='Содержание письма')),
            ],
            options={
                'verbose_name': 'Письмо',
                'verbose_name_plural': 'Письма',
            },
        ),
        migrations.AddField(
            model_name='emaildistribution',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Статус рассылки'),
        ),
        migrations.AlterField(
            model_name='emaildistribution',
            name='period',
            field=models.DurationField(choices=[('1', 'Раз в день'), ('2', 'Раз в неделю'), ('3', 'Раз в месяц')], default='1', verbose_name='Период рассылки'),
        ),
        migrations.AddField(
            model_name='emaildistribution',
            name='message',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='email_distribution.message', verbose_name='Сообщение'),
        ),
    ]