from django import forms
from .models import Vehiculo, MantenimientoVehiculo, Viaje
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
            'intervalo_mantenimiento': 'Intervalo entre manteniminetos correctivos',
            'intervalo_mantenimiento_cambio_filtro_aceite': 'Intervalo entre manteniminetos para cambio del filtro de aceite',
            'intervalo_mantenimiento_cambio_filtro_aire_combustible': 'Intervalo entre manteniminetos para cambio del filtro de aire y combustible',
            'intervalo_mantenimiento_cambio_filtro_caja_corona': 'Intervalo entre manteniminetos para cambio del filtro de caja y corona',
        }
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: KIA'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: Picanto'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: B1542C'}),
            'número_de_chasis': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: 458979BD56'}),
            'motor': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: V8'}),
            'km_recorridos': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'km?'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado en Km'}),
            'intervalo_mantenimiento_cambio_filtro_aceite': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado en Km'}),
            'intervalo_mantenimiento_cambio_filtro_aire_combustible': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado en Km'}),
            'intervalo_mantenimiento_cambio_filtro_caja_corona': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Número determinado en Km'}),
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



class ViajeVehiculoForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = '__all__'
        exclude = ['vehiculo']
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Lugar de partida'}),
            'destino': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Lugar de llegada'}),

            'fecha_salida': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'kilometraje_de_salida': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Km?', 'readonly': 'readonly'}),
            'imagen_de_salida': FileInput(attrs={'class': 'form-control-file m-2'}),

            'fecha_llegada': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora_llegada': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'kilometraje_de_llegada': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Km?'}),
            'imagen_de_llegada': FileInput(attrs={'class': 'form-control-file m-2'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_salida = cleaned_data.get('fecha_salida')
        fecha_llegada = cleaned_data.get('fecha_llegada')
        kilometraje_de_salida = cleaned_data.get('kilometraje_de_salida')
        kilometraje_de_llegada = cleaned_data.get('kilometraje_de_llegada')

        if kilometraje_de_salida > kilometraje_de_llegada:
            self.add_error('kilometraje_de_salida', 'El kilometraje de salida no puede ser mayor al de llegada')

        if kilometraje_de_llegada < kilometraje_de_salida:
            self.add_error('kilometraje_de_llegada', 'El kilometraje de llegada no puede ser menor al de salida')    
        
        if fecha_salida > date.today():
            self.add_error('fecha_salida', 'La fecha de salida no puede ser en el futuro.')
        
        if fecha_llegada > date.today():
            self.add_error('fecha_llegada', 'La fecha de llegada no puede ser en el futuro.')
        
        return cleaned_data



class ViajeVehiculoModAdminForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = '__all__'
        exclude = ['vehiculo']
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Lugar de partida'}),
            'destino': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Lugar de llegada'}),

            'fecha_salida': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de inicio'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de inicio'}),
            'kilometraje_de_salida': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Km?'}),
            'imagen_de_salida': FileInput(attrs={'class': 'form-control-file m-2'}),

            'fecha_llegada': forms.DateInput(attrs={'class': 'form-control m-2', 'placeholder': 'Fecha de fin'}),
            'hora_llegada': forms.TimeInput(attrs={'class': 'form-control m-2', 'placeholder': 'Hora de fin'}),
            'kilometraje_de_llegada': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Km?'}),
            'imagen_de_llegada': FileInput(attrs={'class': 'form-control-file m-2'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_salida = cleaned_data.get('fecha_salida')
        fecha_llegada = cleaned_data.get('fecha_llegada')
        kilometraje_de_salida = cleaned_data.get('kilometraje_de_salida')
        kilometraje_de_llegada = cleaned_data.get('kilometraje_de_llegada')

        if kilometraje_de_salida > kilometraje_de_llegada:
            self.add_error('kilometraje_de_salida', 'El kilometraje de salida no puede ser mayor al de llegada')

        if kilometraje_de_llegada < kilometraje_de_salida:
            self.add_error('kilometraje_de_llegada', 'El kilometraje de llegada no puede ser menor al de salida')    
        
        if fecha_salida > date.today():
            self.add_error('fecha_salida', 'La fecha de salida no puede ser en el futuro.')
        
        if fecha_llegada > date.today():
            self.add_error('fecha_llegada', 'La fecha de llegada no puede ser en el futuro.')
        
        return cleaned_data                