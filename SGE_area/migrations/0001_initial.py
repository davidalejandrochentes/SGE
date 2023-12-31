# Generated by Django 4.2.7 on 2023-11-17 05:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tamaño', models.CharField(max_length=100)),
                ('encargado', models.CharField(max_length=100)),
                ('teléfono_encargado', models.CharField(max_length=100)),
                ('descripción', models.TextField(blank=True, max_length=500, null=True)),
                ('ubicación', models.CharField(blank=True, max_length=100, null=True)),
                ('capacidad', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo_de_área', models.CharField(blank=True, max_length=100, null=True)),
                ('estado_de_ocupación', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_ultimo_mantenimiento', models.DateField(default=datetime.date.today)),
                ('intervalo_mantenimiento', models.IntegerField(default=30)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMantenimientoArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MantenimientoArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_area.area')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_area.tipomantenimientoarea')),
            ],
        ),
    ]
