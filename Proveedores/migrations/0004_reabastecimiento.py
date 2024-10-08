# Generated by Django 5.0.1 on 2024-08-25 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0003_producto_eliminado'),
        ('Proveedores', '0003_proveedor_eliminado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reabastecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('credito', models.BooleanField(default=False)),
                ('eliminado', models.BooleanField(default=False)),
                ('observaciones', models.CharField(max_length=200)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proveedores.proveedor')),
            ],
        ),
    ]
