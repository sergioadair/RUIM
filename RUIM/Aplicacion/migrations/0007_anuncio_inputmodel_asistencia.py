# Generated by Django 4.1.1 on 2022-11-03 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0006_alter_inputmodel_resumen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=255)),
                ('Cuerpo', models.TextField()),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='inputmodel',
            name='asistencia',
            field=models.BooleanField(default=False),
        ),
    ]
