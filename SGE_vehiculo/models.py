from django.db import models
from datetime import date
from datetime import datetime
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
import os


class Vehiculo(models.Model):
    marca = models.CharField(max_length=50, null=False, blank=False)
    modelo = models.CharField(max_length=50, null=False, blank=False)
    matricula = models.CharField(max_length=50, null=False, blank=False)
    número_de_chasis = models.CharField(max_length=50, null=False, blank=False)
    motor = models.CharField(max_length=50, null=False, blank=False)
    km_recorridos = models.IntegerField(blank=False, null=False)
    intervalo_mantenimiento = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to="vehiculo/image", null=False, blank=False)
    fecha_ultimo_mantenimiento = models.DateField(default=date.today, blank=False, null=False)

    nombre_chofer = models.CharField(max_length=50, null=False, blank=False)
    contraseña_chofer = models.CharField(max_length=20, blank=False, null=False)
    teléfono_chofer = models.CharField(max_length=10, blank=False, null=False)
    dirección_chofer = models.CharField(max_length=30, blank=False, null=False)
    dni_chofer = models.IntegerField(max_length=10, blank=False, null=False)
    
    def km_restantes_mantenimiento(self):
        km_restantes = self.intervalo_mantenimiento - (self.km_recorridos % self.intervalo_mantenimiento)
        return km_restantes
    
    def __str__(self):
        return self.modelo


class Viaje(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    origen = models.CharField(max_length=30, blank=False, null=False)
    destino = models.CharField(max_length=30, blank=False, null=False)
    fecha_salida = models.DateField(default=date.today)
    hora_salida = models.TimeField(default=datetime.now().time())
    kilometraje_de_salida = models.IntegerField(max_length=50, blank=False, null=False)
    imagen_de_salida = models.ImageField(upload_to="vehiculo/viaje/salida", null=False, blank=False)
    fecha_llegada = models.DateField(default=date.today)
    hora_llegada = models.TimeField(default=datetime.now().time())
    kilometraje_de_llegada = models.IntegerField(max_length=50, blank=False, null=False)
    imagen_de_llegada = models.ImageField(upload_to="vehiculo/viaje/llegada", null=False, blank=False)

    def __str__(self):
        return self.destino


class TipoMantenimientoVehiculo(models.Model):
    tipo = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.tipo


class MantenimientoVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMantenimientoVehiculo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=date.today)
    hora_inicio = models.TimeField(default=datetime.now().time()) 
    fecha_fin = models.DateField(default=date.today)
    hora_fin = models.TimeField(default=datetime.now().time())
    km_recorridos = models.IntegerField(blank=False, null=False)
    operador = models.CharField(max_length=100, blank=False, null=False)
    descripción = models.TextField(max_length=400, null=False, blank=False)
    partes_y_piezas = models.TextField(max_length=400, null=False, blank=False)
    image = models.ImageField(upload_to="vehiculo/mantenimiento", null=False, blank=False) 

    def __str__(self):
        txt = "Area: {}, Tipo: {}, Fecha: {}"
        return txt.format(self.area, self.tipo, self.fecha)  


@receiver(post_save, sender=MantenimientoVehiculo)
def actualizar_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    vehiculo = instance.vehiculo
    if instance.fecha_fin > vehiculo.fecha_ultimo_mantenimiento:
        vehiculo.fecha_ultimo_mantenimiento = instance.fecha_fin
        vehiculo.save()  

@receiver(pre_delete, sender=MantenimientoVehiculo)
def revertir_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    vehiculo = instance.vehiculo
    mantenimientos_restantes = MantenimientoVehiculo.objects.filter(vehiculo=vehiculo).exclude(id=instance.id).order_by('-fecha')
    if mantenimientos_restantes.exists():
        ultimo_mantenimiento = mantenimientos_restantes.first()
        vehiculo.fecha_ultimo_mantenimiento = ultimo_mantenimiento.fecha_fin
    else:
        vehiculo.fecha_ultimo_mantenimiento = vehiculo.fecha_ultimo_mantenimiento  # Otra opción si no hay mantenimientos restantes
    vehiculo.save()


@receiver(pre_delete, sender=Vehiculo)
def eliminar_imagen_de_vehiculo(sender, instance, **kwargs):
    # Verificar si Vehiculo tiene una imagen asociada y eliminarla
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Vehiculo)
def eliminar_imagen_anterior_al_actualizar(sender, instance, **kwargs):
    if not instance.pk:  # Vehiculo es nuevo, no hay imagen anterior que eliminar
        return False

    try:
        vehiculo_anterior = Vehiculo.objects.get(pk=instance.pk)  # Obtener Vehiculo anterior de la base de datos
    except Vehiculo.DoesNotExist:
        return False  # Vehiculo anterior no existe, no hay imagen anterior que eliminar

    if vehiculo_anterior.image:  # Verificar si Vehiculo anterior tiene una imagen
        nueva_imagen = instance.image
        if vehiculo_anterior.image != nueva_imagen:  # Verificar si se ha seleccionado una nueva imagen
            if os.path.isfile(vehiculo_anterior.image.path):  # Verificar si el archivo de imagen existe en el sistema de archivos
                os.remove(vehiculo_anterior.image.path)


#-----------------------------------------------------------------------------------------------------------------------------
@receiver(pre_delete, sender=MantenimientoVehiculo)
def eliminar_imagen_de_mantenimineto(sender, instance, **kwargs):
    # Verificar si Vehiculo tiene una imagen asociada y eliminarla
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=MantenimientoVehiculo)
def eliminar_imagen_anterior_al_actualizar_mantenimineto(sender, instance, **kwargs):
    if not instance.pk:  # Vehiculo es nuevo, no hay imagen anterior que eliminar
        return False

    try:
        mantenimineto_anterior = MantenimientoVehiculo.objects.get(pk=instance.pk)
    except MantenimientoVehiculo.DoesNotExist:
        return False

    if mantenimineto_anterior.image:
        nueva_imagen = instance.image
        if mantenimineto_anterior.image != nueva_imagen:  # Verificar si se ha seleccionado una nueva imagen
            if os.path.isfile(mantenimineto_anterior.image.path):  # Verificar si el archivo de imagen existe en el sistema de archivos
                os.remove(mantenimineto_anterior.image.path)                    