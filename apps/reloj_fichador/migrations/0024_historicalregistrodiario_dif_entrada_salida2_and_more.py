# Generated by Django 5.1.4 on 2024-12-21 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0023_horas_trabajadas_horas_extras'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalregistrodiario',
            name='dif_entrada_salida2',
            field=models.DurationField(blank=True, help_text='Diferencia E->S (ciclo 2)', null=True),
        ),
        migrations.AddField(
            model_name='historicalregistrodiario',
            name='dif_entrada_salida_total',
            field=models.DurationField(blank=True, help_text='Suma total de diferencias', null=True),
        ),
        migrations.AddField(
            model_name='registrodiario',
            name='dif_entrada_salida2',
            field=models.DurationField(blank=True, help_text='Diferencia E->S (ciclo 2)', null=True),
        ),
        migrations.AddField(
            model_name='registrodiario',
            name='dif_entrada_salida_total',
            field=models.DurationField(blank=True, help_text='Suma total de diferencias', null=True),
        ),
        migrations.AlterField(
            model_name='historicalregistrodiario',
            name='dif_entrada_salida',
            field=models.DurationField(blank=True, help_text='Diferencia E->S (ciclo 1)', null=True),
        ),
        migrations.AlterField(
            model_name='registrodiario',
            name='dif_entrada_salida',
            field=models.DurationField(blank=True, help_text='Diferencia E->S (ciclo 1)', null=True),
        ),
    ]
