#Librerías
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
import calendar
import json

#Modelos
from .models import Costos, Tipos, Parametros, Organizacion

#Forms
from .forms import CostosForm, TipoForm, ParametroForm





def indexConfiguracion(request):
    try:
        if not request.user.has_perm('Configuracion.view_costos'):
            raise PermissionDenied
        return render(request, 'indexConfiguracion.html')
    except PermissionDenied:
        messages.error(request, 'No tienes permiso para ver esta página.')
        # Obtener la URL anterior o redirigir a 'home' si no hay URL previa
        previous_url = request.META.get('HTTP_REFERER', 'home')
        return redirect(previous_url)


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




def analisis_costos(request):
    # Obtener la fecha actual y calcular el primer día del mes
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Obtener todos los costos no eliminados
    costos = Costos.objects.filter(eliminado=False)

    # Resumen de costos por tipo
    costos_por_tipo = costos.values('tipo__nombre').annotate(total=Sum('valor'))

    # Resumen de costos por mes
    costos_por_mes = costos.filter(fecha__gte=start_of_month).values('fecha__month').annotate(total=Sum('valor'))

    # Crear un diccionario para los costos por mes
    costos_mensuales = {calendar.month_name[i]: 0 for i in range(1, 13)}
    for costo in costos_por_mes:
        costos_mensuales[calendar.month_name[costo['fecha__month']]] = float(costo['total'])

    # Convertir los datos a JSON, asegurándonos de que los valores sean flotantes
    costos_por_tipo_json = json.dumps([
        {'tipo__nombre': tipo['tipo__nombre'], 'total': float(tipo['total'])}
        for tipo in costos_por_tipo
    ])
    costos_mensuales_json = json.dumps(costos_mensuales)

    context = {
        'costos': costos,
        'costos_por_tipo_json': costos_por_tipo_json,
        'costos_mensuales_json': costos_mensuales_json,
    }
    
    
    return render(request, 'analisis.html', context)



#Parametrización--------------------------------------------------------------------------

def indexParametrizacion(request):
    return render(request, 'indexParametrizacion.html')




def indexParametros(request):
    parametros = Parametros.objects.filter(eliminado=False)
    return render(request, 'indexParametros.html', {'parametros':parametros})




def crearParametro(request):
    if request.method == 'POST':
        form = ParametroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexParametros')   # Redirige a la lista de parametros
    else:
        form = ParametroForm()
    return render(request, 'crearParametro.html', {'form': form})




def editParametro(request, parametroID):
    parametro = get_object_or_404(Parametros, id=parametroID)
    if request.method == "POST":
        form = ParametroForm(request.POST, instance=parametro)
        if form.is_valid():
            form.save()
            return redirect('indexParametros')
    else:
        form = ParametroForm(instance=parametro)
    return render(request, 'editParametro.html', {'form': form})




def eliminarParametro(request, parametroID):
    parametro = get_object_or_404(Parametros, id=parametroID)
    parametro.eliminado = True
    parametro.save()
    return redirect('indexParametros')


#Organización--------------------------------------------------------------

def indexOrganizacion(request):
    organizacion = Organizacion.objects.get()
    return render(request, 'indexOrganizacion.html', {'parametros':organizacion})

