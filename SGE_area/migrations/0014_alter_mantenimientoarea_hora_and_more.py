# Generated by Django 4.2.7 on 2024-04-12 23:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_area', '0013_alter_mantenimientoarea_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientoarea',
            name='hora',
            field=models.TimeField(default=datetime.time(23, 17, 30, 473920)),
        ),
        migrations.AlterField(
            model_name='mantenimientoarea',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(23, 17, 30, 473881)),
        ),
    ]