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
    km_recorridos = models.BigIntegerField(blank=False, null=False)
    intervalo_mantenimiento = models.IntegerField(blank=False, null=False)

    intervalo_mantenimiento_cambio_filtro_aceite = models.IntegerField(blank=False, null=False)
    intervalo_mantenimiento_cambio_filtro_aire_combustible = models.IntegerField(blank=False, null=False)
    intervalo_mantenimiento_cambio_filtro_caja_corona = models.IntegerField(blank=False, null=False)

    image = models.ImageField(upload_to="vehiculo/image", null=False, blank=False)
    fecha_ultimo_mantenimiento = models.DateField(default=date.today, blank=False, null=False)

    nombre_chofer = models.CharField(max_length=50, null=False, blank=False)
    nombre_usuario_chofer = models.CharField(max_length=20, null=False, blank=False, default="")
    contraseña_chofer = models.CharField(max_length=20, blank=False, null=False)
    teléfono_chofer = models.CharField(max_length=10, blank=False, null=False)
    dirección_chofer = models.CharField(max_length=30, blank=False, null=False)
    dni_chofer = models.BigIntegerField(max_length=20, blank=False, null=False)


    def km_restantes_mantenimiento_correctivo(self):
        ultimo_mantenimiento = MantenimientoVehiculo.objects.filter(vehiculo=self, tipo__id=1).order_by('-fecha_fin').first()
        if ultimo_mantenimiento:
            km_recorridos_ultimo_mantenimiento = ultimo_mantenimiento.km_recorridos
        else:
            km_recorridos_ultimo_mantenimiento = 0

        proximo_mantenimineto = km_recorridos_ultimo_mantenimiento + self.intervalo_mantenimiento
        km_restantes = proximo_mantenimineto - self.km_recorridos
        return km_restantes


    def km_restantes_cambio_de_filtro_aceite(self):
        ultimo_mantenimiento = MantenimientoVehiculo.objects.filter(vehiculo=self, tipo__id=3).order_by('-fecha_fin').first()
        if ultimo_mantenimiento:
            km_recorridos_ultimo_mantenimiento = ultimo_mantenimiento.km_recorridos
        else:
            km_recorridos_ultimo_mantenimiento = 0

        proximo_mantenimineto = km_recorridos_ultimo_mantenimiento + self.intervalo_mantenimiento_cambio_filtro_aceite
        km_restantes = proximo_mantenimineto - self.km_recorridos
        return km_restantes


    def km_restantes_cambio_filtro_aire_combustible(self):
        ultimo_mantenimiento = MantenimientoVehiculo.objects.filter(vehiculo=self, tipo__id=4).order_by('-fecha_fin').first()
        if ultimo_mantenimiento:
            km_recorridos_ultimo_mantenimiento = ultimo_mantenimiento.km_recorridos
        else:
            km_recorridos_ultimo_mantenimiento = 0

        proximo_mantenimineto = km_recorridos_ultimo_mantenimiento + self.intervalo_mantenimiento_cambio_filtro_aire_combustible
        km_restantes = proximo_mantenimineto - self.km_recorridos
        return km_restantes


    def km_restantes_cambio_filtro_caja_corona(self):
        ultimo_mantenimiento = MantenimientoVehiculo.objects.filter(vehiculo=self, tipo__id=5).order_by('-fecha_fin').first()
        if ultimo_mantenimiento:
            km_recorridos_ultimo_mantenimiento = ultimo_mantenimiento.km_recorridos
        else:
            km_recorridos_ultimo_mantenimiento = 0

        proximo_mantenimineto = km_recorridos_ultimo_mantenimiento + self.intervalo_mantenimiento_cambio_filtro_caja_corona
        km_restantes = proximo_mantenimineto - self.km_recorridos
        return km_restantes

    def __str__(self):
        return self.modelo




class Viaje(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    origen = models.CharField(max_length=30, blank=False, null=False)
    destino = models.CharField(max_length=30, blank=False, null=False)
    fecha_salida = models.DateField(default=date.today)
    hora_salida = models.TimeField(default=datetime.now().time())
    kilometraje_de_salida = models.BigIntegerField(max_length=50, blank=False, null=False)
    imagen_de_salida = models.ImageField(upload_to="vehiculo/viaje/salida", null=False, blank=False)
    fecha_llegada = models.DateField(default=date.today)
    hora_llegada = models.TimeField(default=datetime.now().time())
    kilometraje_de_llegada = models.BigIntegerField(max_length=50, blank=False, null=False)
    imagen_de_llegada = models.ImageField(upload_to="vehiculo/viaje/llegada", null=False, blank=False)


    def __str__(self):
        txt = "Vehiculo: {}, Origen: {}, Destino: {}"
        return txt.format(self.vehiculo, self.origen, self.destino)




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
    km_recorridos = models.BigIntegerField(blank=False, null=False)
    operador = models.CharField(max_length=100, blank=False, null=False)
    descripción = models.TextField(max_length=400, null=False, blank=False)
    partes_y_piezas = models.TextField(max_length=400, null=False, blank=False)
    image = models.ImageField(upload_to="vehiculo/mantenimiento/image", null=False, blank=False, default=None)
    image2 = models.ImageField(upload_to="vehiculo/mantenimiento/image", null=False, blank=False, default=None)
    image3 = models.ImageField(upload_to="vehiculo/mantenimiento/image", null=False, blank=False, default=None)

    def __str__(self):
        txt = "Vehiculo: {}, Tipo: {}, Fecha: {}"
        return txt.format(self.vehiculo, self.tipo, self.fecha_fin)



#----------signals------------------------------------------------------------------------------

@receiver(post_save, sender=MantenimientoVehiculo)
def actualizar_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    vehiculo = instance.vehiculo
    if instance.fecha_fin > vehiculo.fecha_ultimo_mantenimiento:
        vehiculo.fecha_ultimo_mantenimiento = instance.fecha_fin
        vehiculo.save()




@receiver(pre_delete, sender=MantenimientoVehiculo)
def revertir_fecha_ultimo_mantenimiento(sender, instance, **kwargs):
    vehiculo = instance.vehiculo
    mantenimientos_restantes = MantenimientoVehiculo.objects.filter(vehiculo=vehiculo).exclude(id=instance.id).order_by('-fecha_fin')
    if mantenimientos_restantes.exists():
        ultimo_mantenimiento = mantenimientos_restantes.first()
        vehiculo.fecha_ultimo_mantenimiento = ultimo_mantenimiento.fecha_fin
    else:
        vehiculo.fecha_ultimo_mantenimiento = vehiculo.fecha_ultimo_mantenimiento  # Otra opción si no hay mantenimientos restantes
    vehiculo.save()




@receiver(post_save, sender=Viaje)
def actualizar_kilometraje(sender, instance, **kwargs):
    vehiculo = instance.vehiculo
    if instance.kilometraje_de_llegada > vehiculo.km_recorridos:
        vehiculo.km_recorridos = instance.kilometraje_de_llegada
        vehiculo.save()




@receiver(pre_delete, sender=Viaje)
def revertir_kilometraje(sender, instance, **kwargs):
    vehiculo = instance.vehiculo
    viajes_restantes = Viaje.objects.filter(vehiculo=vehiculo).exclude(id=instance.id).order_by('-kilometraje_de_llegada')
    if viajes_restantes.exists():
        ultimo_viaje = viajes_restantes.first()
        vehiculo.km_recorridos = ultimo_viaje.kilometraje_de_llegada
    else:
        vehiculo.km_recorridos = vehiculo.km_recorridos  # Otra opción si no hay mantenimientos restantes
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
    if instance.image2:
        if os.path.isfile(instance.image2.path):
            os.remove(instance.image2.path)
    if instance.image3:
        if os.path.isfile(instance.image3.path):
            os.remove(instance.image3.path)

@receiver(pre_save, sender=MantenimientoVehiculo)
def eliminar_imagen_anterior_al_actualizar_mantenimineto(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        mantenimiento_anterior = MantenimientoVehiculo.objects.get(pk=instance.pk)
    except MantenimientoVehiculo.DoesNotExist:
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

#---------------------------------------------------------------------------------------------

@receiver(pre_delete, sender=Viaje)
def eliminar_imagen_de_viaje(sender, instance, **kwargs):
    # Verificar si Vehiculo tiene una imagen asociada y eliminarla
    if instance.imagen_de_salida:
        if os.path.isfile(instance.imagen_de_salida.path):
            os.remove(instance.imagen_de_salida.path)
    if instance.imagen_de_llegada:
        if os.path.isfile(instance.imagen_de_llegada.path):
            os.remove(instance.imagen_de_llegada.path)


@receiver(pre_save, sender=Viaje)
def eliminar_imagen_anterior_al_actualizar_viaje(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        viaje_anterior = Viaje.objects.get(pk=instance.pk)
    except Viaje.DoesNotExist:
        return False

    # Comparar y eliminar image
    if viaje_anterior.imagen_de_salida and instance.imagen_de_salida != viaje_anterior.imagen_de_salida:
        if os.path.isfile(viaje_anterior.imagen_de_salida.path):
            os.remove(viaje_anterior.imagen_de_salida.path)

    # Comparar y eliminar image2
    if viaje_anterior.imagen_de_llegada and instance.imagen_de_llegada != viaje_anterior.imagen_de_llegada:
        if os.path.isfile(viaje_anterior.imagen_de_llegada.path):
            os.remove(viaje_anterior.imagen_de_llegada.path)

