# Generated by Django 4.2.7 on 2024-04-12 20:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_herramienta', '0007_alter_mantenimientoherramienta_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientoherramienta',
            name='hora',
            field=models.TimeField(default=datetime.time(20, 3, 40, 487897)),
        ),
    ]
