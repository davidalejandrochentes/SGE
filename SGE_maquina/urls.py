from django.urls import path
from . import views

urlpatterns = [
    path('maquina/', views.maquina, name="maquina"),
    path('alertas/', views.alertas, name="maquina_alertas"),
    path('tabla/', views.tabla_mantenimientos, name="maquina_tabla_mantenimientos"),
    path('nueva/', views.crear_maquina, name="maquina_nueva"),
    path('detalles/<int:id>', views.detalles, name="detalles_maquina"),
    path('delete/<int:id>', views.eliminar, name="eliminar_maquina"),
    path('delete_mantenimiento/<int:id>', views.eliminar_mantenimiento, name="eliminar_mantenimiento_maquina"),
    path('generar_documento_mantenimientos_por_mes/', views.generar_documento_mantenimientos_por_mes, name='generar_documento_mantenimientos_general_maquina'),
    path('generar_documento_mantenimientos_maquina/<int:id>/', views.generar_documento_mantenimientos_maquina, name='generar_documento_mantenimientos_maquina'),

]
