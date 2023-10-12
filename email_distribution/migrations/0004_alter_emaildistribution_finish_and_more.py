# Generated by Django 4.2.5 on 2023-10-11 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_distribution', '0003_alter_emaildistribution_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaildistribution',
            name='finish',
            field=models.DateTimeField(verbose_name='Дата окончания рассылки'),
        ),
        migrations.AlterField(
            model_name='emaildistribution',
            name='start',
            field=models.DateTimeField(verbose_name='Дата начала рассылки'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='response',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Ответ почтового сервера'),
        ),
    ]
