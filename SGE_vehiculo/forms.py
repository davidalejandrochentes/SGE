from django import forms
from .models import Vehiculo, MantenimientoVehiculo
from django.forms import Textarea

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
            'km_recorridos': 'km recorridos',  # Aquí especificamos la etiqueta con tilde
            'image': 'Imagen',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'operador': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de quien lo realizó'}),
            'tipo': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Tipo de mantenimiento'}),
            'hr_maquina': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Horas de trabajo al momento del Mantenimineto'}),
            'partes_y_piezas': Textarea(attrs={'class': 'form-control', 'placeholder': 'Partes y piezas implicadas'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del mantenimiento'}),
        }