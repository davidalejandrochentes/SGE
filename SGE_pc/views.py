from django.shortcuts import render, redirect, get_object_or_404
from .models import PC, MantenimientoPC, TipoMantenimientoPC
from .forms import PCForm, MantenimientoPCForm
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
def pc(request):
    alert = PC.objects.all()
    pcs = PC.objects.filter(nombre__icontains=request.GET.get('search', ''))
    total_pcs = len(pcs)
    alertas = []
    for pc in alert:
        dias_restantes = pc.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'pc': pc,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'pcs': pcs,
        'total_pcs': total_pcs,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_pc/pc.html', context)

@login_required
def alertas(request):
    alert = PC.objects.filter(nombre__icontains=request.GET.get('search', ''))
    alertas = []
    for pc in alert:
        dias_restantes = pc.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            alertas.append({
                'pc': pc,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_pc/alertas.html', context)

@login_required
def tabla_mantenimientos(request):
    pcs = PC.objects.all()
    tipos_mantenimiento = TipoMantenimientoPC.objects.all()
    for pc in pcs:
        pc.mantenimientos = pc.mantenimientopc_set.all().order_by('-fecha', '-hora')
    context = {
        'pcs': pcs,
        'tipos_mantenimiento': tipos_mantenimiento,
    }
    return render(request, 'SGE_pc/tablas.html', context)

@login_required
def crear_pc(request):
    if request.method == 'GET':
        form = PCForm()
        context = {
            'form': form
        }
        return render(request, 'SGE_pc/nueva.html', context)
    if request.method == 'POST':
        form = PCForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES al formulario
        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'form': form
                }
                return render(request, 'SGE_pc/nueva.html', context)
            else:
                # Manejo del archivo de imagen
                if 'image' in request.FILES:
                    form.instance.image = request.FILES['image']

                form.save()
                return redirect('pc')
        else:
            context = {
                'form': form
            }
            messages.error(request, "Alguno de los datos introducidos no son válidos, revise nuevamente cada campo") 
            return render(request, 'SGE_pc/nueva.html', context)

@login_required
def eliminar(request, id):
    pc = get_object_or_404(PC, id=id)
    pc.delete()
    return redirect('pc')

@login_required
def eliminar_mantenimiento(request, id):
    mantenimiento = get_object_or_404(MantenimientoPC, id=id)
    mantenimiento.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)

@login_required    
def detalles(request, id):
    if request.method == 'GET':
        pc = get_object_or_404(PC, id=id)
        mantenimientos = pc.mantenimientopc_set.all().order_by('-fecha', '-hora')
        form = PCForm(instance=pc)
        form_mant = MantenimientoPCForm()
        tipos_mantenimiento = TipoMantenimientoPC.objects.all()
        context = {
            'pc': pc,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
            }
        return render(request, 'SGE_pc/detalles.html', context)
    
    if request.method == 'POST':
        pc = get_object_or_404(PC, id=id)
        form_mant = MantenimientoPCForm(request.POST, request.FILES)
        form = PCForm(instance=pc)
        form = PCForm(request.POST, request.FILES, instance=pc)

        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form_mant = MantenimientoPCForm()
                tipos_mantenimiento = TipoMantenimientoPC.objects.all()
                mantenimientos = pc.mantenimientopc_set.all().order_by('-fecha', '-hora')
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'pc': pc,
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
                form_mant = MantenimientoPCForm()
                tipos_mantenimiento = TipoMantenimientoPC.objects.all()
                mantenimientos = pc.mantenimientopc_set.all().order_by('-fecha', '-hora')
                context = {
                    'pc': pc,
                    'form': form,
                    'id': id,
                    'form_mant': form_mant,
                    'mantenimientos': mantenimientos,
                    'tipos_mantenimiento': tipos_mantenimiento,
                }
                return render(request, 'SGE_pc/detalles.html', context) 
        
        if form_mant.is_valid():
            mantenimiento = form_mant.save(commit=False)
            mantenimiento.pc = pc
            if 'image' in request.FILES:
                mantenimiento.image = request.FILES['image'] 
            mantenimiento.save()
            form = PCForm(instance=pc)
            tipos_mantenimiento = TipoMantenimientoPC.objects.all()
            mantenimientos = pc.mantenimientopc_set.all().order_by('-fecha', '-hora')
            context = {
            'pc': pc,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
            }
            return render(request, 'SGE_pc/detalles.html', context)  
        else:
            context = {
            'pc': pc,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
            }
            return render(request, 'SGE_pc/detalles.html', context)

@login_required
def generar_documento_mantenimientos_por_mes(request):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    mantenimientos = MantenimientoPC.objects.filter(fecha__year=anio)

    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)

    if tipo_mantenimiento_id:  # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoPC, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    mantenimientos = mantenimientos.order_by('-fecha', '-hora')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_equipos_de_cómputo_{}_{}.xlsx"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_equipos_de_cómputo_{}.xlsx"'.format(anio)

    wb = openpyxl.Workbook()
    ws = wb.active

    headers = ['E Cómputo', 'Tipo', 'Fecha I', 'Hora I', 'Fecha F', 'Hora F', 'Partes y Piezas', 'Descripción']
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)
        ws.cell(row=1, column=col).font = Font(bold=True)
        ws.cell(row=1, column=col).fill = PatternFill(start_color="BFBFBF", end_color="BFBFBF", fill_type="solid")

    row = 2
    for mantenimiento in mantenimientos:
        ws.append([
            mantenimiento.pc.nombre,
            mantenimiento.tipo.tipo,
            mantenimiento.fecha_inicio,
            mantenimiento.hora_inicio,
            mantenimiento.fecha,
            mantenimiento.hora,
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
def generar_documento_mantenimientos_pc(request, id):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    pc = get_object_or_404(PC, pk=id)
    
    mantenimientos = MantenimientoPC.objects.filter(pc=pc).order_by('-fecha', '-hora')

    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)
    if anio:
        mantenimientos = mantenimientos.filter(fecha__year=anio)
    if tipo_mantenimiento_id:  # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoPC, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_pc_{}_{}_{}.xlsx"'.format(pc.nombre, mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_pc_{}_{}.xlsx"'.format(pc.nombre, anio)   

    wb = openpyxl.Workbook()
    ws = wb.active

    # Define los encabezados de la tabla
    headers = ['Tipo', 'Fecha I', 'Hora I', 'Fecha F', 'Hora F', 'Partes y Piezas', 'Descripción']
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)
        ws.cell(row=1, column=col).font = Font(bold=True)
        ws.cell(row=1, column=col).fill = PatternFill(start_color="BFBFBF", end_color="BFBFBF", fill_type="solid")

    # Agrega los datos de los mantenimientos
    row = 2
    for mantenimiento in mantenimientos:
        ws.append([
            mantenimiento.tipo.tipo,
            mantenimiento.fecha_inicio,
            mantenimiento.hora_inicio,
            mantenimiento.fecha,
            mantenimiento.hora,
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

