# Generated by Django 5.0.6 on 2024-07-09 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
    ]
