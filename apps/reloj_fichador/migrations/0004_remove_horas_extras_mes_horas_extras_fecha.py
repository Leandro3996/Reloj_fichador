# Generated by Django 5.0.7 on 2024-08-22 11:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0003_operario_fecha_ingreso_empresa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horas_extras',
            name='mes',
        ),
        migrations.AddField(
            model_name='horas_extras',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
