# Generated by Django 5.2 on 2025-05-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battlebound_tactics', '0005_activa_coste_energia_activa_coste_salud_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugador',
            name='energia_espiritual',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='salud',
            field=models.IntegerField(default=100),
        ),
    ]
