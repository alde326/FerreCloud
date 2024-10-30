from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from Ventas.models import Factura, DetalleFactura
from django.shortcuts import render, redirect
from Configuracion.models import Costos
from django.contrib.auth import logout
from collections import OrderedDict
from django.db.models import Sum
from datetime import datetime
import calendar



@login_required
def homeIndex(request):
    # Cálculo de productos más vendidos
    productos_mas_vendidos = (DetalleFactura.objects
                              .values('producto__nombre')
                              .annotate(cantidad_vendida=Sum('cantidad'))
                              .order_by('-cantidad_vendida')[:5])
    
     # Datos para el gráfico de ventas mensuales
    ventas_mensuales = (Factura.objects
                        .annotate(mes=TruncMonth('fecha'))
                        .values('mes')
                        .annotate(total_ventas=Sum('total_con_iva'))
                        .order_by('mes'))

    # Preparar los datos para Chart.js
    ventas_por_mes = OrderedDict()
    for i in range(1, 13):  # Inicializa el diccionario con los meses del año
        ventas_por_mes[i] = 0

    for venta in ventas_mensuales:
        mes = venta['mes'].month
        ventas_por_mes[mes] = float(venta['total_ventas'])

    # Nombres de los meses y sus respectivos totales
    meses_nombres = [calendar.month_name[i] for i in ventas_por_mes.keys()]
    ventas_totales = list(ventas_por_mes.values())

    # KPIs de facturación
    ingresos_totales = Factura.objects.aggregate(total_ingresos=Sum('total_con_iva'))['total_ingresos'] or 0
    numero_facturas = Factura.objects.count()
    facturas_electronicas = Factura.objects.filter(pagoElectronico=True).count()
    facturas_efectivo = numero_facturas - facturas_electronicas

    # KPIs de costos
    costos_totales = Costos.objects.aggregate(total_costos=Sum('valor'))['total_costos'] or 0
    costos_por_tipo = Costos.objects.values('tipo__nombre').annotate(total_por_tipo=Sum('valor'))

    # Calcular ganancia neta
    ganancias_netas = ingresos_totales - costos_totales

    # Extraer tipos y valores para los gráficos
    tipos_costos = [costo['tipo__nombre'] for costo in costos_por_tipo]
    valores_costos = [float(costo['total_por_tipo']) for costo in costos_por_tipo]

    context = {
        'ingresos_totales': ingresos_totales,
        'numero_facturas': numero_facturas,
        'facturas_electronicas': facturas_electronicas,
        'facturas_efectivo': facturas_efectivo,
        'costos_totales': costos_totales,
        'costos_por_tipo': costos_por_tipo,
        'ganancias_netas': ganancias_netas,
        'tipos_costos': tipos_costos,
        'valores_costos': valores_costos,
        'productos_mas_vendidos': productos_mas_vendidos,
        'meses_nombres': meses_nombres,
        'ventas_totales': ventas_totales,
    }
    return render(request, 'dashboard.html', context)


def salir(request):
    logout(request)
    return redirect('/')


