from django import forms
from .models import Vehiculo, MantenimientoVehiculo
from django.forms import Textarea
from datetime import date

class VehiculoForm(forms.ModelForm):    
    class Meta:
        model = Vehiculo
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        labels = {
            'image': 'Imagen',
            'matricula': 'matrícula',
            'dni_chofer': 'DNI?',
        }
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: KIA'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: Picanto'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: B1542C'}),
            'número_de_chasis': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: 458979BD56'}),
            'motor': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: V8'}),
            'km_recorridos': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': '?km'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado en Km'}),

            'nombre_chofer': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: Juan Chentes'}),
            'contraseña_chofer': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': '1234juan'}),
            'teléfono_chofer': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: +53589874'}),
            'dirección_chofer': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Dirección'}),
            'dni_chofer': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'DNI?'}),
        }


class MantenimientoVehiculoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoVehiculo
        fields = '__all__'
        exclude = ['vehiculo']
        labels = {
            'km_recorridos': 'km recorridos',
            'image': 'Imagen',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'operador': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de quien lo realizó'}),
            'tipo': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Tipo de mantenimiento'}),
            'km_recorridos': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Km?'}),
            'partes_y_piezas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Partes y piezas implicadas'}),
            'descripción': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del mantenimiento'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio > date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser en el futuro.')
        
        if fecha_fin > date.today():
            self.add_error('fecha_fin', 'La fecha de fin no puede ser en el futuro.')
        
        return cleaned_data
