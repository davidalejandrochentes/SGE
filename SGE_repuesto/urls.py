from django.urls import path
from . import views

urlpatterns = [
    path('repuesto_maquina/', views.repuesto_maquina, name="repuesto_maquina"),
    path('eliminar_repuesto_maquina/<int:id>', views.eliminar_repuesto_maquina, name="eliminar_repuesto_maquina"),
    path('detalles_repuesto_maquina/<int:id>', views.detalles, name="detalles_repuesto_maquina"),
    path('actualizar_inventario/<int:id>/', views.actualizar_inventario, name='actualizar_inventario'),
    path('eliminar_inventario/<int:id>', views.eliminar_inventario, name="eliminar_inventario"),
]