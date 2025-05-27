from django.urls import path
from battlebound_tactics import views
from battlebound_tactics.views import RegistroPageView, InicioPageView, EstadisticasPageView, MapaContinentePageView, \
    RegionPageView, CastlevyrPageView

urlpatterns = [
    path('inicio/', InicioPageView.as_view(), name='inicio'),
    path('aventura/', EstadisticasPageView.as_view(), name='estadisticas'),
    path('registro/', RegistroPageView.as_view(), name='registro'),
    path('mapa/', MapaContinentePageView.as_view(), name='continente'),
    path('mapa/region-tranquila', RegionPageView.as_view(), name='region'),
    path('mapa/region-tranquila/castlevyr', CastlevyrPageView.as_view(), name='castlevyr'),
    path("iniciar-combate/<int:enemigo_id>/", views.iniciar_combate, name="iniciar_combate"),
    path('combate/<int:combate_id>/', views.combate, name='combate'),
    path('resultado/<int:combate_id>/', views.resultado_combate, name='resultado_combate'),
    path('posada/', views.posada, name='posada'),
    #    path("verificar_abandono/", views.verificar_abandono, name="verificar_abandono"),
    #    path("resolver_abandono/", views.resolver_abandono, name="resolver_abandono"),
    #    path("abandonar_combate/<int:combate_id>/", views.abandonar_combate, name="abandonar_combate"),
]
