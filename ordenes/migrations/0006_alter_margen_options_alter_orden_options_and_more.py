# Generated by Django 4.2.3 on 2023-08-24 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0005_margen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='margen',
            options={'verbose_name': 'margen', 'verbose_name_plural': 'margenes'},
        ),
        migrations.AlterModelOptions(
            name='orden',
            options={'verbose_name': 'orden', 'verbose_name_plural': 'ordenes'},
        ),
        migrations.AddField(
            model_name='orden',
            name='valorcuota',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Total Compra'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orden',
            name='fecha',
            field=models.DateField(auto_now=True, verbose_name='Fecha de Compra'),
        ),
    ]
