# Generated by Django 4.2.7 on 2024-04-01 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_pc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientopc',
            name='hora',
            field=models.TimeField(default=datetime.time(15, 42, 24, 607757)),
        ),
    ]