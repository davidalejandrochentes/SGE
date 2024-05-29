from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo, MantenimientoVehiculo, TipoMantenimientoVehiculo, Viaje
from .forms import VehiculoForm, MantenimientoVehiculoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

import openpyxl
from openpyxl.styles import Font, PatternFill

@login_required
def vehiculo(request):
    alert = Vehiculo.objects.all()
    vehiculos = Vehiculo.objects.filter(marca__icontains=request.GET.get('search', ''))
    total_vehiculos = len(vehiculos)
    alertas = []
    for vehiculo in alert:
        horas_restantes = vehiculo.km_restantes_mantenimiento()
        if horas_restantes <= 100:
            
            alertas.append({
                'vehiculo': vehiculo,
                'horas_restantes': horas_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['horas_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'vehiculos': vehiculos,
        'total_vehiculos': total_vehiculos,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_vehiculo/vehiculo.html', context)


@login_required
def crear_vehiculo(request):
    if request.method == 'GET':
        form = VehiculoForm()
        context = {
            'form': form
        }
        return render(request, 'SGE_vehiculo/nuevo.html', context)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES al formulario
        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'form': form
                }
                return render(request, 'SGE_vehiculo/nuevo.html', context)
            else:
                # Manejo del archivo de imagen
                if 'image' in request.FILES:
                    form.instance.image = request.FILES['image']
                form.save()
                return redirect('vehiculo')
        else:
            context = {
                'form': form
            }
            messages.error(request, "Alguno de los datos introducidos no son válidos, revise nuevamente cada campo") 
            return render(request, 'SGE_vehiculo/nuevo.html', context)    

@login_required
def alertas(request):
    alert = Vehiculo.objects.filter(marca__icontains=request.GET.get('search', ''))
    alertas = []
    for vehiculo in alert:
        horas_restantes = vehiculo.km_restantes_mantenimiento()
        if horas_restantes <= 100:
            
            alertas.append({
                'vehiculo': vehiculo,
                'horas_restantes': horas_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['horas_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_vehiculo/alertas.html', context)      



@login_required    
def detalles(request, id):
    if request.method == 'GET':
        vehiculo = get_object_or_404(Vehiculo, id=id)
        mantenimientos = vehiculo.mantenimientovehiculo_set.all().order_by('-fecha_fin', '-hora_fin')
        form = VehiculoForm(instance=vehiculo)
        form_mant = MantenimientoVehiculoForm()
        tipos_mantenimiento = TipoMantenimientoVehiculo.objects.all()
        context = {
            'vehiculo': vehiculo,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
        }
        return render(request, 'SGE_vehiculo/detalles.html', context)
    
    if request.method == 'POST':
        vehiculo = get_object_or_404(Vehiculo, id=id)
        form_mant = MantenimientoVehiculoForm(request.POST, request.FILES)
        form = VehiculoForm(instance=vehiculo)
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)

        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form_mant = MantenimientoVehiculoForm()
                tipos_mantenimiento = TipoMantenimientoVehiculo.objects.all()
                mantenimientos = vehiculo.mantenimientovehiculo_set.all().order_by('-fecha_fin', '-hora_fin')
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'vehiculo': vehiculo,
                    'form': form,
                    'id': id,
                    'form_mant': form_mant,
                    'mantenimientos': mantenimientos,
                    'tipos_mantenimiento': tipos_mantenimiento,
                }
                previous_url = request.META.get('HTTP_REFERER')
                return HttpResponseRedirect(previous_url)
            else:
                form.save()
                form_mant = MantenimientoVehiculoForm()
                tipos_mantenimiento = TipoMantenimientoVehiculo.objects.all()
                mantenimientos = vehiculo.mantenimientovehiculo_set.all().order_by('-fecha_fin', '-hora_fin')
                context = {
                    'vehiculo': vehiculo,
                    'form': form,
                    'id': id,
                    'form_mant': form_mant,
                    'mantenimientos': mantenimientos,
                    'tipos_mantenimiento': tipos_mantenimiento,
                }
                return render(request, 'SGE_vehiculo/detalles.html', context) 
        

        if form_mant.is_valid():
            mantenimiento = form_mant.save(commit=False)
            mantenimiento.maquina = maquina
            if 'image' in request.FILES:
                mantenimiento.image = request.FILES['image'] 
            mantenimiento.save()
            form = MaquinaForm(instance=maquina)
            tipos_mantenimiento = TipoMantenimientoMaquina.objects.all()
            mantenimientos = maquina.mantenimientomaquina_set.all().order_by('-fecha', '-hora')
            context = {
                'maquina': maquina,
                'form': form,
                'id': id,
                'form_mant': form_mant,
                'mantenimientos': mantenimientos,
                'tipos_mantenimiento': tipos_mantenimiento,
            }
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url)
        else:
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url) 


@login_required
def eliminar(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    return redirect ('vehiculo')    