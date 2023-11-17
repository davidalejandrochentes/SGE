from django.urls import path
from . import views

urlpatterns = [
    path('area/', views.area, name="area")
]