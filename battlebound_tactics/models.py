from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# ------------------
# JUGADOR
# ------------------
class Jugador(models.Model):
    ALINEACIONES = [
        ('Aliado', 'Aliado'),
        ('Neutro', 'Neutro'),
        ('Enemigo', 'Enemigo'),
    ]

    CLASES = [
        ('Guerrero', 'Guerrero'),
        ('Mago', 'Mago'),
        ('Arquero', 'Arquero'),
        ('Luchador', 'Luchador'),
        ('Espiritualista', 'Espiritualista'),
        ('Astral', 'Astral'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    clase = models.CharField(max_length=50, choices=CLASES, default='Guerrero')
    nivel = models.IntegerField(default=1)
    experiencia = models.IntegerField(default=0)
    experiencia_maxima = models.IntegerField(default=1000)
    alineacion = models.CharField(max_length=10, choices=ALINEACIONES, default='Neutro')

    salud_maxima = models.IntegerField(default=100)
    salud = models.IntegerField(default=100)
    energia_espiritual_maxima = models.IntegerField(default=50)
    energia_espiritual = models.IntegerField(default=50)

    defensa = models.IntegerField(default=15)
    velocidad = models.IntegerField(default=10)
    ataque = models.IntegerField(default=20)

    arma = models.ForeignKey("Arma", on_delete=models.SET_NULL, null=True, blank=True)
    accesorio = models.ForeignKey("Accesorio", on_delete=models.SET_NULL, null=True, blank=True)
    habilidad_pasiva = models.ForeignKey("Pasiva", on_delete=models.SET_NULL, null=True, blank=True)
    habilidad_1 = models.ForeignKey("Activa", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="habilidad_1")
    habilidad_2 = models.ForeignKey("Activa", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="habilidad_2")
    habilidad_3 = models.ForeignKey("Activa", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="habilidad_3")
    oro = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.nombre}"

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"


# ------------------
# MOCHILA Y OBJETOS
# ------------------
class Objeto(models.Model):
    TIPO_OBJETO = [
        ("consumible", "Consumible"),
        ("material", "Material"),
        ("historia", "Historia"),
        ("coleccionable", "Coleccionable"),
        ("botin", "Botin"),

    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_OBJETO)
    precio = models.IntegerField(default=20)
    descripcion = models.TextField()
    efecto = models.JSONField(default=dict, blank=True, null=True)
    foto = models.ImageField(upload_to="resources/objetos/", null=True, blank=True)

    def __str__(self):
        return self.nombre


class Mochila(models.Model):
    jugador = models.OneToOneField(Jugador, on_delete=models.CASCADE, related_name="mochila")
    objetos = models.ManyToManyField(Objeto, through="ObjetoEnMochila")

    def __str__(self):
        return f"Mochila de {self.jugador.nombre}"


class ObjetoEnMochila(models.Model):
    mochila = models.ForeignKey(Mochila, on_delete=models.CASCADE)
    objeto = models.ForeignKey(Objeto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)


# ------------------
# EQUIPAMIENTO
# ------------------
class Arma(models.Model):
    nombre = models.CharField(max_length=100)
    ataque = models.IntegerField(default=0)
    defensa = models.IntegerField(default=0)
    velocidad = models.IntegerField(default=0)
    nivel_necesario = models.IntegerField(default=1)
    foto = models.ImageField(upload_to="resources/armas/", null=True, blank=True)

    def __str__(self):
        return self.nombre


class Accesorio(models.Model):
    nombre = models.CharField(max_length=100)
    salud = models.IntegerField(default=0)
    energia_espiritual = models.IntegerField(default=0)
    defensa = models.IntegerField(default=0)
    velocidad = models.IntegerField(default=0)
    ataque = models.IntegerField(default=0)
    nivel_necesario = models.IntegerField(default=1)
    foto = models.ImageField(upload_to="resources/accesorios/", null=True, blank=True)

    def __str__(self):
        return self.nombre


# ------------------
# HABILIDADES PASIVAS Y ACTIVAS
# ------------------
class Pasiva(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    efecto = models.JSONField(default=dict)

    def __str__(self):
        return self.nombre


class Activa(models.Model):
    nombre = models.CharField(max_length=100)
    coste_energia = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    coste_salud = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(0.99)
        ]
    )
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    efecto = models.JSONField(default=dict)
    nivel_necesario = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Habilidad: {self.nombre} - Nivel {self.nivel_necesario}"


class ActivaEnemigo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    efecto = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.nombre}"


class HabilidadAsignadaEnemigo(models.Model):
    enemigo = models.ForeignKey("Enemigo", on_delete=models.CASCADE, related_name="habilidades_asignadas")
    plantilla = models.ForeignKey("ActivaEnemigo", on_delete=models.CASCADE)
    cooldown_actual = models.IntegerField(default=0)

    def preparada(self):
        """Devuelve True si la habilidad está lista para usarse."""
        return self.cooldown_actual == 0

    def activar(self, cooldown=None):
        """Activa la habilidad, asignando cooldown desde el efecto o un parámetro explícito."""
        if cooldown is not None:
            self.cooldown_actual = cooldown
        else:
            self.cooldown_actual = self.plantilla.efecto.get("cooldown", 1)

    def enfriar(self):
        """Reduce el cooldown actual en 1 si es necesario."""
        if self.cooldown_actual > 0:
            self.cooldown_actual -= 1

    def usar(self, cooldown=None):
        self.activar(cooldown)
        self.save()

    def __str__(self):
        return f"{self.plantilla.nombre} (CD: {self.cooldown_actual}) para {self.enemigo.nombre}"


# ------------------
# HIDDEN POTENTIAL
# ------------------
#class HiddenPotentialNodeTemplate(models.Model):
#    nivel = models.IntegerField()
#descripcion = models.TextField()
#efecto = models.JSONField(default=dict)
#coste_monedas = models.IntegerField(default=0)
#coste_especiales = models.IntegerField(default=0)
#clase_objetivo = models.CharField(max_length=50)

#class HiddenPotential(models.Model):
#   jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="hidden_potential")
#nodo = models.ForeignKey(HiddenPotentialNodeTemplate, on_delete=models.CASCADE)
#desbloqueado = models.BooleanField(default=False)

#def __str__(self):
#    return f"{self.jugador.nombre} - Nivel {self.nodo.nivel}"

# ------------------
# EFECTOS DE ESTADO
# ------------------
# class Estado(models.Model):
#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()
#     efecto = models.JSONField(default=dict)
#
#     def __str__(self):
#         return self.nombre
#
# class EstadoActivo(models.Model):
#     jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="estados")
#     estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
#     turnos_restantes = models.IntegerField(default=1)
#
#     def __str__(self):
#         return f"{self.estado.nombre} en {self.jugador.nombre}"

# ------------------
# ENEMIGOS Y JEFES
# ------------------
class Enemigo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    salud_maxima = models.IntegerField(default=100)
    salud = models.IntegerField(default=100)
    ataque = models.IntegerField(default=10)
    defensa = models.IntegerField(default=10)
    velocidad = models.IntegerField(default=10)
    dificultad = models.CharField(max_length=50)
    experiencia_otorgada = models.IntegerField(default=0)
    oro_otorgado = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    recompensa_especial = models.JSONField(default=dict, blank=True, null=True)
    imagen = models.ImageField(null=True, blank=True)
    habilidad_1 = models.ForeignKey(ActivaEnemigo, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="enemigo_habilidad_1")
    habilidad_2 = models.ForeignKey(ActivaEnemigo, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="enemigo_habilidad_2")
    habilidad_3 = models.ForeignKey(ActivaEnemigo, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="enemigo_habilidad_3")

    def __str__(self):
        return f"{self.nombre} - Dificultad {self.dificultad}"


class Jefe(Enemigo):
    habilidades = models.JSONField(default=dict)
    es_jefe_final = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Jefe"
        verbose_name_plural = "Jefes"


# ------------------
# COMBATE Y TURNOS
# ------------------
class Combate(models.Model):
    nombre = models.CharField(max_length=100)
    registro = models.TextField(blank=True, null=True)
    turnos = models.IntegerField(default=0)
    jugador = models.ForeignKey(Jugador, related_name='Jugador', on_delete=models.CASCADE)
    enemigo = models.ForeignKey(Enemigo, related_name='Enemigo', on_delete=models.CASCADE)

# ------------------
# UBICACIONES
# ------------------

class Ubicacion(models.Model):
    TIPO_CHOICES = [
        ("combate", "Combate"),
        ("dialogo", "Diálogo"),
        ("plantilla", "Plantilla externa"),
    ]

    nombre = models.CharField(max_length=100)
    coordenadas = models.CharField(max_length=100, help_text="Formato: x1,y1,x2,y2")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    enemigo = models.ForeignKey(Enemigo, null=True, blank=True, on_delete=models.SET_NULL)
    plantilla_destino = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre de plantilla para tipo 'plantilla'")
    texto_dialogo = models.TextField(blank=True, null=True, help_text="Texto mostrado si el tipo es 'dialogo'")

    def __str__(self):
        return self.nombre