from django.db import models
from datetime import date
from datetime import datetime
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
import os

    
class Maquina(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    encargado = models.CharField(max_length=100, blank=False, null=False)
    teléfono_encargado = models.CharField(max_length=100, blank=False, null=False)
    descripción = models.TextField(max_length=500, null=False, blank=False)
    ubicación = models.CharField(max_length=100, null=False, blank=False)
    tipo_de_máquina = models.CharField(max_length=100, null=False, blank=False)
    número_de_serie_o_modelo = models.CharField(max_length=100, null=False, blank=False)
    proveedor = models.CharField(max_length=100, null=False, blank=False)
    costo_de_adquisición = models.IntegerField(blank=False, null=False)
    fecha_de_adquisición = models.DateField(default=date.today, blank=False, null=False)
    fecha_de_instalación = models.DateField(default=date.today, blank=False, null=False)
    estado_de_garantía = models.CharField(max_length=100, null=False, blank=False)
    consumo_de_energía = models.CharField(max_length=100, null=False, blank=False)

    fecha_ultimo_mantenimiento = models.DateField(default=date.today, blank=False, null=False)
    intervalo_mantenimiento = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to="maquina/image", null=False, blank=False)

    def dias_restantes_mantenimiento(self):
        dias_pasados = (date.today() - self.fecha_ultimo_mantenimiento).days
        dias_restantes = self.intervalo_mantenimiento - dias_pasados
        return dias_restantes 
    
    def __str__(self):
        return self.nombre


class TipoMantenimientoMaquina(models.Model):
    tipo = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.tipo

class MantenimientoMaquina(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMantenimientoMaquina, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=date.today)
    hora_inicio = models.TimeField(default=datetime.now().time()) 
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now().time())
    partes_y_piezas = models.TextField(max_length=500, null=False, blank=False)
    image = models.ImageField(upload_to="maquina/mantenimiento/image", null=False, blank=False)  
    descripción = models.TextField(max_length=500, null=False, blank=False)

    def __str__(self):
        txt = "Maquina: {}, Tipo: {}, Fecha: {}"
        return txt.format(self.maquina, self.tipo, self.fecha)
    

@receiver(post_save, sender=MantenimientoMaquina)
def actualizar_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    maquina = instance.maquina
    if instance.fecha > maquina.fecha_ultimo_mantenimiento:
        maquina.fecha_ultimo_mantenimiento = instance.fecha
        maquina.save()   

@receiver(pre_delete, sender=MantenimientoMaquina)
def revertir_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    maquina = instance.maquina
    mantenimientos_restantes = MantenimientoMaquina.objects.filter(maquina=maquina).exclude(id=instance.id).order_by('-fecha')
    if mantenimientos_restantes.exists():
        ultimo_mantenimiento = mantenimientos_restantes.first()
        maquina.fecha_ultimo_mantenimiento = ultimo_mantenimiento.fecha
    else:
        maquina.fecha_ultimo_mantenimiento = maquina.fecha_ultimo_mantenimiento  # Otra opción si no hay mantenimientos restantes
    maquina.save()

@receiver(pre_delete, sender=Maquina)
def eliminar_imagen_de_maquina(sender, instance, **kwargs):
    # Verificar si la máquina tiene una imagen asociada y eliminarla
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Maquina)
def eliminar_imagen_anterior_al_actualizar(sender, instance, **kwargs):
    if not instance.pk:  # La máquina es nueva, no hay imagen anterior que eliminar
        return False

    try:
        maquina_anterior = Maquina.objects.get(pk=instance.pk)  # Obtener la máquina anterior de la base de datos
    except Maquina.DoesNotExist:
        return False  # La máquina anterior no existe, no hay imagen anterior que eliminar

    if maquina_anterior.image:  # Verificar si la máquina anterior tiene una imagen
        nueva_imagen = instance.image
        if maquina_anterior.image != nueva_imagen:  # Verificar si se ha seleccionado una nueva imagen
            if os.path.isfile(maquina_anterior.image.path):  # Verificar si el archivo de imagen existe en el sistema de archivos
                os.remove(maquina_anterior.image.path)