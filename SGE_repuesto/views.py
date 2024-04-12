from django.shortcuts import render, redirect, get_object_or_404
from .models import Maquina, Partes, Inventario
from .forms import PCForm, MantenimientoPCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect

import openpyxl
from openpyxl.styles import Font, PatternFill

# Create your views here.
@login_required
def repuesto(request):
    pcs = PC.objects.filter(nombre__icontains=request.GET.get('search', ''))
    
    return render(request, 'SGE_repuesto/repuesto.html', {})

@login_required
def pc(request):
    alert = PC.objects.all()
    pcs = PC.objects.filter(nombre__icontains=request.GET.get('search', ''))
    
    return render(request, 'SGE_pc/pc.html', context)    