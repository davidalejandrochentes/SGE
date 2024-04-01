from django.shortcuts import render, redirect, get_object_or_404
from .models import Maquina, MantenimientoMaquina, TipoMantenimientoMaquina, Componente, MantenimientoComponente, TipoMantenimientoComponente
from .forms import MaquinaForm, MantenimientoMaquinaForm, ComponenteForm, MantenimientoComponenteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create your views here.
@login_required
def maquina(request):
    alert = Maquina.objects.all()
    maquinas = Maquina.objects.filter(nombre__icontains=request.GET.get('search', ''))
    total_maquinas = len(maquinas)
    alertas = []
    for maquina in alert:
        dias_restantes = maquina.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'maquina': maquina,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
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
        dias_restantes = maquina.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'maquina': maquina,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
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
        form_mant = MantenimientoMaquinaForm(request.POST)
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
            return render(request, 'SGE_maquina/detalles.html', context)  
        else:
            context = {
                'maquina': maquina,
                'form': form,
                'id': id,
                'form_mant': form_mant,
                'mantenimientos': mantenimientos,
                'tipos_mantenimiento': tipos_mantenimiento,
            }
            return render(request, 'SGE_maquina/detalles.html', context)

    
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

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}_{}.pdf"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}.pdf"'.format(anio)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Maquina', 'Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.maquina, mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
    else:
        data.append(['Maquina', 'Tipo', 'Mes', 'Año', 'Dia', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.maquina, mantenimiento.tipo, mantenimiento.fecha.month, mantenimiento.fecha.year, mantenimiento.fecha.day, mantenimiento.hora])

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
    if tipo_mantenimiento_id:  # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoMaquina, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}_{}_{}.pdf"'.format(maquina.nombre, mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_maquinas_{}_{}.pdf"'.format(maquina.nombre, anio)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
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
    

#------------------------------------------------------------------------------------------------------------------

@login_required
def componente(request):
    alert = Componente.objects.all()
    componentes = Componente.objects.filter(nombre__icontains=request.GET.get('search', ''))
    total_componentes = len(componentes)
    alertas = []
    for componente in alert:
        dias_restantes = componente.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'componente': componente,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'componentes': componentes,
        'total_componentes': total_componentes,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_maquina/componente/componente.html', context)

@login_required
def alertasComp(request):
    alert = Componente.objects.filter(nombre__icontains=request.GET.get('search', ''))
    alertas = []
    for componente in alert:
        dias_restantes = componente.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'componente': componente,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_maquina/componente/alertas.html', context)

@login_required
def tabla_mantenimientosComp(request):
    componentes = Componente.objects.all()
    tipos_mantenimiento = TipoMantenimientoComponente.objects.all()
    for componente in componentes:
        componente.mantenimientos = componente.mantenimientocomponente_set.all().order_by('-fecha', '-hora')
    context = {
        'componentes': componentes,
        'tipos_mantenimiento': tipos_mantenimiento,
    }
    return render(request, 'SGE_maquina/componente/tablas.html', context)

@login_required
def crear_componente(request):
    if request.method == 'GET':
        form = ComponenteForm()
        context = {
            'form': form
        }
        return render(request, 'SGE_maquina/componente/nueva.html', context)
    if request.method == 'POST':
        form = ComponenteForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES al formulario
        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'form': form
                }
                return render(request, 'SGE_maquina/componente/nueva.html', context)
            else:
                # Manejo del archivo de imagen
                if 'image' in request.FILES:
                    form.instance.image = request.FILES['image']

                form.save()
                return redirect('componente')
        else:
            context = {
                'form': form
            }
            messages.error(request, "Alguno de los datos introducidos no son válidos, revise nuevamente cada campo") 
            return render(request, 'SGE_maquina/componente/nueva.html', context)


@login_required
def eliminarComp(request, id):
    componente = get_object_or_404(Componente, id=id)
    componente.delete()
    return redirect('componente') 

@login_required
def eliminar_mantenimientoComp(request, id):
    mantenimiento = get_object_or_404(MantenimientoComponente, id=id)
    mantenimiento.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)


@login_required
def detallesComp(request, id):
    if request.method == 'GET':
        componente = get_object_or_404(Componente, id=id)
        mantenimientos = componente.mantenimientocomponente_set.all().order_by('-fecha', '-hora')
        form = ComponenteForm(instance=componente)
        form_mant = MantenimientoComponenteForm()
        tipos_mantenimiento = TipoMantenimientoComponente.objects.all()
        context = {
            'componente': componente,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
            }
        return render(request, 'SGE_maquina/componente/detalles.html', context)
    
    if request.method == 'POST':
        componente = get_object_or_404(Componente, id=id)
        form_mant = MantenimientoComponenteForm(request.POST)
        form = ComponenteForm(instance=componente)
        form = ComponenteForm(request.POST, request.FILES, instance=componente)

        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form_mant = MantenimientoComponenteForm()
                tipos_mantenimiento = TipoMantenimientoComponente.objects.all()
                mantenimientos = componente.mantenimientocomponente_set.all().order_by('-fecha', '-hora')
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'componente': componente,
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
                form_mant = MantenimientoComponenteForm()
                tipos_mantenimiento = TipoMantenimientoComponente.objects.all()
                mantenimientos = componente.mantenimientocomponente_set.all().order_by('-fecha', '-hora')
                context = {
                    'componente': componente,
                    'form': form,
                    'id': id,
                    'form_mant': form_mant,
                    'mantenimientos': mantenimientos,
                    'tipos_mantenimiento': tipos_mantenimiento,
                }
                return render(request, 'SGE_maquina/componente/detalles.html', context) 
        
        if form_mant.is_valid():
            mantenimiento = form_mant.save(commit=False)
            mantenimiento.componente = componente
            mantenimiento.save()
            form = ComponenteForm(instance=componente)
            tipos_mantenimiento = TipoMantenimientoComponente.objects.all()
            mantenimientos = componente.mantenimientocomponente_set.all().order_by('-fecha', '-hora')
            context = {
                'componente': componente,
                'form': form,
                'id': id,
                'form_mant': form_mant,
                'mantenimientos': mantenimientos,
                'tipos_mantenimiento': tipos_mantenimiento,
            }
            return render(request, 'SGE_maquina/componente/detalles.html', context)  
        else:
            context = {
                'componente': componente,
                'form': form,
                'id': id,
                'form_mant': form_mant,
                'mantenimientos': mantenimientos,
                'tipos_mantenimiento': tipos_mantenimiento,
            }
            return render(request, 'SGE_maquina/componente/detalles.html', context)

@login_required
def generar_documento_mantenimientos_por_mesComp(request):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_componente_id = request.GET.get('tipo_componente')

    mantenimientos = MantenimientoComponente.objects.filter(fecha__year=anio)

    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)

    if tipo_componente_id:  # Si se seleccionó un tipo de componente
        tipo_componente = get_object_or_404(TipoComponente, pk=tipo_componente_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_componente)

    mantenimientos = mantenimientos.order_by('-fecha', '-hora')

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_componentes_{}_{}.pdf"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_componentes_{}.pdf"'.format(anio)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Componente', 'Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.componente, mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
    else:
        data.append(['Componente', 'Tipo', 'Mes', 'Año', 'Dia', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.componente, mantenimiento.tipo, mantenimiento.fecha.month, mantenimiento.fecha.year, mantenimiento.fecha.day, mantenimiento.hora])

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
def generar_documento_mantenimientos_componente(request, id):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_componente_id = request.GET.get('tipo_componente')

    componente = get_object_or_404(Componente, pk=id)
    
    mantenimientos = MantenimientoComponente.objects.filter(componente=componente).order_by('-fecha', '-hora')

    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)
    if anio:
        mantenimientos = mantenimientos.filter(fecha__year=anio)
    if tipo_componente_id:  # Si se seleccionó un tipo de componente
        tipo_componente = get_object_or_404(TipoComponente, pk=tipo_componente_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_componente)

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_componentes_{}_{}_{}.pdf"'.format(componente.nombre, mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_componentes_{}_{}.pdf"'.format(componente.nombre, anio)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
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


