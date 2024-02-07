# Generated by Django 4.2.7 on 2024-02-07 19:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SGE_area', '0003_area_image_alter_mantenimientoarea_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='image',
            field=models.ImageField(upload_to='area/image'),
        ),
        migrations.AlterField(
            model_name='area',
            name='intervalo_mantenimiento',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='mantenimientoarea',
            name='hora',
            field=models.TimeField(default=datetime.time(19, 0, 51, 982263)),
        ),
    ]
