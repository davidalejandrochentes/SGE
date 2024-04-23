from django.urls import path
from . import views

urlpatterns = [
    path('pc/', views.pc, name="pc"),
    path('alertas/', views.alertas, name="pc_alertas"),
    path('tabla/', views.tabla_mantenimientos, name="pc_tabla_mantenimientos"),
    path('nueva/', views.crear_pc, name="pc_nueva"),
    path('detalles/<int:id>', views.detalles, name="detalles_pc"),
    path('mod_mantenimiento_pc/<int:id>', views.mod_mantenimiento_pc, name="mod_mantenimiento_pc"),
    path('delete/<int:id>', views.eliminar, name="eliminar_pc"),
    path('delete_mantenimiento/<int:id>', views.eliminar_mantenimiento, name="eliminar_mantenimiento_pc"),
    path('generar_documento_mantenimientos_por_mes/', views.generar_documento_mantenimientos_por_mes, name='generar_documento_mantenimientos_general_pc'),
    path('generar_documento_mantenimientos_pc/<int:id>/', views.generar_documento_mantenimientos_pc, name='generar_documento_mantenimientos_pc'),
]
