# Generated by Django 5.0.7 on 2024-08-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0002_remove_area_horario_area_horarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='operario',
            name='fecha_ingreso_empresa',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='operario',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='operario',
            name='titulo_tecnico',
            field=models.BooleanField(default=False),
        ),
    ]
