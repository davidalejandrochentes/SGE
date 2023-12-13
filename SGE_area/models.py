from django.db import models
from datetime import date
from datetime import datetime
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

    
class Area(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    tamaño = models.CharField(max_length=100, blank=False, null=False)
    encargado = models.CharField(max_length=100, blank=False, null=False)
    teléfono_encargado = models.CharField(max_length=100, blank=False, null=False)
    descripción = models.TextField(max_length=500, null=True, blank=True)
    ubicación = models.CharField(max_length=100, null=True, blank=True)
    capacidad = models.CharField(max_length=100, null=True, blank=True)
    tipo_de_área = models.CharField(max_length=100, null=True, blank=True)
    estado_de_ocupación = models.CharField(max_length=100, null=True, blank=True)
    fecha_ultimo_mantenimiento = models.DateField(default=date.today, blank=False, null=False)
    intervalo_mantenimiento = models.IntegerField(default=30, blank=False, null=False)

    def dias_restantes_mantenimiento(self):
        dias_pasados = (date.today() - self.fecha_ultimo_mantenimiento).days
        dias_restantes = self.intervalo_mantenimiento - dias_pasados
        return dias_restantes 
    
    def __str__(self):
        return self.nombre

class TipoMantenimientoArea(models.Model):
    tipo = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.tipo

class MantenimientoArea(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMantenimientoArea, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now().time)   

    def __str__(self):
        txt = "Area: {}, Tipo: {}, Fecha: {}"
        return txt.format(self.area, self.tipo, self.fecha)
    

@receiver(post_save, sender=MantenimientoArea)
def actualizar_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    area = instance.area
    if instance.fecha > area.fecha_ultimo_mantenimiento:
        area.fecha_ultimo_mantenimiento = instance.fecha
        area.save()   

@receiver(pre_delete, sender=MantenimientoArea)
def revertir_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    area = instance.area
    mantenimientos_restantes = MantenimientoArea.objects.filter(area=area).exclude(id=instance.id).order_by('-fecha')
    if mantenimientos_restantes.exists():
        ultimo_mantenimiento = mantenimientos_restantes.first()
        area.fecha_ultimo_mantenimiento = ultimo_mantenimiento.fecha
    else:
        area.fecha_ultimo_mantenimiento = None  # Otra opción si no hay mantenimientos restantes
    area.save()

