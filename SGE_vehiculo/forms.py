from django import forms
from .models import Vehiculo, MantenimientoVehiculo
from django.forms import Textarea, FileInput
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
            'km_recorridos': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'km?'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado en Km'}),
            'image': FileInput(attrs={'class': 'form-control-file m-2'}),

            'nombre_chofer': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: Juan Chentes'}),
            'contraseña_chofer': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': '1234juan'}),
            'teléfono_chofer': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: +53589874'}),
            'dirección_chofer': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Dirección'}),
            'dni_chofer': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'DNI?'}),
        }


class MantenimientoVehiculoCorrectivoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoVehiculo
        fields = '__all__'
        exclude = ['vehiculo', 'tipo']
        labels = {
            'km_recorridos': 'km recorridos',
            'image': 'Imagen#1',
            'image2': 'Imagen#2',
            'image3': 'Imagen#3',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'operador': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de quien lo realizó'}),
            'km_recorridos': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Km?'}),
            'partes_y_piezas': forms.Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Partes y piezas implicadas'}),
            'descripción': forms.Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Descripción del mantenimiento'}),
            'image': FileInput(attrs={'class': 'form-control-file m-2'}),
            'image2': FileInput(attrs={'class': 'form-control-file m-2'}),
            'image3': FileInput(attrs={'class': 'form-control-file m-2'}),
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


class MantenimientoVehiculoPreventivoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoVehiculo
        fields = '__all__'
        exclude = ['vehiculo', 'tipo', 'partes_y_piezas']
        labels = {
            'km_recorridos': 'km recorridos',
            'image': 'Imagen#1',
            'image2': 'Imagen#2',
            'image3': 'Imagen#3',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'operador': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de quien lo realizó'}),
            'km_recorridos': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Km?'}),
            'descripción': forms.Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Descripción del mantenimiento'}),
            'image': FileInput(attrs={'class': 'form-control-file m-2'}),
            'image2': FileInput(attrs={'class': 'form-control-file m-2'}),
            'image3': FileInput(attrs={'class': 'form-control-file m-2'}),
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