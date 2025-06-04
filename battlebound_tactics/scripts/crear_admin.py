import os
import django
from dotenv import load_dotenv

# Cargar entorno y configurar Django
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_final.settings')
django.setup()

from django.contrib.auth.models import User
from battlebound_tactics.models import Jugador
from battlebound_tactics.core.globales.estadisticas import generar_pasiva_aleatoria_jugador

# Cargar credenciales desde el entorno
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')

if not all([username, password, email]):
    raise Exception("Faltan variables necesarias en el archivo ..env")

# Crear superusuario si no existe
user, created = User.objects.get_or_create(username=username, defaults={
    'email': email,
    'is_staff': True,
    'is_superuser': True
})
if created:
    user.set_password(password)
    user.save()
    print(f"Superusuario con nombre '{username}' creado.")
else:
    print(f"Superusuario con nombre '{username}' ya existe.")

# Crear el jugador si no existe
if not hasattr(user, 'jugador'):
    jugador = Jugador.objects.create(
        user=user,
        correo=email,
        nombre="Héroe legendario",
        clase="Astral",
        nivel= 100,
        salud_maxima=2475993,
        salud= 2475993,
        energia_espiritual_maxima=8000,
        energia_espiritual=8000,
        ataque= 300000,
        defensa= 170000,
        velocidad= 166804,
        experiencia_maxima= 14000000
    )
    print(f"Jugador creado para '{username}'.")

    # Asignar una pasiva aleatoria
    generar_pasiva_aleatoria_jugador(jugador)
    print(f"Pasiva aleatoria asignada a '{jugador.nombre}'.")
    print(f"Su personaje completo ha sido creado con éxito.")
else:
    print(f"El usuario '{username}' ya tiene un jugador asignado.")