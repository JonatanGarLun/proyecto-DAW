from django.urls import path
from battlebound_tactics import views
from battlebound_tactics.views import RegistroPageView, InicioPageView, EstadisticasPageView, MapaContinentePageView

urlpatterns = [
    path('inicio/', InicioPageView.as_view(), name='inicio'),
    path('aventura/', EstadisticasPageView.as_view(), name='estadisticas'),
    path('registro/', RegistroPageView.as_view(), name='registro'),
    path('mapa/', MapaContinentePageView.as_view(), name='continente'),

    # path('mapa/<str:ubicacion_nombre>', MapaContinentePageView.as_view(), name='registro'),
    path('combate/', views.combate, name='combate'),
]