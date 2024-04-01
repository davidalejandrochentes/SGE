from django import forms
from .models import Maquina, MantenimientoMaquina, Componente, MantenimientoComponente
from django.forms import Textarea

class MaquinaForm(forms.ModelForm):    
    class Meta:
        model = Maquina
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de la máquina'}),
            'tipo_de_máquina': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de la máquina'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: David A. Chentes'}),
            'teléfono_encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: +53589874'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'ubicación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: oficina de ...'}),
            'número_de_serie_o_modelo': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: B145C394'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "Makita'}),
            'costo_de_adquisición': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': '$'}),
            'fecha_de_adquisición': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'fecha_de_instalación': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'estado_de_garantía': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: si, no'}),
            'consumo_de_energía': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: 200KW'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado de Días'}),
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


class ComponenteForm(forms.ModelForm):    
    class Meta:
        model = Componente
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre del componente'}),
            'maquina': forms.Select(attrs={'class': 'form-select m-2'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'número_de_serie_o_modelo': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: B145C394'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "Makita'}),
            'costo_de_adquisición': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': '$'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado de Días'}),
        }        

class MantenimientoComponenteForm(forms.ModelForm):
    class Meta:
        model = MantenimientoComponente
        fields = ['fecha', 'hora', 'tipo']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora'}),
            'tipo': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Tipo de mantenimiento'}),
        }