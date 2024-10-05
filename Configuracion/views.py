from django.shortcuts import render, redirect, get_object_or_404
from .models import Costos
from .forms import CostosForm




def indexConfiguracion(request):
    return render(request, 'indexConfiguracion.html')


#COSTOS---------------------------


def indexCostos(request):
    costos = Costos.objects.filter(eliminado=False)
    return render(request, 'indexCostos.html',{'costos': costos})


def crearCosto(request):
    if request.method == 'POST':
        form = CostosForm(request.POST)
        if form.is_valid():
            nuevo_costo = form.save()

            return redirect('indexCostos')   # Redirige a la lista de costos
    else:
        form = CostosForm()
    return render(request, 'crearCosto.html', {'form': form})



def editCosto(request, costoID):
    costo = get_object_or_404(Costos, id=costoID)
    if request.method == "POST":
        form = CostosForm(request.POST, instance=costo)
        if form.is_valid():
            costo_actualizado = form.save()
            
            return redirect('indexCostos')
    else:
        form = CostosForm(instance=costo)
    return render(request, 'editCosto.html', {'form': form})



def eliminarCosto(request, costoID):
    costo = get_object_or_404(Costos, id=costoID)
    costo.eliminado = True
    costo.save()
    return redirect('indexCostos')