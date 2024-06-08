from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo, MantenimientoVehiculo, TipoMantenimientoVehiculo, Viaje
from .forms import VehiculoForm, MantenimientoVehiculoCorrectivoForm, MantenimientoVehiculoPreventivoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect

import openpyxl
from openpyxl.styles import Font, PatternFill



# vistas generales ----------------------------------------------------------------------------

@login_required
def vehiculo(request):
    alert = Vehiculo.objects.all()
    vehiculos = Vehiculo.objects.filter(marca__icontains=request.GET.get('search', ''))
    total_vehiculos = len(vehiculos)
    alertas = []
    for vehiculo in alert:
        km_restantes = vehiculo.km_restantes_mantenimiento()
        if km_restantes <= 1000000:
            
            alertas.append({
                'vehiculo': vehiculo,
                'km_restantes': km_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['km_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'vehiculos': vehiculos,
        'total_vehiculos': total_vehiculos,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_vehiculo/vehiculo.html', context)




@login_required
def alertas(request):
    alert = Vehiculo.objects.filter(marca__icontains=request.GET.get('search', ''))
    alertas = []
    for vehiculo in alert:
        km_restantes = vehiculo.km_restantes_mantenimiento()
        if km_restantes <= 10000000:
            
            alertas.append({
                'vehiculo': vehiculo,
                'km_restantes': km_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['km_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_vehiculo/alertas.html', context) 




@login_required
def tabla_mantenimientos(request):
    vehiculos = Vehiculo.objects.all()
    tipos_mantenimiento = TipoMantenimientoVehiculo.objects.all()
    for vehiculo in vehiculos:
        vehiculo.mantenimientos = vehiculo.mantenimientovehiculo_set.all().order_by('-fecha_fin', '-hora_fin')
    context = {
        'vehiculos': vehiculos,
        'tipos_mantenimiento': tipos_mantenimiento,
    }
    return render(request, 'SGE_vehiculo/tablas.html', context) 




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
def detalles(request, id):
    if request.method == 'GET':
        vehiculo = get_object_or_404(Vehiculo, id=id)
        mantenimientos = vehiculo.mantenimientovehiculo_set.all().order_by('-fecha_fin', '-hora_fin')
        form = VehiculoForm(instance=vehiculo)
        context = {
            'vehiculo': vehiculo,
            'form': form,
            'id': id,
            'mantenimientos': mantenimientos,
        }
        return render(request, 'SGE_vehiculo/detalles.html', context)
    
    if request.method == 'POST':
        vehiculo = get_object_or_404(Vehiculo, id=id)
        form = VehiculoForm(instance=vehiculo)
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)

        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                mantenimientos = vehiculo.mantenimientovehiculo_set.all().order_by('-fecha_fin', '-hora_fin')
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'vehiculo': vehiculo,
                    'form': form,
                    'id': id,
                    'mantenimientos': mantenimientos,
                }
                previous_url = request.META.get('HTTP_REFERER')
                return HttpResponseRedirect(previous_url)
            else:
                form.save()
                mantenimientos = vehiculo.mantenimientovehiculo_set.all().order_by('-fecha_fin', '-hora_fin')
                context = {
                    'vehiculo': vehiculo,
                    'form': form,
                    'id': id,
                    'mantenimientos': mantenimientos,
                }
                return render(request, 'SGE_vehiculo/detalles.html', context) 
        
        else:
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url) 




@login_required
def eliminar(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    return redirect ('vehiculo')    

# fin de vistas generales----------------------------------------------------------------------------------




@login_required
def eliminar_mantenimiento(request, id):
    mantenimiento = get_object_or_404(MantenimientoVehiculo, id=id)
    mantenimiento.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)




@login_required
def mod_mantenimineto_vehiculo(request, id):
    if request.method == 'GET':
        mantenimiento = get_object_or_404(MantenimientoVehiculo, id=id)
        vehiculo = mantenimiento.vehiculo
        form_mant = MantenimientoVehiculoForm(instance=mantenimiento)
        context = {
            'form_mant': form_mant,
            'vehiculo': vehiculo,
        }
        return render(request, 'SGE_vehiculo/mod_mantenimineto.html', context)
    
    if request.method == 'POST':
        mantenimiento = get_object_or_404(MantenimientoVehiculo, id=id)
        vehiculo = mantenimiento.vehiculo
        form_mant = MantenimientoVehiculoForm(request.POST, request.FILES, instance=mantenimiento)

        if form_mant.is_valid():
            mantenimiento = form_mant.save(commit=False)
            mantenimiento.vehiculo = vehiculo
            if 'image' in request.FILES:
                mantenimiento.image = request.FILES['image'] 
            mantenimiento.save()
            return redirect('detalles_vehiculo', id=vehiculo.id)
        else:
            context = {
                'form_mant': form_mant,
                'vehiculo': vehiculo,
            }
            messages.error(request, "Alguno de los datos introducidos no son válidos, revise nuevamente cada campo") 
            return render(request, 'SGE_vehiculo/mod_mantenimineto.html', context)

    return HttpResponse("Method Not Allowed", status=405)    
 


@login_required
def registro_de_viajes(request, id):
    if request.method == 'GET':
        vehiculo = get_object_or_404(Vehiculo, id=id)
        context = {
            'vehiculo': vehiculo,
        }
        return render(request, 'SGE_vehiculo/viajes.html', context)      




@login_required
def generar_documento_mantenimientos_por_mes(request):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    mantenimientos = MantenimientoVehiculo.objects.filter(fecha_fin__year=anio)

    if mes:
        mantenimientos = mantenimientos.filter(fecha_fin__month=mes)

    if tipo_mantenimiento_id:  # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoVehiculo, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    mantenimientos = mantenimientos.order_by('-fecha_fin', '-hora_fin')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_vehiculo_{}_{}.xlsx"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_vehiculo_{}.xlsx"'.format(anio)

    wb = openpyxl.Workbook()
    ws = wb.active

    headers = ['Vehiculo', 'Tipo', 'Operador', 'Fecha I', 'Hora I', 'Fecha F', 'Hora F', 'Km Recorridos', 'Partes y Piezas', 'Descripción']
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)
        ws.cell(row=1, column=col).font = Font(bold=True)
        ws.cell(row=1, column=col).fill = PatternFill(start_color="BFBFBF", end_color="BFBFBF", fill_type="solid")

    row = 2
    for mantenimiento in mantenimientos:
        ws.append([
            mantenimiento.vehiculo.modelo,
            mantenimiento.tipo.tipo,
            mantenimiento.operador,
            mantenimiento.fecha_inicio,
            mantenimiento.hora_inicio,
            mantenimiento.fecha_fin,
            mantenimiento.hora_fin,
            mantenimiento.km_recorridos,
            mantenimiento.partes_y_piezas,
            mantenimiento.descripción
        ])

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

    wb.save(response)
    return response



@login_required
def generar_documento_mantenimientos_vehiculo(request, id):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    maquina = get_object_or_404(Vehiculo, pk=id)
    mantenimientos = MantenimientoVehiculo.objects.filter(vehiculo=vehiculo).order_by('-fecha_fin', '-hora_fin')

    if mes:
        mantenimientos = mantenimientos.filter(fecha_fin__month=mes)
    if anio:
        mantenimientos = mantenimientos.filter(fecha_fin__year=anio)
    if tipo_mantenimiento_id: # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoVehiculo, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_vehiculos_{}_{}_{}.xlsx"'.format(vehiculo.marca, mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_vehiculos_{}_{}.xlsx"'.format(vehiculo.marca, anio)

    wb = openpyxl.Workbook()
    ws = wb.active

    # Define los encabezados de la tabla
    headers = ['Tipo', 'Operador', 'Fecha I', 'Hora I', 'Fecha F', 'Hora F', 'Km Recorridos', 'Partes y Piezas', 'Descripción']
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)
        ws.cell(row=1, column=col).font = Font(bold=True)
        ws.cell(row=1, column=col).fill = PatternFill(start_color="BFBFBF", end_color="BFBFBF", fill_type="solid")

    # Agrega los datos de los mantenimientos
    row = 2
    for mantenimiento in mantenimientos:
        ws.append([
            mantenimiento.tipo.tipo,
            mantenimiento.operador,
            mantenimiento.fecha_inicio,
            mantenimiento.hora_inicio,
            mantenimiento.fecha_fin,
            mantenimiento.hora_fin,
            mantenimiento.km_recorridos,
            mantenimiento.partes_y_piezas,
            mantenimiento.descripción
        ])

    # Ajusta el ancho de las columnas automáticamente
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

    wb.save(response)
    return response    