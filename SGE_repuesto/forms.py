from django import forms
from .models import Maquina

class MaquinaRepuestoForm(forms.ModelForm):    
    class Meta:
        model = Maquina
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de la máquina'}),            
        }