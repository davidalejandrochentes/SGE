from django.db import models

# Create your models here.
class Maquina(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.nombre


class Parte(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    #image = models.ImageField(upload_to="repuesto/image", null=False, blank=False, default=None) 
    
    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    parte = models.ForeignKey(Parte, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, null=False, blank=False)
    rosca = models.CharField(max_length=50, null=False, blank=False)
    largo = models.CharField(max_length=50, null=False, blank=False)
    und = models.CharField(max_length=50, null=False, blank=False)
    cantidad_necesaria = models.IntegerField(null=False, blank=False)
    existencia_stock = models.IntegerField(null=False, blank=False)
    salida = models.IntegerField(null=False, blank=False)

    def existencia_fisica(self):
        cantidad_existencia_fisica = self.existencia_stock - self.salida
        return cantidad_existencia_fisica 
    
    def __str__(self):
        txt = "Parte: {}"
        return txt.format(self.parte)
