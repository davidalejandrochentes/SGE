# Generated by Django 4.2.7 on 2024-04-11 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_maquina', '0005_alter_mantenimientomaquina_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimientomaquina',
            name='hora',
            field=models.TimeField(default=datetime.time(18, 44, 12, 649060)),
        ),
        migrations.AlterField(
            model_name='mantenimientomaquina',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(18, 44, 12, 648995)),
        ),
    ]