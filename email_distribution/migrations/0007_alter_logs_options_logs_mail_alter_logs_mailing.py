# Generated by Django 4.2.5 on 2023-10-12 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_distribution', '0006_emaildistribution_next'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logs',
            options={'verbose_name': 'Лог', 'verbose_name_plural': 'Логи'},
        ),
        migrations.AddField(
            model_name='logs',
            name='mail',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_distribution.emaildistribution', verbose_name='Рассылка'),
        ),
    ]