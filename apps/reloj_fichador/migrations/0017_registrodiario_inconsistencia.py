# Generated by Django 5.0.7 on 2024-09-26 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0016_operario_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrodiario',
            name='inconsistencia',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
