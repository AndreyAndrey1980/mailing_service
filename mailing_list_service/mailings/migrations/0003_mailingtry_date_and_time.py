# Generated by Django 5.1.3 on 2024-11-25 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0002_remove_mailingtry_owner_mailingtry_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingtry',
            name='date_and_time',
            field=models.DateTimeField(null=True),
        ),
    ]
