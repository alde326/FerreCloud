from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from Ventas.models import Factura, DetalleFactura


@login_required
def homeIndex(request):
    return render(request, 'dashboard.html')


def salir(request):
    logout(request)
    return redirect('/')


def dashboard_view(request):
    # Agrupar ventas por mes
    ventas_mensuales = Factura.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(total_ventas=Sum('total')).order_by('month')

    # Top 5 productos más vendidos
    productos_vendidos = DetalleFactura.objects.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')[:5]

    # Preparar los datos para JSON
    labels = [dato['month'].strftime("%b") for dato in ventas_mensuales]
    data_ventas = [dato['total_ventas'] for dato in ventas_mensuales]
    productos_top = [{'nombre': p['producto__nombre'], 'cantidad': p['total_vendido']} for p in productos_vendidos]

    return JsonResponse({
        'labels': labels,
        'data_ventas': data_ventas,
        'productos_top': productos_top,
    })
