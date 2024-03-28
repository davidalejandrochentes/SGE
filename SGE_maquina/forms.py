from django import forms
from .models import Maquina, MantenimientoMaquina
from django.forms import Textarea

class MaquinaForm(forms.ModelForm):    
    class Meta:
        model = Maquina
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de la máquina'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Modelo de la máquina'}),
            'marca': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Marca de la máquina'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la máquina'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Ubicación de la máquina'}),
            'estado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Estado de la máquina'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Intervalo de mantenimiento'}),
            
        }

class MantenimientoMaquinaForm(forms.ModelForm):
    class Meta:
        model = MantenimientoMaquina
        fields = ['fecha', 'hora', 'tipo']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora'}),
            'tipo': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Tipo de mantenimiento'}),
        }
