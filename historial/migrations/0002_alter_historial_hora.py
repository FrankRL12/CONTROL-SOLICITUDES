# Generated by Django 5.0.4 on 2024-04-03 21:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historial',
            name='hora',
            field=models.TimeField(default=datetime.time(15, 49, 5, 1809)),
        ),
    ]
