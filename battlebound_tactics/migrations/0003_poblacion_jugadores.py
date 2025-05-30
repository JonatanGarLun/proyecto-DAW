from django.db import migrations
from django.contrib.auth.hashers import make_password


def crear_jugadores(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Jugador = apps.get_model('battlebound_tactics', 'Jugador')

    jugadores_data = [
        {"username": "JS_lover", "email": "rival1@example.com", "nombre": "Jlou", "clase": "Luchador",
         "nivel": 112, "oro": 100000, "victorias": 100, "derrotas": 20},
        {"username": "Duquer", "email": "rival2@example.com", "nombre": "Ankho", "clase": "Guerrero",
         "nivel": 86, "oro": 85000, "victorias": 80, "derrotas": 40},
        {"username": "Listen&Repeat", "email": "rival3@example.com", "nombre": "Tezerina", "clase": "Arquero",
         "nivel": 144, "oro": 120000, "victorias": 120, "derrotas": 30},
        {"username": "Empresario_007", "email": "rival4@example.com", "nombre": "Irina", "clase": "Mago",
         "nivel": 33, "oro": 50000, "victorias": 50, "derrotas": 60},
        {"username": "Pythonico", "email": "rival5@example.com", "nombre": "Reebest", "clase": "Astral",
         "nivel": 247, "oro": 200000, "victorias": 200, "derrotas": 10},
    ]

    for data in jugadores_data:
        user = User.objects.create(
            username=data["username"],
            email=data["email"],
            password=make_password("contrasenya_defecto_123!"),
            is_active=True
        )
        Jugador.objects.create(
            user=user,
            correo=data["email"],
            nombre=data["nombre"],
            oro=data["oro"],
            nivel= data["nivel"],
            clase=data["clase"],
            victorias=data["victorias"],
            derrotas=data["derrotas"]
        )


class Migration(migrations.Migration):
    dependencies = [
        ('battlebound_tactics', '0002_poblacion_inicial'),
    ]

    operations = [
        migrations.RunPython(crear_jugadores),
    ]
