# Generated by Django 4.1.1 on 2022-11-03 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0003_inputmodel_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputmodel',
            name='resumen',
            field=models.FileField(null=True, upload_to=models.EmailField(max_length=250)),
        ),
    ]