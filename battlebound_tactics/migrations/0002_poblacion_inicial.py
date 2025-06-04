import os

from django.conf import settings
from django.core.files import File
from django.db import migrations


def poblar_armas(apps, schema_editor):
    Arma = apps.get_model('battlebound_tactics', 'Arma')
    Arma.objects.create(nombre='Espada de Acero', ataque=180, defensa=30, velocidad=10, nivel_necesario=1)
    Arma.objects.create(nombre='Hacha de Guerra', ataque=240, defensa=15, velocidad=-5, nivel_necesario=3)
    Arma.objects.create(nombre='Katana Rúnica', ataque=200, defensa=20, velocidad=20, nivel_necesario=5)
    Arma.objects.create(nombre='Lanza Solar', ataque=190, defensa=25, velocidad=15, nivel_necesario=2)
    Arma.objects.create(nombre='Martillo de la Verdad', ataque=260, defensa=40, velocidad=-10, nivel_necesario=6)
    Arma.objects.create(nombre='Espada del Vacío', ataque=210, defensa=0, velocidad=25, nivel_necesario=4)
    Arma.objects.create(nombre='Dagas Sombrías', ataque=160, defensa=10, velocidad=30, nivel_necesario=1)
    Arma.objects.create(nombre='Arco de los Cielos', ataque=200, defensa=0, velocidad=20, nivel_necesario=3)
    Arma.objects.create(nombre='Báculo del Juicio', ataque=140, defensa=30, velocidad=15, nivel_necesario=4)
    Arma.objects.create(nombre='Espadón Fantasmal', ataque=230, defensa=15, velocidad=5, nivel_necesario=5)


def poblar_accesorios(apps, schema_editor):
    Accesorio = apps.get_model('battlebound_tactics', 'Accesorio')

    Accesorio.objects.create(nombre='Amuleto de Vitalidad', salud=200, energia_espiritual=0, defensa=50, velocidad=0,
                             ataque=0, nivel_necesario=1)
    Accesorio.objects.create(nombre='Anillo de Energía', salud=0, energia_espiritual=100, defensa=0, velocidad=30,
                             ataque=10, nivel_necesario=1)
    Accesorio.objects.create(nombre='Botas de Viento', salud=250, energia_espiritual=50, defensa=0, velocidad=40,
                             ataque=0, nivel_necesario=2)
    Accesorio.objects.create(nombre='Collar de Fuerza', salud=400, energia_espiritual=0, defensa=0, velocidad=0,
                             ataque=120, nivel_necesario=3)
    Accesorio.objects.create(nombre='Pendientes Sagrados', salud=300, energia_espiritual=200, defensa=30, velocidad=5,
                             ataque=50, nivel_necesario=5)
    Accesorio.objects.create(nombre='Capa de Sombras', salud=450, energia_espiritual=150, defensa=50, velocidad=30,
                             ataque=0, nivel_necesario=8)
    Accesorio.objects.create(nombre='Talisman de Hierro', salud=600, energia_espiritual=200, defensa=80, velocidad=0,
                             ataque=0, nivel_necesario=12)
    Accesorio.objects.create(nombre='Broche de Luz', salud=800, energia_espiritual=325, defensa=125, velocidad=10,
                             ataque=130, nivel_necesario=20)
    Accesorio.objects.create(nombre='Sortija de Venganza', salud=0, energia_espiritual=0, defensa=-40, velocidad=60,
                             ataque=140, nivel_necesario=25)
    Accesorio.objects.create(nombre='Gargantilla Élfica', salud=500, energia_espiritual=400, defensa=40, velocidad=15,
                             ataque=20, nivel_necesario=30)
    # SACRIFICIOS
    Accesorio.objects.create(nombre='Sacrificio de ataque', salud=-5000, energia_espiritual=-100, defensa=-5000, velocidad=-1500,
                             ataque=9500, nivel_necesario=50)

    Accesorio.objects.create(nombre='Sacrificio de defensa', salud=15000, energia_espiritual=-200, defensa=10000, velocidad=-400,
                             ataque=-20000, nivel_necesario=50)

    Accesorio.objects.create(nombre='Sacrificio de energía', salud=-10000, energia_espiritual=3000, defensa=-10000, velocidad=0,
                             ataque=3920, nivel_necesario=50)


def poblar_habilidades_jugador(apps, schema_editor):
    Activa = apps.get_model('battlebound_tactics', 'Activa')

    habilidades = [
        {"nombre": "Explosión Arcana", "descripcion": "Provoca una explosión mágica de gran alcance.",
         "coste_energia": 10, "coste_salud": 0.05, "nivel_necesario": 2,
         "efecto": {"tipo": "dano", "escala_ataque": 3.75, "valor": 100}},

        {"nombre": "Golpe de Luz", "descripcion": "Un ataque con energía sagrada que causa gran daño.",
         "coste_energia": 20, "coste_salud": 0.0, "nivel_necesario": 4,
         "efecto": {"tipo": "dano", "escala_ataque": 4.5, "valor": 150}},

        {"nombre": "Sanación Espiritual menor", "descripcion": "Recupera una pequeña cantidad de salud.", "coste_energia": 100,
         "coste_salud": 0.0, "nivel_necesario": 7, "efecto": {"tipo": "curacion", "escala_salud": 0.15, "valor": 200}},

        {"nombre": "Rugido de Guerra", "descripcion": "Aumenta el ataque temporalmente.", "coste_energia": 100,
         "coste_salud": 0.0, "nivel_necesario": 10,
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.2, "duracion": 3, "porcentaje": True}},

        {"nombre": "Muro de Hierro", "descripcion": "Refuerza la defensa ligeramente durante varios turnos.", "coste_energia": 100,
         "coste_salud": 0.0, "nivel_necesario": 10,
         "efecto": {"tipo": "buff", "stat": "defensa", "valor": 0.2, "duracion": 3, "porcentaje": True}},

        {"nombre": "Debilitar", "descripcion": "Reduce la defensa del enemigo.", "coste_energia": 160, "coste_salud": 0.0,
         "nivel_necesario": 14,
         "efecto": {"tipo": "debuff", "stat": "defensa", "valor": 0.3, "duracion": 3, "porcentaje": True}},

        {"nombre": "Quemadura Intensa", "descripcion": "Aplica una quemadura que causa daño cada turno.",
         "coste_energia": 180, "coste_salud": 0.0, "nivel_necesario": 16,
         "efecto": {"tipo": "negativo", "estado": "quemado", "valor": 0.03, "duracion": 2, "probabilidad": 0.85}},

        {"nombre": "Carga Violenta", "descripcion": "Ataque de daño elevado que también daña al jugador.", "coste_energia": 200,
         "coste_salud": 0.1, "nivel_necesario": 20, "efecto": {"tipo": "dano", "escala_ataque": 6.75, "valor": 200}},

        {"nombre": "Púa Venenosa", "descripcion": "Aplica el estado veneno al enemigo.", "coste_energia": 250,
         "coste_salud": 0.0, "nivel_necesario": 25,
         "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 0.06, "duracion": 3, "probabilidad": 0.9}},

        {"nombre": "Inspiración", "descripcion": "Aumenta en gran medida el ataque del jugador.", "coste_energia": 400,
         "coste_salud": 0.1, "nivel_necesario": 35,
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.5, "duracion": 3, "porcentaje": True}},

        {"nombre": "Fuerza de Voluntad", "descripcion": "Aumenta en gran medida la defensa del jugador.",
         "coste_energia": 400, "coste_salud": 0.5, "nivel_necesario": 35,
         "efecto": {"tipo": "buff", "stat": "defensa", "valor": 0.5, "duracion": 4, "porcentaje": True}},

        {"nombre": "Velocidad Fantasmal", "descripcion": "Incrementa la velocidad durante dos turnos.",
         "coste_energia": 400, "coste_salud": 0.0, "nivel_necesario": 35,
         "efecto": {"tipo": "buff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True}},

        {"nombre": "Golpe Crítico", "descripcion": "Ataque cuerpo a cuerpo con altísimo daño y elevado coste.",
         "coste_energia": 1500, "coste_salud": 0.0, "nivel_necesario": 45,
         "efecto": {"tipo": "dano", "escala_ataque": 9.0, "valor": 300}},

        {"nombre": "Ráfaga de Golpes", "descripcion": "Golpes consecutivos que causan daño moderado.", "coste_energia": 700,
         "coste_salud": 0.02, "nivel_necesario": 45, "efecto": {"tipo": "dano", "escala_ataque": 6.5, "valor": 250}},

        {"nombre": "Impacto Eléctrico", "descripcion": "Aplica el estado de electrocutado al enemigo.", "coste_energia": 1200,
         "coste_salud": 0.0, "nivel_necesario": 50,
         "efecto": {"tipo": "negativo", "estado": "electrocutado", "valor": 0.12, "duracion": 2, "probabilidad": 0.75}},

        {"nombre": "Furia Descontrolada", "descripcion": "Aumenta masívamente el ataque a cambio de un coste vital tremendo.", "coste_energia": 1500,
         "coste_salud": 0.25, "nivel_necesario": 55,
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.75, "duracion": 3, "porcentaje": True}},

        {"nombre": "Invocación Etérea", "descripcion": "Golpea con energía astral que daña levemente al jugador.", "coste_energia": 1800,
         "coste_salud": 0.05, "nivel_necesario": 55, "efecto": {"tipo": "dano", "escala_ataque": 9.5, "valor": 400}},

        {"nombre": "Golpe Descendente", "descripcion": "Salta alto y ataca al enemigo con un golpe descendente directo al cuerpo.",
         "coste_energia": 1600, "coste_salud": 0.0, "nivel_necesario": 58,
         "efecto": {"tipo": "dano", "escala_ataque": 9.25, "valor": 450}},

        {"nombre": "Mirada de Miedo", "descripcion": "Reduce en gran medida velocidad del enemigo por un corto tiempo.",
         "coste_energia": 400, "coste_salud": 0.0, "nivel_necesario": 62,
         "efecto": {"tipo": "debuff", "stat": "velocidad", "valor": 0.55, "duracion": 2, "porcentaje": True}},

        {"nombre": "Sanación Espiritual máxima", "descripcion": "Recupera una gran cantidad de salud.",
         "coste_energia": 3000, "coste_salud": 0.0, "nivel_necesario": 65, "efecto": {"tipo": "curacion", "escala_salud": 0.75, "valor": 2000}},

        {"nombre": "Guionazo", "descripcion": "¿Para que jugar limpio cuándo puedes ganar con el poder del guión?",
         "coste_energia": 5000, "coste_salud": 0.33, "nivel_necesario": 99,
         "efecto": {"tipo": "dano", "escala_ataque": 120, "valor": 20000000}} # SOLO PARA LA EXPOSICIÓN, NO ES PERMANENTE
    ]

    for h in habilidades:
        Activa.objects.create(
            nombre=h["nombre"],
            descripcion=h["descripcion"],
            coste_energia=h["coste_energia"],
            coste_salud=h["coste_salud"],
            nivel_necesario=h["nivel_necesario"],
            efecto=h["efecto"]
        )


def poblar_habilidades_enemigo(apps, schema_editor):
    ActivaEnemigo = apps.get_model('battlebound_tactics', 'ActivaEnemigo')
    habilidades = [
        {"nombre": "Zarpazo Infernal", "descripcion": "Un golpe brutal que desgarra la carne.",
         "efecto": {"tipo": "daño", "escala_ataque": 3.5, "valor": 120, "cooldown": 3}},
        {"nombre": "Aliento Corrosivo", "descripcion": "Daño continuo mediante veneno.",
         "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 0.06, "duracion": 3, "probabilidad": 0.85, "cooldown": 5}},
        {"nombre": "Chispa Eléctrica", "descripcion": "Electrocuta al objetivo durante varios turnos.",
         "efecto": {"tipo": "negativo", "estado": "electrocutado", "valor": 0.08, "duracion": 3, "probabilidad": 0.7, "cooldown": 5}},
        {"nombre": "Furia Demoniaca", "descripcion": "Aumenta su ataque por un tiempo limitado.",
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.35, "duracion": 3, "porcentaje": True, "cooldown": 6}},
        {"nombre": "Escamas de Hierro", "descripcion": "Aumenta la defensa del enemigo.",
         "efecto": {"tipo": "buff", "stat": "defensa", "valor": 0.4, "duracion": 3, "porcentaje": True, "cooldown": 6}},
        {"nombre": "Maleficio Lento", "descripcion": "Reduce la velocidad del jugador.",
         "efecto": {"tipo": "debuff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True, "cooldown": 6}},
        {"nombre": "Llama Maldita", "descripcion": "Inflige quemadura dolorosa con alta probabilidad.",
         "efecto": {"tipo": "negativo", "estado": "quemado", "valor": 0.05, "duracion": 2, "probabilidad": 0.9, "cooldown": 5}},
        {"nombre": "Garra Sangrienta", "descripcion": "Ataque físico potenciado con daño elevado.",
         "efecto": {"tipo": "daño", "escala_ataque": 4.0, "valor": 80, "cooldown": 2}},
        {"nombre": "Regeneración Oscura", "descripcion": "Cura parte de su salud máxima.",
         "efecto": {"tipo": "curacion", "escala_salud": 0.6, "valor": 1500, "cooldown": 10}},
        {"nombre": "Mordida Venenosa", "descripcion": "Ataque con posibilidad de envenenar.",
         "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 0.1, "duracion": 3, "probabilidad": 0.75}},
    ]
    for habilidad in habilidades:
        ActivaEnemigo.objects.create(nombre=habilidad["nombre"], descripcion=habilidad["descripcion"], efecto=habilidad["efecto"])


def poblar_enemigos(apps, schema_editor):
    Enemigo = apps.get_model('battlebound_tactics', 'Enemigo')
    ActivaEnemigo = apps.get_model('battlebound_tactics', 'ActivaEnemigo')

    ruta_base = os.path.join(settings.MEDIA_ROOT)

    # Diccionario con todas las habiidades que pueden tener los enemigos
    habilidades_dict = {
        h.nombre: h for h in ActivaEnemigo.objects.all()
    }

    enemigos = [
        # ===========
        # DIFÍCILES
        # ===========
        {
            "nombre": "Centurión del Crepúsculo",
            "descripcion": "...",
            "salud_maxima": 2500000,
            "salud": 2500000,
            "ataque": 30000,
            "defensa": 20000,
            "velocidad": 25000,
            "dificultad": "Muy Difícil",
            "experiencia_otorgada": 95000,
            "oro_otorgado": 2000,
            "nivel": 35,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_dificiles/enemigo_fuerte_2.png",
            "habilidades": ["Zarpazo Infernal", "Furia Demoníaca", "Escamas de Hierro"]
        },
        {
            "nombre": "Ares del Abismo",
            "descripcion": "...",
            "salud_maxima": 1300000,
            "salud": 1300000,
            "ataque": 20000,
            "defensa": 25000,
            "velocidad": 15000,
            "dificultad": "Difícil",
            "experiencia_otorgada": 55500,
            "oro_otorgado": 120,
            "nivel": 28,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_dificiles/enemigo_fuerte_1_nobg.png",
            "habilidades": ["Furia Demoníaca", "Garra Sangrienta"]
        },
        # ===========
        # MEDIOS
        # ===========
        {
            "nombre": "Guardián del Bosque Sombrío",  # Equilibrado
            "descripcion": "...",
            "salud_maxima": 750000,
            "salud": 750000,
            "ataque": 15000,
            "defensa": 20000,
            "velocidad": 12000,
            "dificultad": "Media",
            "experiencia_otorgada": 47000,
            "oro_otorgado": 72,
            "nivel": 23,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_medios/enemigo_medio2.png",
            "habilidades": ["Aliento Corrosivo", "Maleficio Lento"]
        },
        {
            "nombre": "Demonio sangriento",
            "descripcion": "...",
            "salud_maxima": 400000,
            "salud": 400000,
            "ataque": 10000,
            "defensa": 12000,
            "velocidad": 9000,
            "dificultad": "Media",
            "experiencia_otorgada": 33000,
            "oro_otorgado": 72,
            "nivel": 15,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_medios/enemigo_medio1.png",
            "habilidades": ["Chispa Eléctrica"]
        },
        # ===========
        # FÁCILES
        # ===========
        {
            "nombre": "Monje del Rencor",  # Otro enemigo débil, equilibrado
            "descripcion": "...",
            "salud_maxima": 45000,
            "salud": 45000,
            "ataque": 2500,
            "defensa": 2000,
            "velocidad": 550,
            "dificultad": "Fácil",
            "experiencia_otorgada": 7500,
            "oro_otorgado": 20,
            "nivel": 5,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/enemigo_facil_2-1.png",
            "habilidades": []
        },
        {
            "nombre": "Bestia Granate",  # El segundo más fuerte, equilibrado
            "descripcion": "...",
            "salud_maxima": 60000,
            "salud": 60000,
            "ataque": 2300,
            "defensa": 800,
            "velocidad": 1000,
            "dificultad": "Fácil",
            "experiencia_otorgada": 4000,
            "oro_otorgado": 24,
            "nivel": 12,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-6.png",
            "habilidades": []
        },
        {
            "nombre": "Bestia de Cobalto",  # El rápido, equilibrado
            "descripcion": "...",
            "salud_maxima": 20000,
            "salud": 20000,
            "ataque": 4000,
            "defensa": 400,
            "velocidad": 2200,
            "dificultad": "Fácil",
            "experiencia_otorgada": 3000,
            "oro_otorgado": 24,
            "nivel": 6,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-3.png",
            "habilidades": []
        },
        {
            "nombre": "Bestia de Mármol",  # El tanque, equilibrado
            "descripcion": "...",
            "salud_maxima": 60000,
            "salud": 60000,
            "ataque": 600,
            "defensa": 1600,
            "velocidad": 14,
            "dificultad": "Fácil",
            "experiencia_otorgada": 3000,
            "oro_otorgado": 24,
            "nivel": 4,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-5.png",
            "habilidades": []
        },
        {
            "nombre": "Bestia de Ébano",  # El más fuerte de las bestias, equilirbado
            "descripcion": "...",
            "salud_maxima": 120000,
            "salud": 120000,
            "ataque": 6500,
            "defensa": 6500,
            "velocidad": 2200,
            "dificultad": "Fácil",
            "experiencia_otorgada": 25000,
            "oro_otorgado": 28,
            "nivel": 12,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-4.png",
            "habilidades": ["Mordida venenosa"]
        },
        {
            "nombre": "Bestia Carmesí",  # El más débil, equilibrado
            "descripcion": "...",
            "salud_maxima": 5000,
            "salud": 5000,
            "ataque": 500,
            "defensa": 500,
            "velocidad": 500,
            "dificultad": "Muy fácil",
            "experiencia_otorgada": 8000,
            "oro_otorgado": 53,
            "nivel": 3,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-2.png",
            "habilidades": []
        },
        {
            "nombre": "Duende Chillón",  # El enemigo más básico
            "descripcion": "...",
            "salud_maxima": 750,
            "salud": 750,
            "ataque": 100,
            "defensa": 50,
            "velocidad": 88,
            "dificultad": "Extremadamente Fácil",
            "experiencia_otorgada": 1500,
            "oro_otorgado": 12,
            "nivel": 1,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/enemigo_facil_3.png",
            "habilidades": []
        },
        # ===========
        # JEFES
        # ===========
        {
            "nombre": "Gran Jefe Duende y sus Réplicas",
            "descripcion": "...",
            "salud_maxima": 6750000,
            "salud": 6750000,
            "ataque": 45000,
            "defensa": 45000,
            "velocidad": 40000,
            "dificultad": "Jefe // Muy difícil",
            "experiencia_otorgada": 1750000,
            "oro_otorgado": 8000,
            "nivel": 60,
            "imagen_path": "resources/Pixelarts/enemigos/jefes/jefe_duende.png",
            "habilidades": ["Zarpazo Infernal", "Llama Maldita", "Regeneración Oscura"]
        },
        {
            "nombre": "Havva Skript",  # Equilibrado
            "descripcion": "...",
            "salud_maxima": 20000000,
            "salud": 20000000,
            "ataque": 60000,
            "defensa": 40000,
            "velocidad": 9999999,  # Siempre va primero, a no ser que se debuffe o sea un nivel elevadísimo
            "dificultad": "Jefe // !?!?!",
            "experiencia_otorgada": 20000000,
            "oro_otorgado": 15000,
            "nivel": 1,
            "imagen_path": "resources/Pixelarts/enemigos/jefes/gerbacio.png",
            "habilidades": ["Furia Demoniaca", "Llama Maldita", "Regeneración Oscura"]
        }
    ]
    for enemigo in enemigos:
        imagen_absoluta = os.path.join(ruta_base, enemigo["imagen_path"])
        with open(imagen_absoluta, 'rb') as f:
            imagen_enemigo = File(f)

            habilidades = [habilidades_dict.get(nombre) for nombre in enemigo.get("habilidades", [])]

            enemigo_obj = Enemigo(
                nombre=enemigo["nombre"],
                descripcion=enemigo["descripcion"],
                salud_maxima=enemigo["salud_maxima"],
                salud=enemigo["salud"],
                ataque=enemigo["ataque"],
                defensa=enemigo["defensa"],
                velocidad=enemigo["velocidad"],
                dificultad=enemigo["dificultad"],
                experiencia_otorgada=enemigo["experiencia_otorgada"],
                oro_otorgado=enemigo["oro_otorgado"],
                nivel=enemigo["nivel"],
                habilidad_1=habilidades[0] if len(habilidades) > 0 else None,
                habilidad_2=habilidades[1] if len(habilidades) > 1 else None,
                habilidad_3=habilidades[2] if len(habilidades) > 2 else None,
            )
            enemigo_obj.imagen.save(os.path.basename(imagen_absoluta), imagen_enemigo, save=True)


class Migration(migrations.Migration):
    dependencies = [
        ('battlebound_tactics', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(poblar_armas),
        migrations.RunPython(poblar_accesorios),
        migrations.RunPython(poblar_habilidades_jugador),
        migrations.RunPython(poblar_habilidades_enemigo),
        migrations.RunPython(poblar_enemigos),
    ]
