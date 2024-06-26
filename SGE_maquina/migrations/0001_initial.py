# Generated by Django 4.2.7 on 2024-06-06 13:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('encargado', models.CharField(max_length=100)),
                ('teléfono_encargado', models.CharField(max_length=100)),
                ('descripción', models.TextField(max_length=500)),
                ('ubicación', models.CharField(max_length=100)),
                ('tipo_de_máquina', models.CharField(max_length=100)),
                ('número_de_serie_o_modelo', models.CharField(max_length=100)),
                ('proveedor', models.CharField(max_length=100)),
                ('costo_de_adquisición', models.IntegerField()),
                ('fecha_de_adquisición', models.DateField(default=datetime.date.today)),
                ('fecha_de_instalación', models.DateField(default=datetime.date.today)),
                ('estado_de_garantía', models.CharField(max_length=100)),
                ('consumo_de_energía', models.CharField(max_length=100)),
                ('horas_máquina_trabajada', models.IntegerField(default=0)),
                ('intervalo_mantenimiento', models.IntegerField()),
                ('fecha_ultimo_mantenimiento', models.DateField(default=datetime.date.today)),
                ('image', models.ImageField(upload_to='maquina/image')),
            ],
        ),
        migrations.CreateModel(
            name='TipoMantenimientoMaquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MantenimientoMaquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(default=datetime.date.today)),
                ('hora_inicio', models.TimeField(default=datetime.time(13, 42, 36, 127857))),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('hora', models.TimeField(default=datetime.time(13, 42, 36, 127894))),
                ('operador', models.CharField(default='', max_length=100)),
                ('hr_maquina', models.IntegerField(default=0)),
                ('partes_y_piezas', models.TextField(default='', max_length=500)),
                ('descripción', models.TextField(default='', max_length=500)),
                ('image', models.ImageField(default=None, upload_to='maquina/mantenimiento/image')),
                ('image2', models.ImageField(blank=True, default=None, null=True, upload_to='maquina/mantenimiento/image')),
                ('image3', models.ImageField(blank=True, default=None, null=True, upload_to='maquina/mantenimiento/image')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_maquina.maquina')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_maquina.tipomantenimientomaquina')),
            ],
        ),
    ]
