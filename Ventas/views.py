#Librerías
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import F
from decimal import Decimal
from xhtml2pdf import pisa
import json

#Modelos
from Configuracion.models import Parametros
from .models import Factura, DetalleFactura
from Inventario.models import Producto
from Clientes.models import Cliente




@login_required
def indexVentas(request):
    try:
        # Verifica si el usuario tiene el permiso necesario
        if not request.user.has_perm('Inventario.view_producto'):
            raise PermissionDenied

        # Obtén el parámetro de búsqueda
        query = request.GET.get('buscar', '')
        
        # Filtra los productos que no están eliminados y que coinciden con la búsqueda
        productos = Producto.objects.filter(eliminado=False, nombre__icontains=query)

        # Obtén el parámetro de IVA como un objeto único
        try:
            iva_parametro = Parametros.objects.get(nombre="IVA")
            iva_tasa = Decimal(iva_parametro.porcentaje)
        except Parametros.DoesNotExist:
            messages.error(request, 'El parámetro IVA no está configurado.')
            return redirect('indexVentas')

        # Paginación
        paginator = Paginator(productos, 5)  # Cambia 5 por el número de productos que desees mostrar por página
        page_number = request.GET.get('page')  # Obtiene el número de página de la URL
        productos_paginados = paginator.get_page(page_number)

        return render(request, 'indexVentas.html', {
            'productos': productos_paginados,
            'iva_tasa': iva_tasa,
            'buscar': query,  # Agregar el término de búsqueda al contexto
        })

    except PermissionDenied:
        messages.error(request, 'No tienes permiso para ver esta página.')
        # Obtener la URL anterior o redirigir a 'home' si no hay URL previa
        previous_url = request.META.get('HTTP_REFERER', 'home')
        return redirect(previous_url)





def procesar_formulario(request):

    # Obtén el parámetro de IVA como un objeto único
    try:
        iva_parametro = Parametros.objects.get(nombre="IVA")
        iva_tasa = Decimal(iva_parametro.porcentaje) 
    except Parametros.DoesNotExist:
        messages.error(request, 'El parámetro IVA no está configurado.')
        return redirect('indexVentas')

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
        iva = total * iva_tasa
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

        # Construir la URL para ver la factura usando facturaID
        url_factura = reverse('verFactura', args=[factura.id])

        # Si todo está bien, agregar un mensaje de éxito con el link a la factura
        messages.success(request, f'Venta realizada exitosamente. <a href="{url_factura}">Ver factura</a>.')
        return redirect('indexVentas')

    return render(request, 'indexVentas.html')





def verFactura(request, facturaID):
    factura = get_object_or_404(Factura, id=facturaID)
    detalles = DetalleFactura.objects.filter(factura=facturaID)

    # Añadir el cálculo del total en cada detalle
    for item in detalles:
        item.total = item.cantidad * item.precio_unitario

    # Determinar si hay alguna cantidad devuelta
    hay_devolucion = any(detalle.cantidad_devuelta > 0 for detalle in detalles)

    return render(request, 'factura.html', {'factura': factura, 'detalles': detalles, 'hay_devolucion': hay_devolucion})





def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)
    return response





def verFacturaPDF(request, facturaID):
    factura = get_object_or_404(Factura, id=facturaID)
    detalles = DetalleFactura.objects.filter(factura=facturaID)

    # Añadir el cálculo del total en cada detalle
    for item in detalles:
        item.total = item.cantidad * item.precio_unitario

    # Determinar si hay alguna cantidad devuelta
    hay_devolucion = any(detalle.cantidad_devuelta > 0 for detalle in detalles)

    context = {
        'factura': factura,
        'detalles': detalles,
        'hay_devolucion': hay_devolucion
    }

    return render_to_pdf('facturaPDF.html', context)





def seleccionar_productos_devolucion(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    detalles = factura.detallefactura_set.filter(cantidad__gt=F('cantidad_devuelta'))  # Filtrar detalles no completamente devueltos

    if request.method == 'POST':
        error_ocurrido = False

        # Procesar cada detalle de la factura
        for detalle in detalles:
            cantidad_devolver_str = request.POST.get(f'cantidad_devolver_{detalle.id}', '0')
            cantidad_devolver = int(cantidad_devolver_str) if cantidad_devolver_str.isdigit() else 0
            cantidad_maxima_devolver = detalle.cantidad - detalle.cantidad_devuelta

            if cantidad_devolver > 0:
                if cantidad_devolver > cantidad_maxima_devolver:
                    messages.error(request, f'No puedes devolver más de {cantidad_maxima_devolver} unidades del producto "{detalle.producto.nombre}".')
                    error_ocurrido = True
                else:
                    # Actualizar el stock del producto y la cantidad devuelta en el detalle
                    producto = detalle.producto
                    producto.cantidad += cantidad_devolver
                    producto.save()

                    # Actualizar la cantidad devuelta en el detalle
                    detalle.cantidad_devuelta += cantidad_devolver
                    detalle.save()

        if not error_ocurrido:
            messages.success(request, 'Los productos seleccionados han sido devueltos y el stock actualizado.')
            return redirect('verFactura', facturaID=factura_id)

    # Calcular la cantidad máxima que se puede devolver para cada detalle
    detalles_con_max_devolucion = [
        {
            'detalle': detalle,
            'cantidad_maxima_devolver': detalle.cantidad - detalle.cantidad_devuelta
        }
        for detalle in detalles
    ]

    return render(request, 'devolucion.html', {'factura': factura, 'detalles': detalles_con_max_devolucion})


    