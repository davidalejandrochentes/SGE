from django.shortcuts import render, redirect, get_object_or_404
from .models import Area, MantenimientoArea
from .forms import AreaForm, MantenimientoAreaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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
    for area in areas:
        area.mantenimientos = area.mantenimientoarea_set.all().order_by('-fecha', '-hora')
    context = {
        'areas': areas,
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
def eliminar(request, id):
    area = get_object_or_404(Area, id = id)
    area.delete()
    return redirect ('area') 

@login_required
def eliminar_mantenimiento(request, id):
    mantenimiento = get_object_or_404(MantenimientoArea, id=id)
    mantenimiento.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)

@login_required    
def detalles(request, id):
    if request.method == 'GET':
        area = get_object_or_404(Area, id=id)
        mantenimientos = area.mantenimientoarea_set.all().order_by('-fecha', '-hora')
        form = AreaForm(instance=area)
        form_mant = MantenimientoAreaForm()
        context = {
            'area': area,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos
            }
        return render(request, 'SGE_area/detalles.html', context)
    
    if request.method == 'POST':
        area = get_object_or_404(Area, id = id)
        form_mant = MantenimientoAreaForm(request.POST)
        form = AreaForm(instance= area)
        form = AreaForm(request.POST, instance= area)

        if form.is_valid():
            form.save()
            form_mant = MantenimientoAreaForm()
            mantenimientos = area.mantenimientoarea_set.all().order_by('-fecha', '-hora')
            context = {
            'area': area,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos
            }
            return render(request, 'SGE_area/detalles.html', context) 
        
        if form_mant.is_valid():
            mantenimiento = form_mant.save(commit=False)
            mantenimiento.area = area
            mantenimiento.save()
            form = AreaForm(instance= area)
            mantenimientos = area.mantenimientoarea_set.all().order_by('-fecha', '-hora')
            context = {
            'area': area,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos
            }
            return render(request, 'SGE_area/detalles.html', context)  
        else:
            context = {
            'area': area,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos
            }
            return render(request, 'SGE_area/detalles.html', context) 
    
@login_required
def generar_documento_mantenimientos_por_mes(request):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')

    if mes:  # Si se seleccionó un mes
        mantenimientos = MantenimientoArea.objects.filter(fecha__month=mes, fecha__year=anio).order_by('-fecha', '-hora')
    else:  # Si no se seleccionó un mes
        mantenimientos = MantenimientoArea.objects.filter(fecha__year=anio).order_by('-fecha', '-hora')

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_areas_{}_{}.pdf"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_areas_{}.pdf"'.format(anio)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Area', 'Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.area, mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
    else:
        data.append(['Area', 'Tipo', 'Mes', 'Año', 'Dia', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.area, mantenimiento.tipo, mantenimiento.fecha.month, mantenimiento.fecha.year, mantenimiento.fecha.day, mantenimiento.hora])

    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

@login_required
def generar_documento_mantenimientos_area(request, id):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')

    area = get_object_or_404(Area, pk=id)

    if mes:  # Si se seleccionó un mes
        mantenimientos = MantenimientoArea.objects.filter(fecha__month=mes, fecha__year=anio, area=area).order_by('-fecha', '-hora')
    else:  # Si no se seleccionó un mes
        mantenimientos = MantenimientoArea.objects.filter(fecha__year=anio, area=area).order_by('-fecha', '-hora')    

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_areas_{}_{}_{}.pdf"'.format(area.nombre,mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_areas_{}_{}.pdf"'.format(area.nombre,anio)   

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.area, mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
    else:
        data.append(['Tipo', 'Mes', 'Año', 'Dia', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.tipo, mantenimiento.fecha.month, mantenimiento.fecha.year, mantenimiento.fecha.day, mantenimiento.hora])

    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response    
