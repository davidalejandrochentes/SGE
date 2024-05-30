from django.urls import path
from . import views

urlpatterns = [
    path('vehiculo/', views.vehiculo, name="vehiculo"),
    path('nuevo', views.crear_vehiculo, name="nuevo_vehiculo"),
    path('alertas/', views.alertas, name="maquina_alertas"),
    path('detalles/<int:id>', views.detalles, name="detalles_vehiculo"),
    path('delete/<int:id>', views.eliminar, name="eliminar_vehiculo"),
    path('delete_mantenimiento/<int:id>', views.eliminar_mantenimiento, name="eliminar_mantenimiento_vehiculo"),
]
