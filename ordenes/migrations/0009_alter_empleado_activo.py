# Generated by Django 4.2.3 on 2023-09-03 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0008_comercio_activo_empleado_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='activo',
            field=models.BooleanField(default=True, null=True, verbose_name='Activo'),
        ),
    ]
