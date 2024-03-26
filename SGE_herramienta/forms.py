from django import forms
from .models import Herramienta, MantenimientoHerramienta
from django.forms import Textarea

class HerramientaForm(forms.ModelForm):    
    class Meta:
        model = Herramienta
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de la herramienta'}),
            'número_de_serie': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: B145C394'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'David A. Chentes'}),
            'teléfono_encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "+53589874"'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),            
            'fecha_de_adquisición': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': '$'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "Makita'}),
            'ubicación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: taller'}),
            'estado_de_la_herramienta': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "bueno"'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado de "Días"'}),
        }

class MantenimientoHerramientaForm(forms.ModelForm):
    class Meta:
        model = MantenimientoHerramienta
        fields = ['fecha', 'hora', 'tipo']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora'}),
            'tipo': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Tipo de mantenimiento'}),
        }
