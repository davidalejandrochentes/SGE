from django.urls import path
from . import views

urlpatterns = [
    path('vehiculo/', views.vehiculo, name="vehiculo"),
    path('nuevo', views.crear_vehiculo, name="nuevo_vehiculo"),
    path('alertas/', views.alertas, name="vehiculo_alertas"),
    path('detalles/<int:id>', views.detalles, name="detalles_vehiculo"),
    path('delete/<int:id>', views.eliminar, name="eliminar_vehiculo"),
    path('delete_mantenimiento/<int:id>', views.eliminar_mantenimiento, name="eliminar_mantenimiento_vehiculo"),
    path('mod_mantenimineto_vehiculo/<int:id>', views.mod_mantenimineto_vehiculo, name="mod_mantenimineto_vehiculo"),
    path('tabla/', views.tabla_mantenimientos, name="vehiculo_tabla_mantenimientos"),
    path('generar_documento_mantenimientos_por_mes/', views.generar_documento_mantenimientos_por_mes, name='generar_documento_mantenimientos_general_vehiculo'),
    #path('generar_documento_mantenimientos_vehiculo/<int:id>/', views.generar_documento_mantenimientos_vehiculo, name='generar_documento_mantenimientos_vehiculo'),
    path('registro_de_viajes/<int:id>', views.registro_de_viajes, name="registro_de_viajes")
]
