# Generated by Django 5.2 on 2025-05-06 06:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accesorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('salud', models.IntegerField(default=0)),
                ('energia_espiritual', models.IntegerField(default=0)),
                ('defensa', models.IntegerField(default=0)),
                ('velocidad', models.IntegerField(default=0)),
                ('ataque', models.IntegerField(default=0)),
                ('nivel_necesario', models.IntegerField(default=1)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='resources/accesorios/')),
            ],
        ),
        migrations.CreateModel(
            name='Arma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('ataque', models.IntegerField(default=0)),
                ('defensa', models.IntegerField(default=0)),
                ('velocidad', models.IntegerField(default=0)),
                ('nivel_necesario', models.IntegerField(default=1)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='resources/armas/')),
            ],
        ),
        migrations.CreateModel(
            name='Enemigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('salud', models.IntegerField()),
                ('ataque', models.IntegerField()),
                ('defensa', models.IntegerField()),
                ('velocidad', models.IntegerField()),
                ('dificultad', models.CharField(max_length=50)),
                ('experiencia_otorgada', models.IntegerField(default=0)),
                ('oro_otorgado', models.IntegerField(default=0)),
                ('recompensa_especial', models.JSONField(blank=True, default=dict, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('efecto', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Objeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('consumible', 'Consumible'), ('material', 'Material'), ('historia', 'Historia'), ('coleccionable', 'Coleccionable'), ('botin', 'Botin')], max_length=20)),
                ('precio', models.IntegerField(default=20)),
                ('descripcion', models.TextField()),
                ('efecto', models.JSONField(blank=True, default=dict, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='resources/objetos/')),
            ],
        ),
        migrations.CreateModel(
            name='Pasiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('efecto', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Jefe',
            fields=[
                ('enemigo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='battlebound_tactics.enemigo')),
                ('habilidades', models.JSONField(default=dict)),
                ('es_jefe_final', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Jefe',
                'verbose_name_plural': 'Jefes',
            },
            bases=('battlebound_tactics.enemigo',),
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.EmailField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('clase', models.CharField(choices=[('Guerrero', 'Guerrero'), ('Mago', 'Mago'), ('Arquero', 'Arquero'), ('Luchador', 'Luchador'), ('Espiritualista', 'Espiritualista'), ('Astral', 'Astral')], default='Guerrero', max_length=50)),
                ('nivel', models.IntegerField(default=1)),
                ('experiencia', models.IntegerField(default=0)),
                ('experiencia_maxima', models.IntegerField(default=1000)),
                ('alineacion', models.CharField(choices=[('Aliado', 'Aliado'), ('Neutro', 'Neutro'), ('Enemigo', 'Enemigo')], default='Neutro', max_length=10)),
                ('salud_maxima', models.IntegerField(default=100)),
                ('salud', models.IntegerField(default=models.IntegerField(default=100))),
                ('energia_espiritual_maxima', models.IntegerField(default=50)),
                ('energia_espiritual', models.IntegerField(default=models.IntegerField(default=50))),
                ('defensa', models.IntegerField(default=15)),
                ('velocidad', models.IntegerField(default=10)),
                ('ataque', models.IntegerField(default=20)),
                ('medidor_definitiva', models.IntegerField(default=0)),
                ('oro', models.IntegerField(default=0)),
                ('piedras_dragon', models.IntegerField(default=0)),
                ('accesorio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='battlebound_tactics.accesorio')),
                ('arma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='battlebound_tactics.arma')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('habilidad_pasiva', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='battlebound_tactics.pasiva')),
            ],
            options={
                'verbose_name': 'Jugador',
                'verbose_name_plural': 'Jugadores',
            },
        ),
        migrations.CreateModel(
            name='EstadoActivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turnos_restantes', models.IntegerField(default=1)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battlebound_tactics.estado')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados', to='battlebound_tactics.jugador')),
            ],
        ),
        migrations.CreateModel(
            name='Combate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('registro', models.TextField(blank=True, null=True)),
                ('turnos', models.IntegerField(default=0)),
                ('enemigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enemigo', to='battlebound_tactics.enemigo')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jugador', to='battlebound_tactics.jugador')),
            ],
        ),
        migrations.CreateModel(
            name='Mochila',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jugador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mochila', to='battlebound_tactics.jugador')),
            ],
        ),
        migrations.CreateModel(
            name='ObjetoEnMochila',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('mochila', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battlebound_tactics.mochila')),
                ('objeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battlebound_tactics.objeto')),
            ],
        ),
        migrations.AddField(
            model_name='mochila',
            name='objetos',
            field=models.ManyToManyField(through='battlebound_tactics.ObjetoEnMochila', to='battlebound_tactics.objeto'),
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('acciones', models.TextField()),
                ('combate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turnos_info', to='battlebound_tactics.combate')),
            ],
        ),
    ]
