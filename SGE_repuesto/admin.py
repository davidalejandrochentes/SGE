from django.contrib import admin
from .models import Maquina, Partes, Inventario


admin.site.register(Maquina)
admin.site.register(Partes)
admin.site.register(Inventario)
