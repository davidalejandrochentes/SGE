from django import forms
from .models import Area
from django.forms import Textarea

class AreaForm(forms.ModelForm):
    
    class Meta:
        model = Area
        fields = '__all__' 
        exclude = ['fecha_ultimo_mantenimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre del Area'}),
            'tamaño': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Tamaño del Area'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Encargado del Area'}),
            'teléfono_encargado': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje +53589874'}),
            'descripción': Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'ubicación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: primer piso'}),
            'capacidad': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "4 personas", "3 Carros"...'}),
            'tipo_de_área': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "Oficina", "Comedor"...'}),
            'estado_de_ocupación': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Eje: "ocupada", "En reparación"'}),
            'intervalo_mantenimiento': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number'}),
        }
