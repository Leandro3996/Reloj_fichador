# Generated by Django 5.0.7 on 2024-09-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reloj_fichador', '0014_delete_licencias_licencia_fecha_fin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='operario',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='operarios_fotos/'),
        ),
    ]
