# Generated by Django 4.1.1 on 2022-11-19 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0013_alter_inputmodel_autores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputmodel',
            name='correo',
            field=models.EmailField(max_length=250, unique=True),
        ),
    ]
