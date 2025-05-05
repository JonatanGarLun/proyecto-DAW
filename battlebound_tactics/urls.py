from django.urls import path
from battlebound_tactics.views import RegistroPageView, InicioPageView, AventuraPageView

urlpatterns = [
    path('inicio/', InicioPageView.as_view(), name='inicio'),
    path('aventura/', AventuraPageView.as_view(), name='inicio'),
    path('registro/', RegistroPageView.as_view(), name='registro'),
]