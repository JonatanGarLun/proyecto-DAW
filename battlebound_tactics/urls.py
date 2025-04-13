from django.urls import path
from battlebound_tactics.views import HomePageView, RegistroPageView

urlpatterns = [
    path('inicio/', HomePageView.as_view(), name='home'),
    path('registro/', RegistroPageView.as_view(), name='registro'),
]