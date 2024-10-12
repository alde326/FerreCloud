#Librerías
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.contrib import messages

#Forms
from .forms import EmpleadoForm

#Modelos
from .models import Empleado






def indexEmpleados(request):
    try:
        if not request.user.has_perm('Empleados.view_empleado'):
            raise PermissionDenied
        empleados = Empleado.objects.filter(eliminado=False)
        return render(request, 'indexEmpleados.html', {'empleados': empleados})
    except PermissionDenied:
        messages.error(request, 'No tienes permiso para ver esta página.')
        # Obtener la URL anterior
        previous_url = request.META.get('HTTP_REFERER', 'home')  # 'home' es un fallback en caso de que no haya URL previa
        return redirect(previous_url)




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
