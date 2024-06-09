from django.urls import path
from . import views

urlpatterns = [
    path('vehiculo/', views.vehiculo, name="vehiculo"),
    path('alertas/', views.alertas, name="vehiculo_alertas"),
    path('tabla/', views.tabla_mantenimientos, name="vehiculo_tabla_mantenimientos"),
    path('nueva/', views.crear_vehiculo, name="vehiculo_nueva"),
    path('detalles/<int:id>', views.detalles, name="detalles_vehiculo"),
    path('delete/<int:id>', views.eliminar, name="eliminar_vehiculo"),

    path('mantenimientos_vehiculo_preventivo/<int:id>', views.mantenimientos_vehiculo_preventivo, name="mantenimientos_vehiculo_preventivo"),
    path('mod_mantenimineto_vehiculo_preventivo/<int:id>', views.mod_mantenimineto_vehiculo_preventivo, name="mod_mantenimineto_vehiculo_preventivo"),
    path('nuevo_mantenimineto_vehiculo_preventivo/<int:id>', views.nuevo_mantenimineto_vehiculo_preventivo, name="nuevo_mantenimineto_vehiculo_preventivo"),

    path('mantenimientos_vehiculo_correctivo/<int:id>', views.mantenimientos_vehiculo_correctivo, name="mantenimientos_vehiculo_correctivo"),
    path('mod_mantenimineto_vehiculo_correctivo/<int:id>', views.mod_mantenimineto_vehiculo_correctivo, name="mod_mantenimineto_vehiculo_correctivo"),
    path('nuevo_mantenimineto_vehiculo_correctivo/<int:id>', views.nuevo_mantenimineto_vehiculo_correctivo, name="nuevo_mantenimineto_vehiculo_correctivo"),

    path('delete_mantenimiento/<int:id>', views.eliminar_mantenimiento, name="eliminar_mantenimiento_vehiculo"),
    
    path('documento_general_mantenimientos_vehiculo/', views.documento_general_mantenimientos_vehiculo, name='documento_general_mantenimientos_vehiculo'),
    path('documento_mantenimientos_preventivos_vehiculo/<int:id>/', views.documento_mantenimientos_preventivos_vehiculo, name='documento_mantenimientos_preventivos_vehiculo'),
    path('documento_mantenimientos_correctivos_vehiculo/<int:id>/', views.documento_mantenimientos_correctivos_vehiculo, name='documento_mantenimientos_correctivos_vehiculo'),
]
