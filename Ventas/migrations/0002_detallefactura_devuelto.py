# Generated by Django 5.0.1 on 2024-08-31 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallefactura',
            name='devuelto',
            field=models.BooleanField(default=False),
        ),
    ]
