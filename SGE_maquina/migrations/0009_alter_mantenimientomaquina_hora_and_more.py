# Generated by Django 4.2.7 on 2024-04-12 23:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_maquina', '0008_alter_mantenimientomaquina_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientomaquina',
            name='hora',
            field=models.TimeField(default=datetime.time(23, 17, 30, 484390)),
        ),
        migrations.AlterField(
            model_name='mantenimientomaquina',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(23, 17, 30, 484346)),
        ),
    ]
