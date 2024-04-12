from django.db import models

# Create your models here.
class Maquina(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.nombre


class Partes(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    partes = models.ForeignKey(Partes, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, null=False, blank=False)
    rosca = models.CharField(max_length=50, null=True, blank=True)
    largo = models.CharField(max_length=50, null=True, blank=True)
    und = models.CharField(max_length=50, null=True, blank=True)
    cantidad_necesaria = models.IntegerField(null=False, blank=False)
    existencia_stock = models.IntegerField(null=False, blank=False)
    salida = models.IntegerField(null=False, blank=False)

    def existencia_fisica(self):
        cantidad_existencia_fisica = self.existencia_stock - self.salida
        return cantidad_existencia_fisica 
    
    def __str__(self):
        txt = "Parte: {}"
        return txt.format(self.partes)

