# Generated by Django 5.1.3 on 2024-11-27 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0007_alter_mailingtry_date_and_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingtry',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 27, 14, 17, 33, 324388), null=True),
        ),
    ]