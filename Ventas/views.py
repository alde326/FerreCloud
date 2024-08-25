from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Factura, DetalleFactura
from Inventario.models import Producto
from Clientes.models import Cliente
from django.contrib import messages
import json
from decimal import Decimal

def indexVentas(request):
    productos = Producto.objects.filter(eliminado=False)
    return render(request, 'indexVentas.html', {'productos': productos})


IVA_TASA = Decimal('0.19')


def procesar_formulario(request):
    if request.method == 'POST':
        documento = request.POST.get('documento')
        email = request.POST.get('email')
        nombre = request.POST.get('nombre', '')
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion', '')
        observacion = request.POST.get('observacion', '')
        carrito = request.POST.get('carrito')
        
        carrito = json.loads(carrito)

        # Procesar el carrito y descontar los productos del inventario
        total = Decimal('0.00')
        detalles = []
        for item in carrito:
            try:
                producto = Producto.objects.get(id=item['id'])
                cantidad = Decimal(item['cantidad'])  # Convertir cantidad a Decimal
                if producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    producto.save()
                    total += producto.precio * cantidad
                    detalles.append({
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio_unitario': producto.precio
                    })
                else:
                    messages.error(request, f'No hay suficiente cantidad en inventario para el producto: {producto.nombre}')
                    return redirect('indexVentas')
            except Producto.DoesNotExist:
                messages.error(request, f'El producto con ID {item["id"]} no existe.')
                return redirect('indexVentas')

        # Calcular IVA
        iva = total * IVA_TASA
        total_con_iva = total + iva

        # Registrar al cliente
        cliente, created = Cliente.objects.get_or_create(
            documento=documento,
            defaults={
                'nombre': nombre,
                'telefono': telefono,
                'email': email,
                'direccion': direccion,
                'nivel': 0,
            }
        )

        if not created:
            messages.info(request, 'Cliente ya existente.')

        # Crear la factura
        factura = Factura.objects.create(
            cliente=cliente,
            total=total,
            iva=iva,
            total_con_iva=total_con_iva,
            observacion=observacion
        )

        # Crear los detalles de la factura
        for detalle in detalles:
            DetalleFactura.objects.create(
                factura=factura,
                producto=detalle['producto'],
                cantidad=detalle['cantidad'],
                precio_unitario=detalle['precio_unitario']
            )

        # Si todo está bien, agregar un mensaje de éxito
        messages.success(request, 'Venta realizada exitosamente y factura creada.')
        return redirect('indexVentas')

    return render(request, 'indexVentas.html')