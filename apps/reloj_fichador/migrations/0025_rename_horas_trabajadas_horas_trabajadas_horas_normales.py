# Generated by Django 5.1.4 on 2024-12-23 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0024_historicalregistrodiario_dif_entrada_salida2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='horas_trabajadas',
            old_name='horas_trabajadas',
            new_name='horas_normales',
        ),
    ]
