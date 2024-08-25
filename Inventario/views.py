from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Producto
from django.db.models import Q


def indexInventarios(request):
    productos = Producto.objects.filter(eliminado=False).exclude(cantidad=0)
    return render(request, 'indexInventarios.html', {'productos': productos})


def newProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexInventarios')   # Redirige a la lista de empleados
    else:
        form = ProductForm()
    
    return render(request, 'newProduct.html', {'form': form})


def eliminarProducto(request, productoID):
    producto = get_object_or_404(Producto, id=productoID)
    producto.eliminado = True
    producto.save()
    return redirect('indexProveedor')


def product_search(request):
    query = request.GET.get('query', '')
    presentacion = request.GET.get('presentacion', '')
    proveedor = request.GET.get('proveedor', '')
    order_by = request.GET.get('order_by', '')

    filters = Q()
    
    if query:
        filters &= Q(nombre__icontains=query)
    if presentacion:
        filters &= Q(presentacion__icontains=presentacion)
    if proveedor:
        filters &= Q(proveedor__icontains=proveedor)
    
    productos = Producto.objects.filter(filters)
    
    if order_by:
        productos = productos.order_by(order_by)
    
    return render(request, 'indexInventarios.html', {'productos': productos})



def edit_product(request, product_id):
    producto = get_object_or_404(Producto, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Cambia esto a la URL de la lista de productos
    else:
        form = ProductForm(instance=producto)
    return render(request, 'editProduct.html', {'form': form})
