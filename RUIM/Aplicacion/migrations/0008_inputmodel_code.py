# Generated by Django 4.1.2 on 2022-11-05 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0007_anuncio_inputmodel_asistencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputmodel',
            name='code',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]