from django.shortcuts import render, redirect, get_object_or_404
from .models import Maquina, Parte, Inventario
from .forms import MaquinaRepuestoForm, ParteRepuestoForm, InventarioRepuestoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect

import openpyxl
from openpyxl.styles import Font, PatternFill

# Create your views here.
@login_required
def repuesto_maquina(request):
    if request.method == 'GET':
        maquinas = Maquina.objects.filter(nombre__icontains=request.GET.get('search', ''))
        form = MaquinaRepuestoForm()
        context = {
            'maquinas': maquinas,
            'form': form
        }
        return render(request, 'SGE_repuesto/repuesto.html', context)
    if request.method == 'POST':
        form = MaquinaRepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            form = MaquinaRepuestoForm()
            maquinas = Maquina.objects.filter(nombre__icontains=request.GET.get('search', ''))
            context = {
            'maquinas': maquinas,
            'form': form
            }
            return render(request, 'SGE_repuesto/repuesto.html', context)
        else:
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url)   
        

@login_required
def eliminar_repuesto_maquina(request, id):
    maquina = get_object_or_404(Maquina, id=id)
    maquina.delete()
    return redirect('repuesto_maquina')


@login_required
def detalles(request, id):
    if request.method == 'GET':
        maquina = get_object_or_404(Maquina, id=id)
        partes_maquina = Parte.objects.filter(maquina=maquina)
        part_form = ParteRepuestoForm()
        inve_form = InventarioRepuestoForm()
        context = {
            'maquina': maquina,
            'partes_maquina': partes_maquina,
            'part_form': part_form,
            'inve_form': inve_form
        }
        return render(request, 'SGE_repuesto/detalles.html', context) 

    if request.method == 'POST':
        maquina = get_object_or_404(Maquina, id=id)
        partes_maquina = Parte.objects.filter(maquina=maquina)
        part_form = ParteRepuestoForm(request.POST)
        inve_form = InventarioRepuestoForm(request.POST)

        if part_form.is_valid():
            parte = part_form.save(commit=False)
            parte.maquina = maquina
            parte.save()

        if inve_form.is_valid():
            inve_instance = inve_form.save(commit=False)
            parte_id = request.POST.get('parte')
            parte_instance = get_object_or_404(Parte, id=parte_id)
            inve_instance.parte = parte_instance
            inve_instance.save()

        if 'parte' in request.POST:
            parte_id = request.POST.get('parte')
            parte = get_object_or_404(Parte, id=parte_id)
            parte.delete()    

        maquina = get_object_or_404(Maquina, id=id)
        part_form = ParteRepuestoForm()
        inve_form = InventarioRepuestoForm()
        partes_maquina = Parte.objects.filter(maquina=maquina)
        context = {
            'maquina': maquina,
            'part_form': part_form,
            'partes_maquina': partes_maquina,
            'inve_form': inve_form
        }
        return render(request, 'SGE_repuesto/detalles.html', context)  