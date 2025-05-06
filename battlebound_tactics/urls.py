from django.urls import path
from battlebound_tactics.views import RegistroPageView, InicioPageView, EstadisticasPageView

urlpatterns = [
    path('inicio/', InicioPageView.as_view(), name='inicio'),
    path('aventura/', EstadisticasPageView.as_view(), name='inicio'),
    path('registro/', RegistroPageView.as_view(), name='registro'),
]