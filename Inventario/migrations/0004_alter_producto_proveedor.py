# Generated by Django 5.0.1 on 2024-09-04 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0003_producto_eliminado'),
        ('Proveedores', '0004_reabastecimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proveedores.proveedor'),
        ),
    ]
