from django.urls import path
from . import views

urlpatterns = [
    path('area/', views.area, name="area"),
    path('alertas/', views.alertas, name="area_alertas"),
    path('tabla/', views.tabla_mantenimientos, name="area_tabla_mantenimientos"),
    path('nueva/', views.crear_area, name="area_nueva"),
    path('detalles/<int:id>', views.detalles, name="detalles_area")
]