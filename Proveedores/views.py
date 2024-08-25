from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProveedorForm  # Importa el formulario de Proveedores
from .forms import ReabastecimientoForm
from .models import Proveedor
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


def reabastecerProductos(request):
    if request.method == 'POST':
        form = ReabastecimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexProveedores')
    else:
        form = ReabastecimientoForm()
    
    return render(request, 'reabastecer.html', {'form': form})



