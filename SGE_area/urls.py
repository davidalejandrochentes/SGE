from django.urls import path
from . import views

urlpatterns = [
    path('area/', views.area, name="area"),
    path('alertas/', views.alertas, name="area_alertas"),
    path('tabla_mantenimientos/', views.tabla_mantenimientos, name="area_tabla_mantenimientos"),
]