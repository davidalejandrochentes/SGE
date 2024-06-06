from django import forms
from .models import Maquina, MantenimientoMaquina
from django.forms import Textarea
from datetime import date

class MaquinaForm(forms.ModelForm):    
    class Meta:
        model = Maquina
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        labels = {
            'image': 'Imagen',  # Aquí especificamos la etiqueta con tilde
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de la máquina'}),
            'tipo_de_máquina': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'De tornedo, exe...'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: David A. Chentes'}),
            'teléfono_encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: +53589874'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'ubicación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: Taller de ...'}),
            'número_de_serie_o_modelo': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: B145C394'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "Makita'}),
            'costo_de_adquisición': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': '$'}),
            'fecha_de_adquisición': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'fecha_de_instalación': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha'}),
            'estado_de_garantía': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: si, no'}),
            'consumo_de_energía': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: 200KW'}),
            'horas_máquina_trabajada': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado de horas'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado de horas'}),
        }

class MantenimientoMaquinaCorrectivoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoMaquina
        fields = '__all__'
        exclude = ['maquina', 'tipo']
        labels = {
            'hr_maquina': 'Horas máquina de trabajo',  # Aquí especificamos la etiqueta con tilde
            'image': 'Imagen#1',
            'image2': 'Imagen#2',
            'image3': 'Imagen#3',
            'fecha': 'fecha de fin',
            'hora': 'hora de fin',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'operador': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de quien lo realizó'}),
            'hr_maquina': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Horas de trabajo al momento del Mantenimineto'}),
            'partes_y_piezas': Textarea(attrs={'class': 'form-control', 'placeholder': 'Partes y piezas implicadas'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del mantenimiento'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha')
        
        if fecha_inicio > date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser en el futuro.')
        
        if fecha_fin > date.today():
            self.add_error('fecha', 'La fecha de fin no puede ser en el futuro.')
        
        return cleaned_data    



class MantenimientoMaquinaPreventivoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoMaquina
        fields = '__all__'
        exclude = ['maquina', 'tipo', 'partes_y_piezas']
        labels = {
            'hr_maquina': 'Horas máquina de trabajo',  # Aquí especificamos la etiqueta con tilde
            'image': 'Imagen',
            'image2': 'Imagen#2',
            'image3': 'Imagen#3',
            'fecha': 'fecha de fin',
            'hora': 'hora de fin',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'operador': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de quien lo realizó'}),
            'hr_maquina': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Horas de trabajo al momento del Mantenimineto'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del mantenimiento'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha')
        
        if fecha_inicio > date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser en el futuro.')
        
        if fecha_fin > date.today():
            self.add_error('fecha', 'La fecha de fin no puede ser en el futuro.')
        
        return cleaned_data 