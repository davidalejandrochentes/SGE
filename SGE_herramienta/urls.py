from django.urls import path
from . import views

urlpatterns = [
    path('herramienta/', views.herramienta, name="herramienta"),
    path('alertas/', views.alertas, name="herramienta_alertas"),
]