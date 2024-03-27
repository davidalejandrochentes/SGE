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
        form_mant = MantenimientoPCForm(request.POST)
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

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_pc_{}_{}.pdf"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_pc_{}.pdf"'.format(anio)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['PC', 'Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.pc, mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
    else:
        data.append(['PC', 'Tipo', 'Mes', 'Año', 'Dia', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.pc, mantenimiento.tipo, mantenimiento.fecha.month, mantenimiento.fecha.year, mantenimiento.fecha.day, mantenimiento.hora])

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

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_pc_{}_{}_{}.pdf"'.format(pc.nombre, mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_pc_{}_{}.pdf"'.format(pc.nombre, anio)   

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
    else:
        data.append(['Tipo', 'Mes', 'Año', 'Día', 'Hora'])
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

