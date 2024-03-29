# Generated by Django 4.2.7 on 2024-03-26 12:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Herramienta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('número_de_serie', models.CharField(max_length=100)),
                ('encargado', models.CharField(blank=True, max_length=100, null=True)),
                ('teléfono_encargado', models.CharField(blank=True, max_length=100, null=True)),
                ('descripción', models.TextField(blank=True, max_length=500, null=True)),
                ('fecha_de_adquisición', models.CharField(blank=True, max_length=100, null=True)),
                ('costo', models.CharField(blank=True, max_length=100, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=100, null=True)),
                ('ubicación', models.CharField(blank=True, max_length=100, null=True)),
                ('estado_de_la_herramienta', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_ultimo_mantenimiento', models.DateField(default=datetime.date.today)),
                ('intervalo_mantenimiento', models.IntegerField()),
                ('image', models.ImageField(upload_to='herramienta/image')),
            ],
        ),
        migrations.CreateModel(
            name='TipoMantenimientoHerramienta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MantenimientoHerramienta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('hora', models.TimeField(default=datetime.time(12, 58, 14, 620818))),
                ('herramienta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_herramienta.herramienta')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_herramienta.tipomantenimientoherramienta')),
            ],
        ),
    ]
