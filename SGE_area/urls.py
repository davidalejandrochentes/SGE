from django.urls import path
from . import views

urlpatterns = [
    path('area/', views.area, name="area"),
    path('alertas/', views.alertas, name="area_alertas"),
    path('tabla/', views.tabla_mantenimientos, name="area_tabla_mantenimientos"),
    path('nueva/', views.crear_area, name="area_nueva"),
    path('detalles/<int:id>', views.detalles, name="detalles_area"),
    path('delete/<int:id>', views.eliminar, name="eliminar_area"),
    path('delete_mantenimiento/<int:id>', views.eliminar_mantenimiento, name="eliminar_mantenimiento_area"),
    path('generar_documento_mantenimientos_por_mes/', views.generar_documento_mantenimientos_por_mes, name='generar_documento_mantenimientos_general_area'),
    path('generar_documento_mantenimientos_area/<int:id>/', views.generar_documento_mantenimientos_area, name='generar_documento_mantenimientos_area'),
]