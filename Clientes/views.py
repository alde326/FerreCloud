from django.shortcuts import render, redirect, get_object_or_404   
from .forms import ClienteForm  # Importa el formulario de cliente
from .models import Cliente
from Ventas.models import Factura


def indexClientes(request):
    clientes = Cliente.objects.filter(eliminado=False)  # Filtrar clientes que no están eliminados
    return render(request, 'indexCliente.html', {'clientes': clientes})


def crearCliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexClientes')  # Redirige a la lista de cliente
    else:
        form = ClienteForm()
    
    return render(request, 'crearCliente.html', {'form': form})


def editCliente(request, clienteID):
    cliente = get_object_or_404(Cliente, id=clienteID) 
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('indexClientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editCliente.html', {'form': form})


def eliminarCliente(request, clienteID):
    cliente = get_object_or_404(Cliente, id=clienteID)
    cliente.eliminado = True
    cliente.save()
    return redirect('indexClientes')


def comprasCliente(request, clienteID):
    cliente = get_object_or_404(Cliente, id=clienteID)
    facturas = Factura.objects.filter(cliente=cliente)
    return render(request, 'comprasCliente.html', {'cliente': cliente, 'facturas': facturas})
