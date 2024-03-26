from django.urls import path
from . import views

urlpatterns = [
    path('herramienta/', views.herramienta, name="herramienta"),
    path('alertas/', views.alertas, name="herramienta_alertas"),
    path('tabla/', views.tabla_mantenimientos, name="herramienta_tabla_mantenimientos"),
    path('nueva/', views.crear_herramienta, name="herramienta_nueva"),
    path('detalles/<int:id>', views.detalles, name="detalles_herramienta"),
    path('delete/<int:id>', views.eliminar, name="eliminar_herramienta"),
    path('delete_mantenimiento/<int:id>', views.eliminar_mantenimiento, name="eliminar_mantenimiento_herramienta"),
]