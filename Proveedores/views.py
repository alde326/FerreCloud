from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProveedorForm, ReabastecimientoForm, ReabastecimientoDetalleFormSet
from .models import Proveedor, Reabastecimiento, Producto, ReabastecimientoDetalle
import json

#Muestra el template de la lista de proveedores
@login_required
def indexProveedores(request):
    proveedores = Proveedor.objects.filter(eliminado=False)
    return render(request, 'indexProveedor.html', {'proveedores': proveedores})


#Formulario de creación de proveedores
def crearProveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexProveedores')   # Redirige a la lista de proveedores
    else:
        form = ProveedorForm()
    
    return render(request, 'crearProveedor.html', {'form': form})


#Formulario de edición de proveedores
def editProveedor(request, proveedorID):
    proveedor = get_object_or_404(Proveedor, id=proveedorID)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('indexProveedor')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editProveedor.html', {'form': form})


#Eliminación lógica de los proveedores
def eliminarProveedor(request, proveedorID):
    proveedores = get_object_or_404(Proveedor, id=proveedorID)
    proveedores.eliminado = True
    proveedores.save()
    return redirect('indexInventarios')


#Muestra las ordenes de compra generadas
def indexOrdenes(request):
    ordenes = Reabastecimiento.objects.filter(eliminado=False)
    return render(request, 'indexOrdenes.html', {'ordenes': ordenes})




@csrf_exempt
def crearReabastecimiento(request):
    productos = list(Producto.objects.values('id', 'nombre'))  # Lista de productos para el formulario

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proveedor = data.get('proveedor')
            fecha_esperada = data.get('fechaEsperada')
            credito = data.get('credito')
            observaciones = data.get('observaciones')
            detalles = data.get('detalles')

            # Crear la instancia de Reabastecimiento
            reabastecimiento = Reabastecimiento.objects.create(
                proveedor_id=proveedor,
                fechaEsperada=fecha_esperada,
                credito=credito,
                observaciones=observaciones
            )

            # Guardar los detalles
            for detalle in detalles:
                ReabastecimientoDetalle.objects.create(
                    reabastecimiento=reabastecimiento,
                    producto_id=detalle['producto'],
                    cantidad=detalle['cantidad'],
                    observaciones=detalle.get('observaciones', '')
                )

            return JsonResponse({'success': True, 'redirect_url': 'http://127.0.0.1:8000/proveedor/'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    else:
        form = ReabastecimientoForm()
        return render(request, 'crearReabastecimiento.html', {
            'form': form,
            'productos': json.dumps(productos)
        })





