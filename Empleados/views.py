from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmpleadoForm  # Importa el formulario de empleado
from .models import Empleado
from django.contrib.auth import authenticate, login


def indexEmpleados(request):
    empleados = Empleado.objects.filter(eliminado=False)
    return render(request, 'indexEmpleados.html', {'empleados': empleados})


def crearEmpleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
           
            return redirect('indexEmpleados')   # Redirige a la lista de empleados
    else:
        form = EmpleadoForm()
    return render(request, 'crearEmpleado.html', {'form': form})

def editEmpleado(request, empleadoID):
    empleado = get_object_or_404(Empleado, id=empleadoID)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('indexEmpleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'editEmpleado.html', {'form': form})


def eliminarEmpleado(request, empleadoID):
    empleados = get_object_or_404(Empleado, id=empleadoID)
    empleados.eliminado = True
    empleados.save()
    return redirect('indexEmpleados')
