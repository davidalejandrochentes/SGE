from django.db import models
from datetime import date
from datetime import datetime
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
import os

    
class PC(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    modelo = models.CharField(max_length=100, null=False, blank=False)
    número_de_inventario = models.CharField(max_length=100, blank=False, null=False)
    encargado = models.CharField(max_length=100, blank=False, null=False)
    teléfono_encargado = models.CharField(max_length=100, blank=False, null=False)
    descripción = models.TextField(max_length=500, null=False, blank=False)
    ubicación = models.CharField(max_length=100, null=False, blank=False)
    costo_de_adquisición = models.IntegerField(blank=False, null=False)
    fecha_de_adquisición = models.DateField(default=date.today, blank=False, null=False)
    fecha_de_retirada = models.DateField(default=date.today, blank=False, null=False)
    estado = models.CharField(max_length=100, null=False, blank=False)
    garantía = models.CharField(max_length=100, null=False, blank=False)
    software_instalado = models.CharField(max_length=100, null=False, blank=False)
    fecha_ultimo_mantenimiento = models.DateField(default=date.today, blank=False, null=False)
    intervalo_mantenimiento = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to="pc/image", null=False, blank=False)

    def dias_restantes_mantenimiento(self):
        dias_pasados = (date.today() - self.fecha_ultimo_mantenimiento).days
        dias_restantes = self.intervalo_mantenimiento - dias_pasados
        return dias_restantes 
    
    def __str__(self):
        return self.nombre

class TipoMantenimientoPC(models.Model):
    tipo = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.tipo

class MantenimientoPC(models.Model):
    pc = models.ForeignKey(PC, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMantenimientoPC, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now().time())   

    def __str__(self):
        txt = "Equipo: {}, Tipo: {}, Fecha: {}"
        return txt.format(self.pc, self.tipo, self.fecha)
    

@receiver(post_save, sender=MantenimientoPC)
def actualizar_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    pc = instance.pc
    if instance.fecha > pc.fecha_ultimo_mantenimiento:
        pc.fecha_ultimo_mantenimiento = instance.fecha
        pc.save()   

@receiver(pre_delete, sender=MantenimientoPC)
def revertir_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    pc = instance.pc
    mantenimientos_restantes = MantenimientoPC.objects.filter(pc=pc).exclude(id=instance.id).order_by('-fecha')
    if mantenimientos_restantes.exists():
        ultimo_mantenimiento = mantenimientos_restantes.first()
        pc.fecha_ultimo_mantenimiento = ultimo_mantenimiento.fecha
    else:
        pc.fecha_ultimo_mantenimiento = pc.fecha_ultimo_mantenimiento  # Otra opción si no hay mantenimientos restantes
    pc.save()

@receiver(pre_delete, sender=PC)
def eliminar_imagen_de_pc(sender, instance, **kwargs):
    # Verificar si el área tiene una imagen asociada y eliminarla
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=PC)
def eliminar_imagen_anterior_al_actualizar(sender, instance, **kwargs):
    if not instance.pk:  # El área es nueva, no hay imagen anterior que eliminar
        return False

    try:
        pc_anterior = PC.objects.get(pk=instance.pk)  # Obtener el área anterior de la base de datos
    except PC.DoesNotExist:
        return False  # El área anterior no existe, no hay imagen anterior que eliminar

    if pc_anterior.image:  # Verificar si el área anterior tiene una imagen
        nueva_imagen = instance.image
        if pc_anterior.image != nueva_imagen:  # Verificar si se ha seleccionado una nueva imagen
            if os.path.isfile(pc_anterior.image.path):  # Verificar si el archivo de imagen existe en el sistema de archivos
                os.remove(pc_anterior.image.path)
