# Generated by Django 5.0.7 on 2024-09-26 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0015_operario_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='operario',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
