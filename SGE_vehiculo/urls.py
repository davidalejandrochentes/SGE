from django.urls import path
from . import views

urlpatterns = [
    path('vehiculo/', views.vehiculo, name="vehiculo"),
    path('nuevo', views.crear_vehiculo, name="nuevo_vehiculo")
]
