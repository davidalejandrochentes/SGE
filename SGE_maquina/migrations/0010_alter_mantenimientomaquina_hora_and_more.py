# Generated by Django 4.2.7 on 2024-04-13 11:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_maquina', '0009_alter_mantenimientomaquina_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientomaquina',
            name='hora',
            field=models.TimeField(default=datetime.time(11, 42, 1, 540204)),
        ),
        migrations.AlterField(
            model_name='mantenimientomaquina',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(11, 42, 1, 540175)),
        ),
    ]
