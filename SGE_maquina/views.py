from django.shortcuts import render, redirect, get_object_or_404
from .models import Maquina, MantenimientoMaquina, TipoMantenimientoMaquina
from .forms import MaquinaForm, MantenimientoMaquinaForm
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



# Create your views here.
@login_required
def maquina(request):
    alert = Maquina.objects.all()
    maquinas = Maquina.objects.filter(nombre__icontains=request.GET.get('search', ''))
    total_maquinas = len(maquinas)
    alertas = []
    for maquina in alert:
        horas_restantes = maquina.horas_restantes_mantenimiento()
        if horas_restantes <= 100:
            
            alertas.append({
                'maquina': maquina,
                'horas_restantes': horas_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['horas_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'maquinas': maquinas,
        'total_maquinas': total_maquinas,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_maquina/maquina.html', context)


@login_required
def alertas(request):
    alert = Maquina.objects.filter(nombre__icontains=request.GET.get('search', ''))
    alertas = []
    for maquina in alert:
        horas_restantes = maquina.horas_restantes_mantenimiento()
        if horas_restantes <= 100:
            
            alertas.append({
                'maquina': maquina,
                'horas_restantes': horas_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['horas_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_maquina/alertas.html', context)


@login_required
def tabla_mantenimientos(request):
    maquinas = Maquina.objects.all()
    tipos_mantenimiento = TipoMantenimientoMaquina.objects.all()
    for maquina in maquinas:
        maquina.mantenimientos = maquina.mantenimientomaquina_set.all().order_by('-fecha', '-hora')
    context = {
        'maquinas': maquinas,
        'tipos_mantenimiento': tipos_mantenimiento,
    }
    return render(request, 'SGE_maquina/tablas.html', context)


@login_required
def crear_maquina(request):
    if request.method == 'GET':
        form = MaquinaForm()
        context = {
            'form': form
        }
        return render(request, 'SGE_maquina/nueva.html', context)
    if request.method == 'POST':
        form = MaquinaForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES al formulario
        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'form': form
                }
                return render(request, 'SGE_maquina/nueva.html', context)
            else:
                # Manejo del archivo de imagen
                if 'image' in request.FILES:
                    form.instance.image = request.FILES['image']

                form.save()
                return redirect('maquina')
        else:
            context = {
                'form': form
            }
            messages.error(request, "Alguno de los datos introducidos no son válidos, revise nuevamente cada campo") 
            return render(request, 'SGE_maquina/nueva.html', context)


@login_required
def eliminar(request, id):
    maquina = get_object_or_404(Maquina, id=id)
    maquina.delete()
    return redirect ('maquina') 

@login_required
def eliminar_mantenimiento(request, id):
    mantenimiento = get_object_or_404(MantenimientoMaquina, id=id)
    mantenimiento.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)


@login_required    
def detalles(request, id):
    if request.method == 'GET':
        maquina = get_object_or_404(Maquina, id=id)
        mantenimientos = maquina.mantenimientomaquina_set.all().order_by('-fecha', '-hora')
        form = MaquinaForm(instance=maquina)
        form_mant = MantenimientoMaquinaForm()
        tipos_mantenimiento = TipoMantenimientoMaquina.objects.all()
        context = {
            'maquina': maquina,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
        }
        return render(request, 'SGE_maquina/detalles.html', context)
    
    if request.method == 'POST':
        maquina = get_object_or_404(Maquina, id=id)
        form_mant = MantenimientoMaquinaForm(request.POST, request.FILES)
        form = MaquinaForm(instance=maquina)
        form = MaquinaForm(request.POST, request.FILES, instance=maquina)

        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form_mant = MantenimientoMaquinaForm()
                tipos_mantenimiento = TipoMantenimientoMaquina.objects.all()
                mantenimientos = maquina.mantenimientomaquina_set.all().order_by('-fecha', '-hora')
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
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
                form.save()
                form_mant = MantenimientoMaquinaForm()
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
                return render(request, 'SGE_maquina/detalles.html', context) 
        

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
def generar_documento_mantenimientos_por_mes(request):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    mantenimientos = MantenimientoMaquina.objects.filter(fecha__year=anio)

    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)

    if tipo_mantenimiento_id:  # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoMaquina, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    mantenimientos = mantenimientos.order_by('-fecha', '-hora')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}_{}.xlsx"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}.xlsx"'.format(anio)

    wb = openpyxl.Workbook()
    ws = wb.active

    headers = ['Maquina', 'Tipo', 'Fecha I', 'Hora I', 'Fecha F', 'Hora F', 'Hr Máquina', 'Partes y Piezas', 'Descripción']
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)
        ws.cell(row=1, column=col).font = Font(bold=True)
        ws.cell(row=1, column=col).fill = PatternFill(start_color="BFBFBF", end_color="BFBFBF", fill_type="solid")

    row = 2
    for mantenimiento in mantenimientos:
        ws.append([
            mantenimiento.maquina.nombre,
            mantenimiento.tipo.tipo,
            mantenimiento.fecha_inicio,
            mantenimiento.hora_inicio,
            mantenimiento.fecha,
            mantenimiento.hora,
            mantenimiento.hr_maquina,
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
def generar_documento_mantenimientos_maquina(request, id):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    maquina = get_object_or_404(Maquina, pk=id)
    mantenimientos = MantenimientoMaquina.objects.filter(maquina=maquina).order_by('-fecha', '-hora')

    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)
    if anio:
        mantenimientos = mantenimientos.filter(fecha__year=anio)
    if tipo_mantenimiento_id: # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoMaquina, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}_{}_{}.xlsx"'.format(maquina.nombre, mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}_{}.xlsx"'.format(maquina.nombre, anio)

    wb = openpyxl.Workbook()
    ws = wb.active

    # Define los encabezados de la tabla
    headers = ['Tipo', 'Fecha I', 'Hora I', 'Fecha F', 'Hora F', 'Hr Máquina', 'Partes y Piezas', 'Descripción']
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
            mantenimiento.hr_maquina,
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
