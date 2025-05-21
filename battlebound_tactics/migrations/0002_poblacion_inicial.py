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
    Accesorio.objects.create(nombre='Amuleto de Vitalidad', salud=800, energia_espiritual=0, defensa=50, velocidad=0, ataque=0, nivel_necesario=1)
    Accesorio.objects.create(nombre='Anillo de Energía', salud=0, energia_espiritual=600, defensa=0, velocidad=10, ataque=0, nivel_necesario=1)
    Accesorio.objects.create(nombre='Botas de Viento', salud=150, energia_espiritual=150, defensa=0, velocidad=40, ataque=0, nivel_necesario=2)
    Accesorio.objects.create(nombre='Collar de Fuerza', salud=400, energia_espiritual=0, defensa=0, velocidad=0, ataque=100, nivel_necesario=3)
    Accesorio.objects.create(nombre='Pendientes Sagrados', salud=300, energia_espiritual=400, defensa=30, velocidad=5, ataque=0, nivel_necesario=2)
    Accesorio.objects.create(nombre='Capa de Sombras', salud=150, energia_espiritual=150, defensa=50, velocidad=30, ataque=0, nivel_necesario=4)
    Accesorio.objects.create(nombre='Talisman de Hierro', salud=600, energia_espiritual=100, defensa=80, velocidad=0, ataque=0, nivel_necesario=5)
    Accesorio.objects.create(nombre='Broche de Luz', salud=100, energia_espiritual=500, defensa=25, velocidad=10, ataque=30, nivel_necesario=3)
    Accesorio.objects.create(nombre='Sortija de Venganza', salud=0, energia_espiritual=0, defensa=0, velocidad=10, ataque=140, nivel_necesario=5)
    Accesorio.objects.create(nombre='Gargantilla Élfica', salud=500, energia_espiritual=300, defensa=40, velocidad=15, ataque=20, nivel_necesario=4)

def poblar_habilidades_jugador(apps, schema_editor):
    Activa = apps.get_model('battlebound_tactics', 'Activa')

    habilidades = [
        {"nombre": "Explosión Arcana", "descripcion": "Provoca una explosión mágica de gran alcance.", "coste_energia": 10, "coste_salud": 0.05, "nivel_necesario": 1, "efecto": {"tipo": "daño", "escala_ataque": 3.75, "valor": 100}},
        {"nombre": "Golpe de Luz", "descripcion": "Un ataque con energía sagrada que causa gran daño.", "coste_energia": 12, "coste_salud": 0.0, "nivel_necesario": 2, "efecto": {"tipo": "daño", "escala_ataque": 3.5, "valor": 150}},
        {"nombre": "Sanación Espiritual", "descripcion": "Recupera una gran cantidad de salud.", "coste_energia": 15, "coste_salud": 0.0, "nivel_necesario": 2, "efecto": {"tipo": "curacion", "escala_salud": 0.75, "valor": 200}},
        {"nombre": "Rugido de Guerra", "descripcion": "Aumenta el ataque temporalmente.", "coste_energia": 8, "coste_salud": 0.0, "nivel_necesario": 3, "efecto": {"tipo": "buff", "stat": "ataque", "valor": 100, "duracion": 3, "porcentaje": False}},
        {"nombre": "Muro de Hierro", "descripcion": "Refuerza la defensa durante varios turnos.", "coste_energia": 10, "coste_salud": 0.0, "nivel_necesario": 4, "efecto": {"tipo": "buff", "stat": "defensa", "valor": 0.2, "duracion": 3, "porcentaje": True}},
        {"nombre": "Debilitar", "descripcion": "Reduce la defensa del enemigo.", "coste_energia": 7, "coste_salud": 0.0, "nivel_necesario": 4, "efecto": {"tipo": "debuff", "stat": "defensa", "valor": 0.2, "duracion": 3, "porcentaje": True}},
        {"nombre": "Quemadura Interna", "descripcion": "Aplica una quemadura que causa daño progresivo.", "coste_energia": 10, "coste_salud": 0.0, "nivel_necesario": 5, "efecto": {"tipo": "negativo", "estado": "quemado", "valor": 6, "duracion": 3, "probabilidad": 0.85}},
        {"nombre": "Carga Violenta", "descripcion": "Daño elevado con coste físico.", "coste_energia": 5, "coste_salud": 0.1, "nivel_necesario": 6, "efecto": {"tipo": "daño", "escala_ataque": 4.5, "valor": 50}},
        {"nombre": "Flecha Envenenada", "descripcion": "Inflige daño y aplica veneno.", "coste_energia": 10, "coste_salud": 0.0, "nivel_necesario": 6, "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 5, "duracion": 3, "probabilidad": 0.9}},
        {"nombre": "Inspiración", "descripcion": "Aumenta el ataque del jugador.", "coste_energia": 12, "coste_salud": 0.0, "nivel_necesario": 7, "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.25, "duracion": 3, "porcentaje": True}},
        {"nombre": "Fuerza de Voluntad", "descripcion": "Aumenta ligeramente la defensa por algunos turnos.", "coste_energia": 8, "coste_salud": 0.0, "nivel_necesario": 8, "efecto": {"tipo": "buff", "stat": "defensa", "valor": 50, "duracion": 4, "porcentaje": False}},
        {"nombre": "Velocidad Fantasmal", "descripcion": "Incrementa la velocidad durante dos turnos.", "coste_energia": 10, "coste_salud": 0.0, "nivel_necesario": 9, "efecto": {"tipo": "buff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True}},
        {"nombre": "Golpe Crítico", "descripcion": "Ataque con alta probabilidad de daño aumentado.", "coste_energia": 9, "coste_salud": 0.0, "nivel_necesario": 10, "efecto": {"tipo": "daño", "escala_ataque": 4.0, "valor": 100}},
        {"nombre": "Ráfaga de Golpes", "descripcion": "Golpes múltiples de bajo daño.", "coste_energia": 10, "coste_salud": 0.0, "nivel_necesario": 6, "efecto": {"tipo": "daño", "escala_ataque": 1.5, "valor": 80}},
        {"nombre": "Impacto Eléctrico", "descripcion": "Aplica un estado de electrocutado.", "coste_energia": 12, "coste_salud": 0.0, "nivel_necesario": 7, "efecto": {"tipo": "negativo", "estado": "electrocutado", "valor": 4, "duracion": 3, "probabilidad": 0.75}},
        {"nombre": "Furia Descontrolada", "descripcion": "Aumenta ataque, reduce defensa.", "coste_energia": 12, "coste_salud": 0.1, "nivel_necesario": 7, "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.4, "duracion": 3, "porcentaje": True}},
        {"nombre": "Invocación Etérea", "descripcion": "Golpea con energía astral.", "coste_energia": 15, "coste_salud": 0.0, "nivel_necesario": 8, "efecto": {"tipo": "daño", "escala_ataque": 3.25, "valor": 200}},
        {"nombre": "Golpe Descendente", "descripcion": "Ataque que ignora parte de la defensa enemiga.", "coste_energia": 12, "coste_salud": 0.0, "nivel_necesario": 6, "efecto": {"tipo": "daño", "escala_ataque": 3.75, "valor": 150}},
        {"nombre": "Giro Cortante", "descripcion": "Ataque giratorio que daña a todos los enemigos.", "coste_energia": 13, "coste_salud": 0.05, "nivel_necesario": 9, "efecto": {"tipo": "daño", "escala_ataque": 3.0, "valor": 180}},
        {"nombre": "Mirada de Miedo", "descripcion": "Reduce velocidad del enemigo por un corto tiempo.", "coste_energia": 9, "coste_salud": 0.0, "nivel_necesario": 4, "efecto": {"tipo": "debuff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True}},
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
        {"nombre": "Zarpazo Infernal", "descripcion": "Un golpe brutal que desgarra la carne.", "efecto": {"tipo": "daño", "escala_ataque": 3.5, "valor": 120}},
        {"nombre": "Aliento Corrosivo", "descripcion": "Daño continuo mediante veneno.", "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 6, "duracion": 3, "probabilidad": 0.85}},
        {"nombre": "Chispa Eléctrica", "descripcion": "Electrocuta al objetivo durante varios turnos.", "efecto": {"tipo": "negativo", "estado": "electrocutado", "valor": 5, "duracion": 3, "probabilidad": 0.7}},
        {"nombre": "Furia Demoníaca", "descripcion": "Aumenta su ataque por un tiempo limitado.", "efecto": {"tipo": "buff", "stat": "ataque", "valor": 0.35, "duracion": 3, "porcentaje": True}},
        {"nombre": "Escamas de Hierro", "descripcion": "Aumenta la defensa del enemigo.", "efecto": {"tipo": "buff", "stat": "defensa", "valor": 0.4, "duracion": 3, "porcentaje": True}},
        {"nombre": "Maleficio Lento", "descripcion": "Reduce la velocidad del jugador.", "efecto": {"tipo": "debuff", "stat": "velocidad", "valor": 0.3, "duracion": 2, "porcentaje": True}},
        {"nombre": "Llama Maldita", "descripcion": "Inflige quemadura dolorosa con alta probabilidad.", "efecto": {"tipo": "negativo", "estado": "quemado", "valor": 6, "duracion": 3, "probabilidad": 0.9}},
        {"nombre": "Garra Sangrienta", "descripcion": "Ataque físico potenciado con daño elevado.", "efecto": {"tipo": "daño", "escala_ataque": 4.0, "valor": 80}},
        {"nombre": "Regeneración Oscura", "descripcion": "Cura parte de su salud máxima.", "efecto": {"tipo": "curacion", "escala_salud": 0.6, "valor": 150}},
        {"nombre": "Mordida Venenosa", "descripcion": "Ataque con posibilidad de envenenar.", "efecto": {"tipo": "negativo", "estado": "veneno", "valor": 5, "duracion": 3, "probabilidad": 0.75}},
    ]
    for h in habilidades:
        ActivaEnemigo.objects.create(nombre=h["nombre"], descripcion=h["descripcion"], efecto=h["efecto"])


def poblar_enemigos(apps, schema_editor):
    Enemigo = apps.get_model('battlebound_tactics', 'Enemigo')
    enemigos = [
        {"nombre": "Ares del Abismo", "descripcion": "Una imponente figura de músculos colosales y rostro cubierto por una sombra eterna. Se dice que Ares del Abismo fue creado en una forja maldita, alimentada por el odio de mil guerreros caídos. Su fuerza brutal solo es igualada por su silencio aterrador.", "salud_maxima": 42000, "salud": 42000, "ataque": 420, "defensa": 350, "velocidad": 115, "dificultad": "Difícil", "experiencia_otorgada": 25000, "oro_otorgado": 120, "nivel": 30, "imagen": "static/resources/Pixelarts/enemigos/enemigos_dificiles/enemigo_fuerte_1_nobg.png"},
        {"nombre": "Monje del Rencor", "descripcion": "Este viejo monje fue corrompido por la frustración y la traición. Su expresión amarga y su cuerpo encorvado ocultan un poder psíquico oscuro que utiliza para castigar a quienes perturban su soledad.", "salud_maxima": 1000, "salud": 1000, "ataque": 60, "defensa": 40, "velocidad": 85, "dificultad": "Fácil", "experiencia_otorgada": 500, "oro_otorgado": 12, "nivel": 5, "imagen": "static/resources/Pixelarts/enemigos/enemigos_faciles/enemigo_facil_2-1.png"},
        {"nombre": "Bestia de Cobalto", "descripcion": "Una criatura hecha aparentemente de piedra viva teñida de azul. La Bestia de Cobalto es ágil y feroz, con garras afiladas y ojos que brillan como fuego.", "salud_maxima": 1500, "salud": 1500, "ataque": 90, "defensa": 60, "velocidad": 88, "dificultad": "Fácil", "experiencia_otorgada": 800, "oro_otorgado": 14, "nivel": 6, "imagen": "static/resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-3.png"},
        {"nombre": "Bestia de Cobalto", "descripcion": "Una criatura hecha aparentemente de piedra viva teñida de azul. La Bestia de Cobalto es ágil y feroz, con garras afiladas y ojos que brillan como fuego.", "salud_maxima": 1800, "salud": 1800, "ataque": 100, "defensa": 65, "velocidad": 88, "dificultad": "Fácil", "experiencia_otorgada": 900, "oro_otorgado": 16, "nivel": 6, "imagen": "static/resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-6.png"},
        {"nombre": "Guardián del Bosque Sombrío", "descripcion": "Vestido con una antigua armadura de tonos tierra, este soldado sin rostro protege los secretos del bosque oscuro.", "salud_maxima": 14000, "salud": 14000, "ataque": 200, "defensa": 190, "velocidad": 75, "dificultad": "Media", "experiencia_otorgada": 10000, "oro_otorgado": 50, "nivel": 18, "imagen": "static/resources/Pixelarts/enemigos/enemigos_medios/enemigo_medio2.png"},
        {"nombre": "Bestia de Mármol", "descripcion": "Petrificada por una maldición olvidada, esta criatura parece una estatua que respira. Su piel de mármol es casi impenetrable.", "salud_maxima": 1700, "salud": 1700, "ataque": 75, "defensa": 130, "velocidad": 30, "dificultad": "Fácil", "experiencia_otorgada": 700, "oro_otorgado": 13, "nivel": 6, "imagen": "static/resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-5.png"},
        {"nombre": "Bestia de Ébano", "descripcion": "Forjada en la oscuridad total, la Bestia de Ébano es un cazador nocturno que se desliza entre sombras.", "salud_maxima": 1900, "salud": 1900, "ataque": 105, "defensa": 80, "velocidad": 105, "dificultad": "Fácil", "experiencia_otorgada": 950, "oro_otorgado": 18, "nivel": 7, "imagen": "static/resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-4.png"},
        {"nombre": "Bestia Carmesí", "descripcion": "Llameante como el mismo infierno, esta criatura ardiente parece alimentarse de ira.", "salud_maxima": 2000, "salud": 2000, "ataque": 115, "defensa": 70, "velocidad": 120, "dificultad": "Fácil", "experiencia_otorgada": 1000, "oro_otorgado": 20, "nivel": 7, "imagen": "static/resources/Pixelarts/enemigos/enemigos_faciles/sprite_enemigo_facil1-2.png"},
        {"nombre": "Duende Chillón", "descripcion": "Una criatura pequeña, escandalosa y sorprendentemente difícil de atrapar.", "salud_maxima": 800, "salud": 800, "ataque": 40, "defensa": 25, "velocidad": 140, "dificultad": "Fácil", "experiencia_otorgada": 400, "oro_otorgado": 10, "nivel": 3, "imagen": "static/resources/Pixelarts/enemigos/enemigos_faciles/enemigo_facil_3.png"},
        {"nombre": "Gran Jefe Duende y sus Réplicas", "descripcion": "El Gran Jefe Duende lidera con una mezcla de locura y fuerza desmedida.", "salud_maxima": 60000, "salud": 60000, "ataque": 500, "defensa": 250, "velocidad": 115, "dificultad": "Muy difícil", "experiencia_otorgada": 30000, "oro_otorgado": 200, "nivel": 35, "imagen": "static/resources/Pixelarts/enemigos/jefes/jefe_duende.png"},
        {"nombre": "Centurión del Crepúsculo", "descripcion": "Un guerrero legendario de una era olvidada, resucitado por magia antigua.", "salud_maxima": 35000, "salud": 35000, "ataque": 300, "defensa": 280, "velocidad": 100, "dificultad": "Difícil", "experiencia_otorgada": 20000, "oro_otorgado": 100, "nivel": 28, "imagen": "static/resources/Pixelarts/enemigos/enemigos_dificiles/enemigo_fuerte_2.png"}
    ]
    for enemigo in enemigos:
        Enemigo.objects.create(**enemigo)

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
