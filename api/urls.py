from django.urls import path, include
from rest_framework import routers
from api.views import JugadorViewSet, ApiRootViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'jugadores', JugadorViewSet)
router.register(r'', ApiRootViewSet, basename='api_root')



urlpatterns = [
    path('', include(router.urls)),
]