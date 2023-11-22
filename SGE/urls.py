from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"), 
    path('soporte/', views.soporte, name="soporte")
]