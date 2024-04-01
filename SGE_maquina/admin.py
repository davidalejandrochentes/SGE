from django.contrib import admin
from .models import Maquina, TipoMantenimientoMaquina, MantenimientoMaquina, Componente, TipoMantenimientoComponente, MantenimientoComponente


admin.site.register(TipoMantenimientoMaquina)
admin.site.register(MantenimientoMaquina)
admin.site.register(TipoMantenimientoComponente)
admin.site.register(MantenimientoComponente)

class MaquinaAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Verifica si el objeto ya existe (es decir, si se está editando y no creando uno nuevo)
            return ['fecha_ultimo_mantenimiento']
        else:
            return []

admin.site.register(Maquina, MaquinaAdmin)

class ComponenteAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Verifica si el objeto ya existe (es decir, si se está editando y no creando uno nuevo)
            return ['fecha_ultimo_mantenimiento']
        else:
            return []

admin.site.register(Componente, ComponenteAdmin)
