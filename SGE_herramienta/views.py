from django.shortcuts import render, redirect, get_object_or_404
from .models import Herramienta, MantenimientoHerramienta, TipoMantenimientoHerramienta
from .forms import HerramientaForm, MantenimientoHerramientaForm
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
def herramienta(request):
    alert = Herramienta.objects.all()
    herramientas = Herramienta.objects.filter(nombre__icontains=request.GET.get('search', ''))
    total_herramientas = len(herramientas)
    alertas = []
    for herramienta in alert:
        dias_restantes = herramienta.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'herramienta': herramienta,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'herramientas': herramientas,
        'total_herramientas': total_herramientas,
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_herramienta/herramienta.html', context)    

@login_required
def alertas(request):
    alert = Herramienta.objects.filter(nombre__icontains=request.GET.get('search', ''))
    alertas = []
    for herramienta in alert:
        dias_restantes = herramienta.dias_restantes_mantenimiento()
        if dias_restantes <= 7:
            
            alertas.append({
                'herramienta': herramienta,
                'dias_restantes': dias_restantes
            })
    alertas_ordenadas = sorted(alertas, key=lambda x: x['dias_restantes'])
    total_alertas = len(alertas_ordenadas)
    context = {
        'alertas': alertas_ordenadas,
        'total_alertas': total_alertas,
    }
    return render(request, 'SGE_herramienta/alertas.html', context)    

@login_required
def tabla_mantenimientos(request):
    herramientas = Herramienta.objects.all()
    tipos_mantenimiento = TipoMantenimientoHerramienta.objects.all()
    for herramienta in herramientas:
        herramienta.mantenimientos = herramienta.mantenimientoherramienta_set.all().order_by('-fecha', '-hora')
    context = {
        'herramientas': herramientas,
        'tipos_mantenimiento': tipos_mantenimiento,
    }
    return render(request, 'SGE_herramienta/tablas.html', context)    


@login_required
def crear_herramienta(request):
    if request.method == 'GET':
        form = HerramientaForm()
        context = {
            'form': form
        }
        return render(request, 'SGE_herramienta/nueva.html', context)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES al formulario
        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'form': form
                }
                return render(request, 'SGE_herramienta/nueva.html', context)
            else:
                # Manejo del archivo de imagen
                if 'image' in request.FILES:
                    form.instance.image = request.FILES['image']

                form.save()
                return redirect('herramienta')
        else:
            context = {
                'form': form
            }
            messages.error(request, "Alguno de los datos introducidos no son válidos, revise nuevamente cada campo") 
            return render(request, 'SGE_herramienta/nueva.html', context)    

@login_required
def eliminar(request, id):
    herramienta = get_object_or_404(Herramienta, id = id)
    herramienta.delete()
    return redirect ('herramienta') 

@login_required
def eliminar_mantenimiento(request, id):
    mantenimiento = get_object_or_404(MantenimientoHerramienta, id=id)
    mantenimiento.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)    

@login_required    
def detalles(request, id):
    if request.method == 'GET':
        herramienta = get_object_or_404(Herramienta, id=id)
        mantenimientos = herramienta.mantenimientoherramienta_set.all().order_by('-fecha', '-hora')
        form = HerramientaForm(instance=herramienta)
        form_mant = MantenimientoHerramientaForm()
        tipos_mantenimiento = TipoMantenimientoHerramienta.objects.all()
        context = {
            'herramienta': herramienta,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
            }
        return render(request, 'SGE_herramienta/detalles.html', context)
    
    if request.method == 'POST':
        herramienta = get_object_or_404(Herramienta, id = id)
        form_mant = MantenimientoHerramientaForm(request.POST)
        form = HerramientaForm(instance= herramienta)
        form = HerramientaForm(request.POST, request.FILES, instance= herramienta)

        if form.is_valid():
            intervalo_mantenimiento = form.cleaned_data.get('intervalo_mantenimiento')
            if intervalo_mantenimiento < 0:
                form_mant = MantenimientoHerramientaForm()
                tipos_mantenimiento = TipoMantenimientoHerramienta.objects.all()
                mantenimientos = herramienta.mantenimientoherramienta_set.all().order_by('-fecha', '-hora')
                form.add_error('intervalo_mantenimiento', 'El intervalo de mantenimiento no puede ser un número negativo')
                context = {
                    'herramienta': herramienta,
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
                form_mant = MantenimientoHerramientaForm()
                tipos_mantenimiento = TipoMantenimientoHerramienta.objects.all()
                mantenimientos = herramienta.mantenimientoherramienta_set.all().order_by('-fecha', '-hora')
                context = {
                    'herramienta': herramienta,
                    'form': form,
                    'id': id,
                    'form_mant': form_mant,
                    'mantenimientos': mantenimientos,
                    'tipos_mantenimiento': tipos_mantenimiento,
                }
                return render(request, 'SGE_herramienta/detalles.html', context) 
        
        if form_mant.is_valid():
            mantenimiento = form_mant.save(commit=False)
            mantenimiento.herramienta = herramienta
            mantenimiento.save()
            form = HerramientaForm(instance= herramienta)
            tipos_mantenimiento = TipoMantenimientoHerramienta.objects.all()
            mantenimientos = herramienta.mantenimientoherramienta_set.all().order_by('-fecha', '-hora')
            context = {
            'herramienta': herramienta,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
            }
            return render(request, 'SGE_herramienta/detalles.html', context)  
        else:
            context = {
            'herramienta': herramienta,
            'form': form,
            'id': id,
            'form_mant': form_mant,
            'mantenimientos': mantenimientos,
            'tipos_mantenimiento': tipos_mantenimiento,
            }
            return render(request, 'SGE_herramienta/detalles.html', context)             

@login_required
def generar_documento_mantenimientos_por_mes(request):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    mantenimientos = MantenimientoHerramienta.objects.filter(fecha__year=anio)

    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)

    if tipo_mantenimiento_id:  # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoHerramienta, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)

    mantenimientos = mantenimientos.order_by('-fecha', '-hora')

    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_herramientas_{}_{}.pdf"'.format(mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_herramientas_{}.pdf"'.format(anio)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Herramienta', 'Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.herramienta, mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
    else:
        data.append(['Herramienta', 'Tipo', 'Mes', 'Año', 'Dia', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.herramienta, mantenimiento.tipo, mantenimiento.fecha.month, mantenimiento.fecha.year, mantenimiento.fecha.day, mantenimiento.hora])

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
def generar_documento_mantenimientos_herramienta(request, id):
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    tipo_mantenimiento_id = request.GET.get('tipo_mantenimiento')

    herramienta = get_object_or_404(Herramienta, pk=id)
    
    mantenimientos = MantenimientoHerramienta.objects.filter(herramienta=herramienta).order_by('-fecha', '-hora')


    if mes:
        mantenimientos = mantenimientos.filter(fecha__month=mes)
    if anio:
        mantenimientos = mantenimientos.filter(fecha__year=anio)
    if tipo_mantenimiento_id:  # Si se seleccionó un tipo de mantenimiento
        tipo_mantenimiento = get_object_or_404(TipoMantenimientoHerramienta, pk=tipo_mantenimiento_id)
        mantenimientos = mantenimientos.filter(tipo=tipo_mantenimiento)


    response = HttpResponse(content_type='application/pdf')
    if mes:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_herramientas_{}_{}_{}.pdf"'.format(herramienta.nombre,mes, anio)
    else:
        response['Content-Disposition'] = 'attachment; filename="mantenimientos_herramientas_{}_{}.pdf"'.format(herramienta.nombre,anio)   

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = []
    if mes:
        data.append(['Tipo', 'Fecha', 'Hora'])
        for mantenimiento in mantenimientos:
            data.append([mantenimiento.herramienta, mantenimiento.tipo, mantenimiento.fecha, mantenimiento.hora])
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