# Generated by Django 4.2.7 on 2024-06-06 13:40

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
            ],
        ),
        migrations.CreateModel(
            name='Parte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('image', models.ImageField(default=None, upload_to='repuesto/image')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_repuesto.maquina')),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(default='', max_length=50)),
                ('rosca', models.CharField(default='', max_length=50)),
                ('largo', models.CharField(default='', max_length=50)),
                ('und', models.CharField(default='', max_length=50)),
                ('cantidad_necesaria', models.IntegerField()),
                ('existencia_stock', models.IntegerField()),
                ('salida', models.IntegerField()),
                ('parte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGE_repuesto.parte')),
            ],
        ),
    ]
