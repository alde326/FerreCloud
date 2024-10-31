#Librerías
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
import calendar

#Modelos
from Empleados.models import Empleado
from Ventas.models import Factura
from Configuracion.models import Costos
from Configuracion.models import Parametros






def index(request):
    try:
        # Verifica si el usuario tiene el permiso necesario
        if not request.user.has_perm('Impuestos.view_parametros'):
            raise PermissionDenied

        return render(request, 'indexinitialTaxes.html')
    
    except PermissionDenied:
        messages.error(request, 'No tienes permiso para ver esta página.')
        # Obtener la URL anterior o redirigir a 'home' si no hay URL previa
        previous_url = request.META.get('HTTP_REFERER', 'home')
        return redirect(previous_url)





# TODO Make index template with all the information
def indexTaxes(request):
    if request.method == 'POST':
        bimestre = int(request.POST.get('bimestre', 0))  # Obtener el bimestre del formulario

        # Obtener el rango bimensual basado en el bimestre
        inicio_rango, fin_rango = get_bimonthly_range(bimestre)

        #Tasas
        # Lista de nombres de parámetros
        nombres_parametros = ["IBC", "Salud", "Pensión", "Caja", "ARL", "ICA"]

        # Diccionario para almacenar las tasas
        tasas = {}

        # Obtener tasas usando un bucle
        for nombre in nombres_parametros:
            parametro = Parametros.objects.get(nombre=nombre)
            tasas[nombre] = Decimal(parametro.porcentaje)


        # Calcular las ventas y otros valores para el rango seleccionado
        ingresosBrutos = calculateSales(inicio_rango, fin_rango)
        nomina = calculateNomine()
        IBC = calculateIBC(ingresosBrutos, tasas["IBC"])
        costos = calculateCostos(inicio_rango, fin_rango)

        ingresosDepurados = ingresosBrutos - costos

        # Calculo de prestaciones sociales
        salud = calculateSalud(nomina, tasas["Salud"])
        pension = calculatePension(nomina, tasas["Pensión"])
        cajaDeCompensacion = calculateCaja(nomina, tasas["Caja"])
        ARL = calculateARL(nomina, tasas["ARL"]) 
        aportes = salud + pension + cajaDeCompensacion + ARL


        INCRNGO = calculateINCRNGO(inicio_rango, fin_rango)
        ICA = calculateICA(inicio_rango, fin_rango, ingresosBrutos, tasas["ICA"])


        return render(request, 'indexTaxes.html', {
            'sales': ingresosBrutos, 
            'costos': costos,
            'IBC': IBC,
            'ingresosDepurados': ingresosDepurados,

            #Seguridad social
            'aportes': aportes,
            'salud': salud, 
            'pension': pension, 
            'cajaDeCompensacion': cajaDeCompensacion, 
            'ARL': ARL, 
            #Tasas
            'tasas':tasas,

            'ICA':ICA,
            'INCRNGO': INCRNGO,   
        })
    else:
        # Manejo de método GET si es necesario
        return render(request, 'indexinitialTaxes.html')




def get_bimonthly_range(bimestre):
    año_actual = timezone.now().year
    
    # Definir los rangos bimensuales
    if bimestre == 1:
        inicio_rango = datetime(año_actual, 1, 1)
        fin_rango = datetime(año_actual, 2, calendar.monthrange(año_actual, 2)[1], 23, 59, 59)
    elif bimestre == 2:
        inicio_rango = datetime(año_actual, 3, 1)
        fin_rango = datetime(año_actual, 4, 30, 23, 59, 59)
    elif bimestre == 3:
        inicio_rango = datetime(año_actual, 5, 1)
        fin_rango = datetime(año_actual, 6, 30, 23, 59, 59)
    elif bimestre == 4:
        inicio_rango = datetime(año_actual, 7, 1)
        fin_rango = datetime(año_actual, 8, 31, 23, 59, 59)
    elif bimestre == 5:
        inicio_rango = datetime(año_actual, 9, 1)
        fin_rango = datetime(año_actual, 10, 31, 23, 59, 59)
    elif bimestre == 6:
        inicio_rango = datetime(año_actual, 11, 1)
        fin_rango = datetime(año_actual, 12, 31, 23, 59, 59)
    else:
        raise ValueError("Bimestre inválido")

    return inicio_rango, fin_rango






def calculateSales(inicio_rango, fin_rango):
    # Filtrar facturas dentro del rango
    ventas = Factura.objects.filter(
        fecha__range=[inicio_rango, fin_rango]
    ).aggregate(sales=Sum('total_con_iva'))
    
    return ventas['sales'] if ventas['sales'] else 0
 




def calculateIBC(ingresosBrutos, tasa):
    return ingresosBrutos * tasa #Formula para el IBC





# TODO Calculate heath
def calculateSalud(nomina, tasa):
    return Decimal(nomina) * tasa





# TODO Calculate pesión
def calculatePension(nomina, tasa):
    return Decimal(nomina) * tasa





# TODO Calculate caja de compensación familiar
def calculateCaja(nomina, tasa):
    return Decimal(nomina) * tasa





def calculateARL(nomina, tasa):
    return Decimal(nomina) * tasa





def calculateICA(inicio_rango, fin_rango, sales, tasa):
    return 0





# TODO Calculate nomine
def calculateNomine():
    nomine = Empleado.objects.filter(eliminado=False).aggregate(Sum('salario'))
    return nomine['salario__sum'] or 0  # Devuelve 0 si no hay empleados





def calculateCostos(inicio_rango, fin_rango):
    costos = Costos.objects.filter(
        fecha__range=[inicio_rango, fin_rango]
    ).exclude(tipo_id=4).aggregate(valorcitos=Sum('valor'))
    
    return costos['valorcitos'] if costos['valorcitos'] else 0





def calculateINCRNGO(inicio_rango, fin_rango):
    costos = Costos.objects.filter(
        fecha__range=[inicio_rango, fin_rango],
        tipo_id=4
    ).aggregate(valorcitos=Sum('valor'))
    
    return costos['valorcitos'] if costos['valorcitos'] else 0





# TODO Calculate taxes
def calculateTaxes():
    
    taxes = 0

    return taxes