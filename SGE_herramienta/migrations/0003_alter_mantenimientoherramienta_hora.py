# Generated by Django 4.2.7 on 2024-04-01 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_herramienta', '0002_alter_herramienta_costo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientoherramienta',
            name='hora',
            field=models.TimeField(default=datetime.time(15, 42, 24, 631214)),
        ),
    ]