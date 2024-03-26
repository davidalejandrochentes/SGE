from django.shortcuts import render, redirect, get_object_or_404
from .models import Herramienta, MantenimientoHerramienta, TipoMantenimientoHerramienta
from .forms import HerramientaForm, MantenimientoHerramientaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create your views here.
@login_required
def herramienta(request):
    alert = Herramienta.objects.all()
    herramientas = Herramienta.objects.filter(nombre__icontains=request.GET.get('search', ''))
    total_herramientas = len(herramientas)
    alertas = []
    for herramienta in alert:
        dias_restantes = herramienta.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'herramienta': herramienta,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'herramientas': herramientas,
        'total_herramientas': total_herramientas,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_herramienta/herramienta.html', context)    

@login_required
def alertas(request):
    alert = Herramienta.objects.filter(nombre__icontains=request.GET.get('search', ''))
    alertas = []
    for herramienta in alert:
        dias_restantes = herramienta.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'herramienta': herramienta,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_herramienta/alertas.html', context)    

@login_required
def tabla_mantenimientos(request):
    herramientas = Herramienta.objects.all()
    tipos_mantenimiento = TipoMantenimientoHerramienta.objects.all()
    for herramienta in herramientas:
        herramienta.mantenimientos = herramienta.mantenimientoherramienta_set.all().order_by('-fecha', '-hora')
    context = {
        'herramientas': herramientas,
        'tipos_mantenimiento': tipos_mantenimiento,
    }
    return render(request, 'SGE_herramienta/tablas.html', context)    


@login_required
def crear_herramienta(request):
    if request.method == 'GET':
        form = HerramientaForm()
        context = {
            'form': form
        }
        return render(request, 'SGE_herramienta/nueva.html', context)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES al formulario
        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'form': form
                }
                return render(request, 'SGE_herramienta/nueva.html', context)
            else:
                # Manejo del archivo de imagen
                if 'image' in request.FILES:
                    form.instance.image = request.FILES['image']

                form.save()
                return redirect('herramienta')
        else:
            context = {
                'form': form
            }
            messages.danger(request, "Alguno de los datos introducidos no son válidos") 
            return render(request, 'SGE_herramienta/nueva.html', context)    