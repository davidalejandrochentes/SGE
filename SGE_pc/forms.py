from django import forms
from .models import PC, MantenimientoPC
from django.forms import Textarea

class PCForm(forms.ModelForm):    
    class Meta:
        model = PC
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre del PC'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: DEll, HP, Azuz'}),
            'numero_de_inventario': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: B145C394'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: David A. Chentes'}),
            'teléfono_encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: +53589874'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'ubicación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: oficina de ...'}),
            'costo_de_adquisición': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': '$'}),
            'fecha_de_adquisición': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'fecha_de_retirada': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'estado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: bueno, malo, regular'}),
            'garantía': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: si, no'}),
            'software_instalado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: windows, linux, mac'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado de "Días"'}),
            
        }

class MantenimientoPCForm(forms.ModelForm):
    class Meta:
        model = MantenimientoPC
        fields = ['fecha', 'hora', 'tipo']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora'}),
            'tipo': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Tipo de mantenimiento'}),
        }
