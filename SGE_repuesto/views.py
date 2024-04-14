from django.shortcuts import render, redirect, get_object_or_404
from .models import Maquina, Parte, Inventario
from .forms import MaquinaRepuestoForm, ParteRepuestoForm, InventarioRepuestoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect

import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

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
def eliminar_inventario(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    inventario.delete()
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)    


def actualizar_inventario(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    if request.method == 'POST':
        form = InventarioRepuestoForm(request.POST, instance=inventario)
        if form.is_valid():
            form.save()
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url)
    else:
        form = InventarioRepuestoForm(instance=inventario)
    previous_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_url)

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

        action = request.POST.get('action')
        if action == 'delete':
            parte_id = request.POST.get('parte')
            parte_instance = get_object_or_404(Parte, id=parte_id)
            parte_instance.delete()
            
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

        maquina = get_object_or_404(Maquina, id=id)
        part_form = ParteRepuestoForm()
        inve_form = InventarioRepuestoForm()
        partes_maquina = Parte.objects.filter(maquina=maquina)
        context = {
            'maquina': maquina,
            'part_form': part_form,
            'partes_maquina': partes_maquina,
            'inve_form': inve_form,
        }
        return render(request, 'SGE_repuesto/detalles.html', context)  





def descargar_excel(request, id):
    maquina = get_object_or_404(Maquina, id=id)
    partes_maquina = Parte.objects.filter(maquina=maquina)

    # Crear el libro de Excel y la hoja de trabajo
    wb = Workbook()
    ws = wb.active
    ws.title = "Detalles"

    # Definir colores
    header_fill = PatternFill(start_color="FFA07A", end_color="FFA07A", fill_type="solid")

    # Escribir encabezados
    headers = ["Parte", "Tipo", "Rosca", "Largo", "Und", "Cantidad necesaria", "Existencia en stock", "Salida", "Existencia física"]
    ws.append(headers)

    # Aplicar estilo a la cabecera
    for cell in ws[1]:
        cell.fill = header_fill

    # Escribir datos de cada parte
    for parte in partes_maquina:
        inventarios = parte.inventario_set.all()
        if inventarios:
            start_row = ws.max_row + 1
            end_row = start_row + len(inventarios) - 1
            ws.cell(row=start_row, column=1, value=parte.nombre)
            ws.merge_cells(start_row=start_row, end_row=end_row, start_column=1, end_column=1)
            for i, inventario in enumerate(inventarios, start=start_row):
                row_data = [inventario.tipo, inventario.rosca, inventario.largo, inventario.und, inventario.cantidad_necesaria, inventario.existencia_stock, inventario.salida, inventario.existencia_fisica()]
                for j, value in enumerate(row_data, start=2):  # Start from column 2 to leave the first column for "Parte"
                    ws.cell(row=i, column=j, value=value)

    # Ajustar el ancho de las columnas automáticamente
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

    # Guardar el libro de Excel en un HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="detalles_maquina_{maquina.id}.xlsx"'
    wb.save(response)

    return response



