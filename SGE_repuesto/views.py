from django.shortcuts import render, redirect, get_object_or_404
from .models import Maquina, Partes, Inventario
#from .forms import PCForm, MantenimientoPCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect

import openpyxl
from openpyxl.styles import Font, PatternFill

# Create your views here.
@login_required
def repuesto_maquina(request):
    maquinas = Maquina.objects.filter(nombre__icontains=request.GET.get('search', ''))
    context = {
        'maquinas': maquinas
    }
    return render(request, 'SGE_repuesto/repuesto.html', context)

@login_required
def eliminar_repuesto_maquina(request, id):
    maquina = get_object_or_404(Maquina, id=id)
    maquina.delete()
    return redirect('repuesto_maquina')