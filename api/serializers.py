from battlebound_tactics.models import Jugador, Enemigo, Jefe, Combate

class JugadorSerializer:
    class Meta:
        model = Jugador
        fields = '__all__'

class EnemigoSerializer:
    class Meta:
        model = Enemigo
        fields = '__all__'

class JefeSerializer:
    class Meta:
        model = Jefe
        fields = '__all__'

class CombateSerializer:
    class Meta:
        model = Combate
        fields = '__all__'