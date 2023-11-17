from django.contrib import admin
from .models import Area, TipoMantenimientoArea, MantenimientoArea

# Register your models here.
admin.site.register(Area)
admin.site.register(TipoMantenimientoArea)
admin.site.register(MantenimientoArea)
