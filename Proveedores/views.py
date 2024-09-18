from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ProveedorForm, ReabastecimientoForm, ReabastecimientoDetalleFormSet
from .models import Proveedor, Reabastecimiento, Producto
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




def crearReabastecimiento(request):
    productos = list(Producto.objects.values('id', 'nombre'))  # Convertir a una lista de diccionarios
    if request.method == 'POST':
        form = ReabastecimientoForm(request.POST)

        print(request.POST)

        if form.is_valid():
            # Ahora que el formulario es válido, podemos acceder a cleaned_data
            formset = ReabastecimientoDetalleFormSet(request.POST, instance=form.instance, form_kwargs={'proveedor': form.cleaned_data.get('proveedor')})
            
            if formset.is_valid():
                reabastecimiento = form.save()
                #Aquí procesar los nuevos datos del formulario
                for detalle_form in formset:
                    detalle = detalle_form.save(commit=False)
                    detalle.reabastecimiento = reabastecimiento
                    detalle.save()
                return JsonResponse({'success': True, 'redirect_url': 'http://127.0.0.1:8000/proveedor/'})  #Cambiar la ruta de redirección
        else:
            # Si el formulario principal no es válido, crea el formset sin datos
            formset = ReabastecimientoDetalleFormSet(form_kwargs={'proveedor': None})
    
    else:
        form = ReabastecimientoForm()
        formset = ReabastecimientoDetalleFormSet(form_kwargs={'proveedor': None})
    
    return render(request, 'crearReabastecimiento.html', {
        'form': form, 
        'formset': formset,
        'productos': json.dumps(productos)  # Serialización a JSON
    })





