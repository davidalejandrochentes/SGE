from django.shortcuts import render, redirect, get_object_or_404
from .models import Herramienta, MantenimientoHerramienta, TipoMantenimientoHerramienta
#from .forms import AreaForm, MantenimientoAreaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create your views here.
def herramienta(request):
    return HttpResponse("todo funciona")

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