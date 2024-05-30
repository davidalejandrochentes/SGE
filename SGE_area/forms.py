from django import forms
from .models import Area, MantenimientoArea
from django.forms import Textarea
from datetime import date

class AreaForm(forms.ModelForm):    
    class Meta:
        model = Area
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        labels = {
            'image': 'Imagen',  # Aquí especificamos la etiqueta con tilde
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre del area de trabajo'}),
            'tamaño': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: 4x4, 5x9'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'David A. Chentes'}),
            'teléfono_encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: +53589874'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'ubicación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: primer piso'}),
            'capacidad': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: 4 personas, 3 Carros'}),
            'tipo_de_área': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: Oficina, Comedor'}),
            'estado_de_ocupación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: ocupada, En reparación'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado de Días'}),
        }

class MantenimientoAreaForm(forms.ModelForm):
    class Meta:
        model = MantenimientoArea
        fields = '__all__'
        exclude = ['area']
        labels = {
            'image_antes': 'Imagen Antes',
            'image': 'Imagen Despues',
            'fecha': 'fecha de fin',
            'hora': 'hora de fin',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'operador': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de quien lo realizó'}),
            'tipo': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Tipo de mantenimiento'}),
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