# Generated by Django 4.2.5 on 2023-09-20 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_distribution', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaildistribution',
            name='period',
            field=models.DurationField(default=datetime.timedelta(days=1), verbose_name='Период рассылки'),
        ),
    ]
