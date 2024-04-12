from django.urls import path
from . import views

urlpatterns = [
    path('repuesto/', views.repuesto, name="repuesto"),
]