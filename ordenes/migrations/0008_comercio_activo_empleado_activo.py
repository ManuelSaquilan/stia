# Generated by Django 4.2.3 on 2023-09-03 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0007_alter_orden_valorcuota'),
    ]

    operations = [
        migrations.AddField(
            model_name='comercio',
            name='activo',
            field=models.BooleanField(null=True, verbose_name='Activo'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='activo',
            field=models.BooleanField(null=True, verbose_name='Activo'),
        ),
    ]