# Generated by Django 4.2.7 on 2024-04-09 01:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_maquina', '0002_componente_tipomantenimientocomponente_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mantenimientocomponente',
            name='componente',
        ),
        migrations.RemoveField(
            model_name='mantenimientocomponente',
            name='tipo',
        ),
        migrations.AddField(
            model_name='mantenimientomaquina',
            name='descripción',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='mantenimientomaquina',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='mantenimientomaquina',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(1, 59, 51, 945147)),
        ),
        migrations.AddField(
            model_name='mantenimientomaquina',
            name='image',
            field=models.ImageField(default='', upload_to='maquina/mantenimiento/image'),
        ),
        migrations.AddField(
            model_name='mantenimientomaquina',
            name='partes_y_piezas',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='maquina',
            name='horas_máquina_trabajada',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mantenimientomaquina',
            name='hora',
            field=models.TimeField(default=datetime.time(1, 59, 51, 945183)),
        ),
        migrations.DeleteModel(
            name='Componente',
        ),
        migrations.DeleteModel(
            name='MantenimientoComponente',
        ),
        migrations.DeleteModel(
            name='TipoMantenimientoComponente',
        ),
    ]