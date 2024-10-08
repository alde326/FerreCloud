# Generated by Django 5.0.6 on 2024-07-02 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('documento', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('nivel', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
