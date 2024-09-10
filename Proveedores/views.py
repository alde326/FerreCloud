from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProveedorForm, ReabastecimientoForm, ReabastecimientoDetalleFormSet
from .models import Proveedor, Reabastecimiento
from django.contrib.auth.decorators import login_required

@login_required
def indexProveedores(request):
    proveedores = Proveedor.objects.filter(eliminado=False)
    return render(request, 'indexProveedor.html', {'proveedores': proveedores})


def crearProveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexProveedores')   # Redirige a la lista de proveedores
    else:
        form = ProveedorForm()
    
    return render(request, 'crearProveedor.html', {'form': form})


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


def eliminarProveedor(request, proveedorID):
    proveedores = get_object_or_404(Proveedor, id=proveedorID)
    proveedores.eliminado = True
    proveedores.save()
    return redirect('indexInventarios')


def indexOrdenes(request):
    ordenes = Reabastecimiento.objects.filter(eliminado=False)
    return render(request, 'indexOrdenes.html', {'ordenes': ordenes})


def crearReabastecimiento(request):
    if request.method == 'POST':
        form = ReabastecimientoForm(request.POST)
        if form.is_valid():
            proveedor = form.cleaned_data.get('proveedor')
            formset = ReabastecimientoDetalleFormSet(request.POST, instance=form.instance, form_kwargs={'proveedor': proveedor})
            if formset.is_valid():
                reabastecimiento = form.save()
                detalles = formset.save(commit=False)
                for detalle in detalles:
                    detalle.reabastecimiento_id = reabastecimiento
                    detalle.save()
                return redirect('indexOrdenes')
    else:
        form = ReabastecimientoForm()
        formset = ReabastecimientoDetalleFormSet(form_kwargs={'proveedor': None})
    
    return render(request, 'crearReabastecimiento.html', {'form': form, 'formset': formset})


