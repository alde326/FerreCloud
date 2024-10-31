#Librerías
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, F
from django.db.models import Q

import calendar
import json

#Modelos
from .models import Costos, Tipos, Parametros, Organizacion
from Ventas.models import Factura, DetalleFactura

#Forms
from .forms import CostosForm, TipoForm, ParametroForm, OrganizacionForm, ReporteVentasForm





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

    # Obtener los parámetros de búsqueda y filtro
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    tipo = request.GET.get('tipo')
    busqueda = request.GET.get('busqueda')  # Nuevo parámetro de búsqueda

    # Filtrar por fecha
    if fecha_inicio and fecha_fin:
        costos = costos.filter(fecha__range=[fecha_inicio, fecha_fin])

    # Filtrar por tipo
    if tipo:
        costos = costos.filter(tipo__id=tipo)

    # Filtrar por búsqueda (nombre o descripción)
    if busqueda:
        costos = costos.filter(Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda))

    # Obtener los tipos para el filtro
    tipos = Tipos.objects.filter(eliminado=False)

    return render(request, 'indexCostos.html', {'costos': costos, 'tipos': tipos})







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
    costos = Costos.objects.filter(eliminado=False, ingreso_egreso=False)

    # Resumen de costos por tipo
    costos_por_tipo = costos.values('tipo__nombre').annotate(total=Sum('valor'))

    # Resumen de costos por mes
    costos_por_mes = costos.filter(fecha__gte=start_of_month).values('fecha__month').annotate(total=Sum('valor'))

    # Crear un diccionario para los costos por mes
    costos_mensuales = {calendar.month_name[i]: 0 for i in range(1, 13)}
    for costo in costos_por_mes:
        costos_mensuales[calendar.month_name[costo['fecha__month']]] = float(costo['total'])

    # Obtener ingresos
    ingresos = Costos.objects.filter(eliminado=False, ingreso_egreso=True)

    # Resumen de ingresos por tipo
    ingresos_por_tipo = ingresos.values('tipo__nombre').annotate(total=Sum('valor'))

    # Resumen de ingresos por mes
    ingresos_por_mes = ingresos.filter(fecha__gte=start_of_month).values('fecha__month').annotate(total=Sum('valor'))

    # Crear un diccionario para los ingresos por mes
    ingresos_mensuales = {calendar.month_name[i]: 0 for i in range(1, 13)}
    for ingreso in ingresos_por_mes:
        ingresos_mensuales[calendar.month_name[ingreso['fecha__month']]] = float(ingreso['total'])

    # Calcular totales
    total_costos = costos.aggregate(total=Sum('valor'))['total'] or 0
    total_ingresos = ingresos.aggregate(total=Sum('valor'))['total'] or 0
    ganancia_perdida = total_ingresos - total_costos

    # Crear un diccionario para comparar ingresos y costos
    comparacion_mensual = {
        'mes': [],
        'ingresos': [],
        'costos': []
    }

    for month in calendar.month_name[1:]:
        comparacion_mensual['mes'].append(month)
        comparacion_mensual['ingresos'].append(ingresos_mensuales[month])
        comparacion_mensual['costos'].append(costos_mensuales[month])

    # Convertir los datos a JSON
    costos_por_tipo_json = json.dumps([
        {'tipo__nombre': tipo['tipo__nombre'], 'total': float(tipo['total'])}
        for tipo in costos_por_tipo
    ])
    costos_mensuales_json = json.dumps(costos_mensuales)
    ingresos_por_tipo_json = json.dumps([
        {'tipo__nombre': tipo['tipo__nombre'], 'total': float(tipo['total'])}
        for tipo in ingresos_por_tipo
    ])
    ingresos_mensuales_json = json.dumps(ingresos_mensuales)
    comparacion_mensual_json = json.dumps(comparacion_mensual)

    context = {
        'costos': costos,
        'ingresos': ingresos,
        'total_costos': total_costos,
        'total_ingresos': total_ingresos,
        'ganancia_perdida': ganancia_perdida,
        'costos_por_tipo_json': costos_por_tipo_json,
        'costos_mensuales_json': costos_mensuales_json,
        'ingresos_por_tipo_json': ingresos_por_tipo_json,
        'ingresos_mensuales_json': ingresos_mensuales_json,
        'comparacion_mensual_json': comparacion_mensual_json,  # Agregar comparación
    }
    
    return render(request, 'analisisDeGastos.html', context)





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




def editOrganizacion(request):
    organizacion = get_object_or_404(Organizacion, id=1)
    if request.method == "POST":
        form = OrganizacionForm(request.POST, instance=organizacion)
        if form.is_valid():
            form.save()
            return redirect('indexOrganizacion')
    else:
        form = OrganizacionForm(instance=organizacion)
    return render(request, 'editOrganizacion.html', {'form': form})


#-------------------------------------REPORTES--------------------------------------------------

def indexReportes(request):
    return render(request, 'indexReportes.html')




def reporte_ventas(request):
    form = ReporteVentasForm(request.GET or None)
    facturas = Factura.objects.all()
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            facturas = facturas.filter(fecha__range=[fecha_inicio, fecha_fin])

    # Resumen de ventas
    total_vendido = facturas.aggregate(Sum('total'))['total__sum'] or 0
    total_iva = facturas.aggregate(Sum('iva'))['iva__sum'] or 0
    total_facturas = facturas.count()

    # Detalles de productos vendidos
    detalles = DetalleFactura.objects.filter(factura__in=facturas).values('producto__nombre').annotate(
    total_vendido=Sum('cantidad'),
    total_precio=Sum(F('precio_unitario') * F('cantidad'))
    )

    context = {
        'form': form,
        'total_vendido': total_vendido,
        'total_iva': total_iva,
        'total_facturas': total_facturas,
        'detalles': detalles,
    }
    
    return render(request, 'reporteDeVentas.html', context)