# Generated by Django 5.1.4 on 2024-12-21 02:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0022_alter_horas_trabajadas_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='horas_trabajadas',
            name='horas_extras',
            field=models.DurationField(default=datetime.timedelta),
        ),
    ]
