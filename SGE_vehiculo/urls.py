from django.urls import path
from . import views

urlpatterns = [
    path('vehiculo/', views.vehiculo, name="vehiculo"),
    path('nuevo', views.crear_vehiculo, name="nuevo_vehiculo"),
    path('alertas/', views.alertas, name="maquina_alertas"),
]
