from django.urls import path
from . import views

urlpatterns = [
    path('pc/', views.pc, name="pc"),
]