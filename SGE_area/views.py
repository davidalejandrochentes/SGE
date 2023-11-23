from django.shortcuts import render, redirect, get_object_or_404
from .models import Area, TipoMantenimientoArea, MantenimientoArea
from .forms import AreaForm, MantenimientoAreaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def area(request):
    alert = Area.objects.all()
    areas = Area.objects.filter(nombre__icontains=request.GET.get('search', ''))
    total_areas = len(areas)
    alertas = []
    for area in alert:
        dias_restantes = area.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'area': area,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'areas': areas,
        'total_areas': total_areas,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_area/area.html', context)

@login_required
def alertas(request):
    alert = Area.objects.filter(nombre__icontains=request.GET.get('search', ''))
    alertas = []
    for area in alert:
        dias_restantes = area.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'area': area,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_area/alertas.html', context)

@login_required
def tabla_mantenimientos(request):
    areas = Area.objects.all()
    context = {
        'areas': areas
    }
    return render(request, 'SGE_area/tablas.html', context)

@login_required
def crear_area(request):
    if request.method == 'GET':
        form = AreaForm()
        context = {
            'form': form
        }
        return render(request, 'SGE_area/nueva.html', context)
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid:
            form.save()
        else:
            context = {
                'form': form
            }
            messages.danger(request, "Alguno de los datos introducidos no son validos") 
            return render(request, 'SGE_area/nueva.html', context)
        return redirect('area')

@login_required    
def detalles(request, id):
    if request.method == 'GET':
        area = get_object_or_404(Area, id = id)
        form = AreaForm(instance= area)
        form_mantenimiento = MantenimientoAreaForm(initial={'area': area})
        context = {
            'area': area,
            'form': form,
            'form_mantenimiento': form_mantenimiento,
            'id': id, 
        }
        return render(request, 'SGE_area/detalles.html', context)   
    if request.method == 'POST':
        area = get_object_or_404(Area, id = id)
        form = AreaForm(request.POST, instance= area)
        if form.is_valid():
            form.save()
            context = {
                'area': area,
                'form': form,
                'id': id, 
                }
            return render(request, 'SGE_area/detalles.html', context) 
        else:
            context = {
                'area': area,
                'form': form,
                'id': id, 
                }
            messages.danger(request, "Alguno de los datos introducidos no son validos") 
            return render(request, 'SGE_area/detalles.html', context) 

@login_required
def eliminar(request, id):
    area = get_object_or_404(Area, id = id)
    area.delete()
    return redirect ('area') 
