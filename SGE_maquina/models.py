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
    
    horas_máquina_trabajada = models.IntegerField(blank=False, null=False, default=0)
    intervalo_mantenimiento = models.IntegerField(blank=False, null=False)
    fecha_ultimo_mantenimiento = models.DateField(default=date.today, blank=False, null=False)
    image = models.ImageField(upload_to="maquina/image", null=False, blank=False)

    def horas_restantes_mantenimiento(self):
        ultimo_mantenimiento = MantenimientoMaquina.objects.filter(maquina=self).order_by('-fecha').first()
        if ultimo_mantenimiento:
            horas_uso_ultimo_mantenimiento = ultimo_mantenimiento.hr_maquina
        else:
            horas_uso_ultimo_mantenimiento = 0

        proximo_mantenimineto = horas_uso_ultimo_mantenimiento + self.intervalo_mantenimiento
        horas_restantes = proximo_mantenimineto - self.horas_máquina_trabajada
        return horas_restantes   
    
    
    def __str__(self):
        return self.nombre


class TipoMantenimientoMaquina(models.Model):
    tipo = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.tipo

class MantenimientoMaquina(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=date.today)
    hora_inicio = models.TimeField(default=datetime.now().time()) 
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now().time())
    operador = models.CharField(max_length=100, blank=False, null=False, default="")
    tipo = models.ForeignKey(TipoMantenimientoMaquina, on_delete=models.CASCADE)
    hr_maquina = models.IntegerField(blank=False, null=False, default=0)
    partes_y_piezas = models.TextField(max_length=500, null=False, blank=False, default="")
    descripción = models.TextField(max_length=500, null=False, blank=False, default="")
    image = models.ImageField(upload_to="maquina/mantenimiento/image", null=False, blank=False, default=None)  
    image2 = models.ImageField(upload_to="maquina/mantenimiento/image", null=True, blank=True, default=None)
    image3 = models.ImageField(upload_to="maquina/mantenimiento/image", null=True, blank=True, default=None)

    

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


#-----------------------------------------------------------------------------------------------------------------------------
@receiver(pre_delete, sender=MantenimientoMaquina)
def eliminar_imagen_de_mantenimineto(sender, instance, **kwargs):
    # Verificar si la máquina tiene una imagen asociada y eliminarla
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    if instance.image2:
        if os.path.isfile(instance.image2.path):
            os.remove(instance.image2.path)  
    if instance.image3:
        if os.path.isfile(instance.image3.path):
            os.remove(instance.image3.path)





@receiver(pre_save, sender=MantenimientoMaquina)
def eliminar_imagen_anterior_al_actualizar_mantenimineto(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        mantenimiento_anterior = MantenimientoMaquina.objects.get(pk=instance.pk)
    except MantenimientoMaquina.DoesNotExist:
        return False

    # Comparar y eliminar image
    if mantenimiento_anterior.image and instance.image != mantenimiento_anterior.image:
        if os.path.isfile(mantenimiento_anterior.image.path):
            os.remove(mantenimiento_anterior.image.path)
    
    # Comparar y eliminar image2
    if mantenimiento_anterior.image2 and instance.image2 != mantenimiento_anterior.image2:
        if os.path.isfile(mantenimiento_anterior.image2.path):
            os.remove(mantenimiento_anterior.image2.path)
    
    # Comparar y eliminar image3
    if mantenimiento_anterior.image3 and instance.image3 != mantenimiento_anterior.image3:
        if os.path.isfile(mantenimiento_anterior.image3.path):
            os.remove(mantenimiento_anterior.image3.path)