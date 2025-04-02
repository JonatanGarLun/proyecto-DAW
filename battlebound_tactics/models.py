from django.db import models
from datetime import timedelta
from django.utils.timezone import now

# -------------------- Jugador --------------------
class Jugador(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    nivel = models.IntegerField(default=1)
    experiencia_actual = models.IntegerField(default=0)
    experiencia_necesaria = models.IntegerField(default=1000)

    salud_maxima = models.IntegerField(default=100)
    salud = models.IntegerField(default=100)
    energia_espiritual_maxima = models.IntegerField(default=100)
    energia_espiritual = models.IntegerField(default=100)

    defensa = models.IntegerField(default=10)
    velocidad = models.IntegerField(default=10)
    ataque = models.IntegerField(default=10)

    # Estas estadísticas no escalan con el nivel
    chance_adicional = models.FloatField(default=0.0)
    chance_critico = models.FloatField(default=0.0)
    chance_esquivar = models.FloatField(default=0.0)
    medidor_definitiva = models.FloatField(default=0.0)
    habilidad_pasiva = models.CharField(max_length=200, blank=True, null=True)

    oro = models.IntegerField(default=0)
    monedas_especiales = models.IntegerField(default=0)
    reputacion = models.IntegerField(default=0)

    clase = models.CharField(max_length=100, default="Guerrero")  # Para la habilidad final
    arma = models.ForeignKey('Arma', on_delete=models.SET_NULL, null=True, blank=True)
    accesorio = models.ForeignKey('Accesorio', on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to="jugadores/", blank=True, null=True)

    def __str__(self):
        return self.nombre


# -------------------- Equipamiento --------------------
class Arma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ataque = models.IntegerField(default=0)
    defensa = models.IntegerField(default=0)
    velocidad = models.IntegerField(default=0)
    foto = models.ImageField(upload_to="armas/", blank=True, null=True)

    def __str__(self):
        return self.nombre

class Accesorio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    salud = models.IntegerField(default=0)
    energia_espiritual = models.IntegerField(default=0)
    chance_adicional = models.FloatField(default=0.0)
    chance_critico = models.FloatField(default=0.0)
    chance_esquivar = models.FloatField(default=0.0)
    defensa = models.IntegerField(default=0)
    velocidad = models.IntegerField(default=0)
    ataque = models.IntegerField(default=0)
    foto = models.ImageField(upload_to="accesorios/", blank=True, null=True)

    def __str__(self):
        return self.nombre


# -------------------- Objetos y Mochila --------------------
class Objeto(models.Model):
    TIPO_OBJETO = [
        ('consumible', 'Consumible'),
        ('material', 'Material'),
        ('equipable', 'Equipable'),
        ('misión', 'Misión'),
    ]
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_OBJETO, default='consumible')
    descripcion = models.TextField(blank=True, null=True)
    efecto = models.JSONField(default=dict, blank=True, null=True)
    foto = models.ImageField(upload_to="objetos/", blank=True, null=True)

    def __str__(self):
        return self.nombre

class MochilaObjeto(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="mochila")
    objeto = models.ForeignKey(Objeto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    class Meta:
        unique_together = ('jugador', 'objeto')


# -------------------- Combate --------------------
class Combate(models.Model):
    nombre = models.CharField(max_length=100)
    luchador_1 = models.ForeignKey(Jugador, related_name="combates_1", on_delete=models.CASCADE)
    luchador_2 = models.ForeignKey(Jugador, related_name="combates_2", on_delete=models.CASCADE)
    registro = models.TextField(blank=True, null=True)
    turnos = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    combate = models.ForeignKey(Combate, on_delete=models.CASCADE, related_name="turnos")
    numero = models.IntegerField()
    acciones = models.TextField()

    def __str__(self):
        return f"Turno {self.numero} - {self.combate.nombre}"


# -------------------- Tienda --------------------
class Tienda(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    objetos_disponibles = models.ManyToManyField(Objeto, blank=True)

    def __str__(self):
        return self.nombre


# -------------------- Misiones y Trabajos --------------------
class Mision(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    recompensa = models.JSONField()  # Ej: {"oro": 1000, "objeto": "Espada"}
    nivel_requerido = models.IntegerField()

    def __str__(self):
        return self.nombre

class Trabajo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    recompensa = models.IntegerField()
    minijuego = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


# -------------------- Recompensa Diaria --------------------
class RecompensaDiaria(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    ultima_reclamacion = models.DateTimeField(auto_now=True)

    def puede_reclamar(self):
        return now() - self.ultima_reclamacion >= timedelta(days=1)


# -------------------- Hidden Potential --------------------
class HiddenPotentialNode(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="hidden_potential")
    nivel = models.IntegerField()
    efecto = models.CharField(max_length=255)
    costo_oro = models.IntegerField()
    costo_monedas_especiales = models.IntegerField(default=0)
    desbloqueado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('jugador', 'nivel')

    def desbloquear(self):
        if not self.desbloqueado and self.jugador.oro >= self.costo_oro and self.jugador.monedas_especiales >= self.costo_monedas_especiales:
            self.jugador.oro -= self.costo_oro
            self.jugador.monedas_especiales -= self.costo_monedas_especiales
            self.jugador.save()
            self.desbloqueado = True
            self.save()
            return f"Nivel {self.nivel} desbloqueado: {self.efecto}"
        return "No puedes desbloquear este nodo."

    def __str__(self):
        return f"Nivel {self.nivel} - {self.efecto}"
