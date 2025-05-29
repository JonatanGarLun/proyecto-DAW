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
    Accesorio.objects.create(nombre='Amuleto de Vitalidad', salud=800, energia_espiritual=0, defensa=50, velocidad=0,
                             ataque=0, nivel_necesario=1)
    Accesorio.objects.create(nombre='Anillo de Energía', salud=0, energia_espiritual=600, defensa=0, velocidad=10,
                             ataque=0, nivel_necesario=1)
    Accesorio.objects.create(nombre='Botas de Viento', salud=150, energia_espiritual=150, defensa=0, velocidad=40,
                             ataque=0, nivel_necesario=2)
    Accesorio.objects.create(nombre='Collar de Fuerza', salud=400, energia_espiritual=0, defensa=0, velocidad=0,
                             ataque=100, nivel_necesario=3)
    Accesorio.objects.create(nombre='Pendientes Sagrados', salud=300, energia_espiritual=400, defensa=30, velocidad=5,
                             ataque=0, nivel_necesario=2)
    Accesorio.objects.create(nombre='Capa de Sombras', salud=150, energia_espiritual=150, defensa=50, velocidad=30,
                             ataque=0, nivel_necesario=4)
    Accesorio.objects.create(nombre='Talisman de Hierro', salud=600, energia_espiritual=100, defensa=80, velocidad=0,
                             ataque=0, nivel_necesario=5)
    Accesorio.objects.create(nombre='Broche de Luz', salud=100, energia_espiritual=500, defensa=25, velocidad=10,
                             ataque=30, nivel_necesario=3)
    Accesorio.objects.create(nombre='Sortija de Venganza', salud=0, energia_espiritual=0, defensa=0, velocidad=10,
                             ataque=140, nivel_necesario=5)
    Accesorio.objects.create(nombre='Gargantilla Élfica', salud=500, energia_espiritual=300, defensa=40, velocidad=15,
                             ataque=20, nivel_necesario=4)


def poblar_habilidades_jugador(apps, schema_editor):
    Activa = apps.get_model('battlebound_tactics', 'Activa')

    habilidades = [
        {"nombre": "Explosión Arcana", "descripcion": "Provoca una explosión mágica de gran alcance.",
         "coste_energia": 10, "coste_salud": 0.05, "nivel_necesario": 1,
         "efecto": {"tipo": "dano", "escala_ataque": 3.75, "valor": 100}},
        {"nombre": "Golpe de Luz", "descripcion": "Un ataque con energía sagrada que causa gran daño.",
         "coste_energia": 12, "coste_salud": 0.0, "nivel_necesario": 2,
         "efecto": {"tipo": "dano", "escala_ataque": 3.5, "valor": 150}},
        {"nombre": "Sanación Espiritual", "descripcion": "Recupera una gran cantidad de salud.", "coste_energia": 15,
         "coste_salud": 0.0, "nivel_necesario": 2, "efecto": {"tipo": "curacion", "escala_salud": 0.75, "valor": 200}},
        {"nombre": "Rugido de Guerra", "descripcion": "Aumenta el ataque temporalmente.", "coste_energia": 8,
         "coste_salud": 0.0, "nivel_necesario": 3,
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 100, "duracion": 3, "porcentaje": False}},
        {"nombre": "Muro de Hierro", "descripcion": "Refuerza la defensa durante varios turnos.", "coste_energia": 10,
         "coste_salud": 0.0, "nivel_necesario": 4,
         "efecto": {"tipo": "buff", "stat": "defensa", "valor": 0.2, "duracion": 3, "porcentaje": True}},
        {"nombre": "Debilitar", "descripcion": "Reduce la defensa del enemigo.", "coste_energia": 7, "coste_salud": 0.0,
         "nivel_necesario": 4,
         "efecto": {"tipo": "debuff", "stat": "defensa", "valor": 0.2, "duracion": 3, "porcentaje": True}},
        {"nombre": "Quemadura Interna", "descripcion": "Aplica una quemadura que causa daño progresivo.",
         "coste_energia": 10, "coste_salud": 0.0, "nivel_necesario": 5,
         "efecto": {"tipo": "negativo", "estado": "quemado", "valor": 6, "duracion": 3, "probabilidad": 0.85}},
        {"nombre": "Carga Violenta", "descripcion": "Daño elevado con coste físico.", "coste_energia": 5,
         "coste_salud": 0.1, "nivel_necesario": 6, "efecto": {"tipo": "dano", "escala_ataque": 4.5, "valor": 50}},
        {"nombre": "Flecha Envenenada", "descripcion": "Inflige daño y aplica veneno.", "coste_energia": 10,
         "coste_salud": 0.0, "nivel_necesario": 6,
         "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 5, "duracion": 3, "probabilidad": 0.9}},
        {"nombre": "Inspiración", "descripcion": "Aumenta el ataque del jugador.", "coste_energia": 12,
         "coste_salud": 0.0, "nivel_necesario": 7,
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.25, "duracion": 3, "porcentaje": True}},
        {"nombre": "Fuerza de Voluntad", "descripcion": "Aumenta ligeramente la defensa por algunos turnos.",
         "coste_energia": 8, "coste_salud": 0.0, "nivel_necesario": 8,
         "efecto": {"tipo": "buff", "stat": "defensa", "valor": 50, "duracion": 4, "porcentaje": False}},
        {"nombre": "Velocidad Fantasmal", "descripcion": "Incrementa la velocidad durante dos turnos.",
         "coste_energia": 10, "coste_salud": 0.0, "nivel_necesario": 9,
         "efecto": {"tipo": "buff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True}},
        {"nombre": "Golpe Crítico", "descripcion": "Ataque con alta probabilidad de daño aumentado.",
         "coste_energia": 9, "coste_salud": 0.0, "nivel_necesario": 10,
         "efecto": {"tipo": "dano", "escala_ataque": 4.0, "valor": 100}},
        {"nombre": "Ráfaga de Golpes", "descripcion": "Golpes múltiples de bajo daño.", "coste_energia": 10,
         "coste_salud": 0.0, "nivel_necesario": 6, "efecto": {"tipo": "dano", "escala_ataque": 1.5, "valor": 80}},
        {"nombre": "Impacto Eléctrico", "descripcion": "Aplica un estado de electrocutado.", "coste_energia": 12,
         "coste_salud": 0.0, "nivel_necesario": 7,
         "efecto": {"tipo": "negativo", "estado": "electrocutado", "valor": 4, "duracion": 3, "probabilidad": 0.75}},
        {"nombre": "Furia Descontrolada", "descripcion": "Aumenta ataque, reduce defensa.", "coste_energia": 12,
         "coste_salud": 0.1, "nivel_necesario": 7,
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.4, "duracion": 3, "porcentaje": True}},
        {"nombre": "Invocación Etérea", "descripcion": "Golpea con energía astral.", "coste_energia": 15,
         "coste_salud": 0.0, "nivel_necesario": 8, "efecto": {"tipo": "dano", "escala_ataque": 3.25, "valor": 200}},
        {"nombre": "Golpe Descendente", "descripcion": "Ataque que ignora parte de la defensa enemiga.",
         "coste_energia": 12, "coste_salud": 0.0, "nivel_necesario": 6,
         "efecto": {"tipo": "dano", "escala_ataque": 3.75, "valor": 150}},
        {"nombre": "Giro Cortante", "descripcion": "Ataque giratorio que daña a todos los enemigos.",
         "coste_energia": 13, "coste_salud": 0.05, "nivel_necesario": 9,
         "efecto": {"tipo": "dano", "escala_ataque": 3.0, "valor": 180}},
        {"nombre": "Mirada de Miedo", "descripcion": "Reduce velocidad del enemigo por un corto tiempo.",
         "coste_energia": 9, "coste_salud": 0.0, "nivel_necesario": 4,
         "efecto": {"tipo": "debuff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True}},
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
         "efecto": {"tipo": "daño", "escala_ataque": 3.5, "valor": 120}},
        {"nombre": "Aliento Corrosivo", "descripcion": "Daño continuo mediante veneno.",
         "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 600, "duracion": 3, "probabilidad": 0.85}},
        {"nombre": "Chispa Eléctrica", "descripcion": "Electrocuta al objetivo durante varios turnos.",
         "efecto": {"tipo": "negativo", "estado": "electrocutado", "valor": 500, "duracion": 3, "probabilidad": 0.7}},
        {"nombre": "Furia Demoníaca", "descripcion": "Aumenta su ataque por un tiempo limitado.",
         "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.35, "duracion": 3, "porcentaje": True}},
        {"nombre": "Escamas de Hierro", "descripcion": "Aumenta la defensa del enemigo.",
         "efecto": {"tipo": "buff", "stat": "defensa", "valor": 0.4, "duracion": 3, "porcentaje": True}},
        {"nombre": "Maleficio Lento", "descripcion": "Reduce la velocidad del jugador.",
         "efecto": {"tipo": "debuff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True}},
        {"nombre": "Llama Maldita", "descripcion": "Inflige quemadura dolorosa con alta probabilidad.",
         "efecto": {"tipo": "negativo", "estado": "quemado", "valor": 600, "duracion": 3, "probabilidad": 0.9}},
        {"nombre": "Garra Sangrienta", "descripcion": "Ataque físico potenciado con daño elevado.",
         "efecto": {"tipo": "daño", "escala_ataque": 4.0, "valor": 80}},
        {"nombre": "Regeneración Oscura", "descripcion": "Cura parte de su salud máxima.",
         "efecto": {"tipo": "curacion", "escala_salud": 0.6, "valor": 1500}},
        {"nombre": "Mordida Venenosa", "descripcion": "Ataque con posibilidad de envenenar.",
         "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 500, "duracion": 3, "probabilidad": 0.75}},
    ]
    for h in habilidades:
        ActivaEnemigo.objects.create(nombre=h["nombre"], descripcion=h["descripcion"], efecto=h["efecto"])


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
            "salud_maxima": 98000,
            "salud": 98000,
            "ataque": 9800,
            "defensa": 7840,
            "velocidad": 182,
            "dificultad": "Difícil",
            "experiencia_otorgada": 950000,
            "oro_otorgado": 2000,
            "nivel": 28,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_dificiles/enemigo_fuerte_2.png",
            "habilidades": ["Zarpazo Infernal", "Furia Demoníaca", "Escamas de Hierro"]
        },
        {
            "nombre": "Ares del Abismo",
            "descripcion": "...",
            "salud_maxima": 105000,
            "salud": 105000,
            "ataque": 10500,
            "defensa": 8400,
            "velocidad": 187,
            "dificultad": "Difícil",
            "experiencia_otorgada": 52500,
            "oro_otorgado": 120,
            "nivel": 30,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_dificiles/enemigo_fuerte_1_nobg.png",
            "habilidades": ["Furia Demoníaca", "Garra Sangrienta"]
        },
        # ===========
        # MEDIOS
        # ===========
        {
            "nombre": "Guardián del Bosque Sombrío",  # Equilibrado
            "descripcion": "...",
            "salud_maxima": 600000,
            "salud": 600000,
            "ataque": 4000,
            "defensa": 12500,
            "velocidad": 4600,
            "dificultad": "Media",
            "experiencia_otorgada": 18000,
            "oro_otorgado": 72,
            "nivel": 18,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_medios/enemigo_medio2.png",
            "habilidades": ["Aliento Corrosivo", "Maleficio Lento"]
        },
        {
            "nombre": "Demonio sangriento",
            "descripcion": "...",
            "salud_maxima": 120000,
            "salud": 36000,
            "ataque": 2400,
            "defensa": 6000,
            "velocidad": 120,
            "dificultad": "Media",
            "experiencia_otorgada": 18000,
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
            "salud_maxima": 15000,
            "salud": 15000,
            "ataque": 300,
            "defensa": 400,
            "velocidad": 72,
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
            "salud_maxima": 30000,
            "salud": 30000,
            "ataque": 500,
            "defensa": 500,
            "velocidad": 100,
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
            "salud_maxima": 4000,
            "salud": 4000,
            "ataque": 1000,
            "defensa": 100,
            "velocidad": 400,
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
            "ataque": 200,
            "defensa": 1600,
            "velocidad": 14,
            "dificultad": "Fácil",
            "experiencia_otorgada": 3000,
            "oro_otorgado": 24,
            "nivel": 7,
            "imagen_path": "resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-5.png",
            "habilidades": []
        },
        {
            "nombre": "Bestia de Ébano",  # El más fuerte de las bestias, equilirbado
            "descripcion": "...",
            "salud_maxima": 60000,
            "salud": 60000,
            "ataque": 600,
            "defensa": 600,
            "velocidad": 120,
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
            "ataque": 150,
            "defensa": 300,
            "velocidad": 99,
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
            "salud_maxima": 1750000,
            "salud": 1750000,
            "ataque": 17500,
            "defensa": 14000,
            "velocidad": 40000,
            "dificultad": "Jefe // Muy difícil",
            "experiencia_otorgada": 1750000,
            "oro_otorgado": 8000,
            "nivel": 35,
            "imagen_path": "resources/Pixelarts/enemigos/jefes/jefe_duende.png",
            "habilidades": ["Zarpazo Infernal", "Llama Maldita", "Regeneración Oscura"]
        },
        {
            "nombre": "Havva Skript",  # Equilibrado
            "descripcion": "...",
            "salud_maxima": 20000000,
            "salud": 20000000,
            "ataque": 175000,
            "defensa": 40000,
            "velocidad": 9999999,  # Siempre va primero
            "dificultad": "Jefe // !?!?!",
            "experiencia_otorgada": 20000000,
            "oro_otorgado": 15000,
            "nivel": 1,
            "imagen_path": "resources/Pixelarts/enemigos/jefes/gerbacio.png",
            "habilidades": ["Furia Demoniaca", "Escamas de Hierro", "Regeneración Oscura"]
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
