# Generated by Django 5.0.1 on 2024-11-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proveedores', '0006_remove_reabastecimiento_cantidad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reabastecimiento',
            name='estado',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
