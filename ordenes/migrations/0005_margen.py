# Generated by Django 4.2.1 on 2023-08-10 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0004_alter_orden_fecha_alter_orden_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Margen',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('margen', models.IntegerField(verbose_name='Margen')),
            ],
            options={
                'db_table': 'margen',
            },
        ),
    ]
