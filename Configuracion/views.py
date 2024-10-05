from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg
from django.utils.dateparse import parse_date
from django.http import JsonResponse
import json
from .models import Costos, Tipos
from .forms import CostosForm, TipoForm




def indexConfiguracion(request):
    return render(request, 'indexConfiguracion.html')


#COSTOS---------------------------


def indexCostos(request):
    costos = Costos.objects.filter(eliminado=False)
    
    # Obtener los parámetros de fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    tipo = request.GET.get('tipo')
    
    if fecha_inicio and fecha_fin:
        costos = costos.filter(fecha__range=[fecha_inicio, fecha_fin])
    
    if tipo:
        costos = costos.filter(tipo__id=tipo)


    return render(request, 'indexCostos.html', {'costos': costos})




def crearCosto(request):
    if request.method == 'POST':
        form = CostosForm(request.POST)
        if form.is_valid():
            nuevo_costo = form.save()

            return redirect('indexCostos')   # Redirige a la lista de costos
    else:
        form = CostosForm()
    return render(request, 'crearCosto.html', {'form': form})




def editCosto(request, costoID):
    costo = get_object_or_404(Costos, id=costoID)
    if request.method == "POST":
        form = CostosForm(request.POST, instance=costo)
        if form.is_valid():
            costo_actualizado = form.save()
            
            return redirect('indexCostos')
    else:
        form = CostosForm(instance=costo)
    return render(request, 'editCosto.html', {'form': form})



def eliminarCosto(request, costoID):
    costo = get_object_or_404(Costos, id=costoID)
    costo.eliminado = True
    costo.save()
    return redirect('indexCostos')




def indexTipos(request):
    tipos = Tipos.objects.filter(eliminado=False)
    return render(request, 'indexTipos.html', {'tipos': tipos})




def crearTipo(request):
    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            nuevo_costo = form.save()

            return redirect('indexTipos')   # Redirige a la lista de costos
    else:
        form = TipoForm()
    return render(request, 'crearTipo.html', {'form': form})




def editTipo(request, tipoID):
    tipo = get_object_or_404(Tipos, id=tipoID)
    if request.method == "POST":
        form = TipoForm(request.POST, instance=tipo)
        if form.is_valid():
            tipo_actualizado = form.save()
            
            return redirect('indexTipos')
    else:
        form = TipoForm(instance=tipo)
    return render(request, 'editTipo.html', {'form': form})




def eliminarTipo(request, tipoID):
    tipo = get_object_or_404(Tipos, id=tipoID)
    tipo.eliminado = True
    tipo.save()
    return redirect('indexTipos')




def reporteCostos(request):
    # Inicializamos el queryset con los costos no eliminados
    costos = Costos.objects.filter(eliminado=False)

    # Filtros por fechas
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        costos = costos.filter(fecha__range=[fecha_inicio, fecha_fin])

    # Calcular estadísticas de los costos filtrados
    total_costos = costos.aggregate(total=Sum('valor'))
    promedio_costos = costos.aggregate(promedio=Avg('valor'))

    # Preparar datos para el gráfico
    fechas = costos.values_list('fecha', flat=True)
    valores = costos.values_list('valor', flat=True)

    context = {
        'costos': costos,
        'total_costos': total_costos,
        'promedio_costos': promedio_costos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'fechas': json.dumps(list(fechas)),
        'valores': json.dumps(list(valores)),
    }

    return render(request, 'reporteCostos.html', context)