# Generated by Django 5.0.1 on 2024-03-04 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamitos', '0003_prestamo_total_pagar'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='avatar',
            field=models.URLField(blank=True, null=True),
        ),
    ]
