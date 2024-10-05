from django.shortcuts import render
from Ventas.models import Factura
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
import calendar





# TODO Make index template with all the information
def indexTaxes(request):

    ingresosBrutos = calculateSales()
    IBC = calculateIBC(ingresosBrutos)
    costos = 0

    salud = calculateSalud(IBC)
    pension = calculatePension(IBC)
    cajaDeCompensacion = calculateCaja(IBC)
    ARL = 0 

    aportes = salud + pension + cajaDeCompensacion


    return render(request, 'indexTaxes.html', {'sales':ingresosBrutos, 'costos':costos, 'IBC': IBC, 'aportes':aportes, 'salud':salud, 'pension':pension, 'cajaDeCompensacion':cajaDeCompensacion, 'ARL':ARL, 'aportes':aportes })




# TODO Calculate sales
def calculateSales():
    
    sales = 0

    # Obtener la fecha actual
    fecha_actual = timezone.now()
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year
    
    # Definir los rangos bime nsuales
    if mes_actual in [1, 2]:
        inicio_rango = datetime(año_actual, 1, 1)
        # Obtener el último día de febrero según el año actual (28 o 29 días)
        fin_rango = datetime(año_actual, 2, calendar.monthrange(año_actual, 2)[1], 23, 59, 59)
    elif mes_actual in [3, 4]:
        inicio_rango = datetime(año_actual, 3, 1)
        fin_rango = datetime(año_actual, 4, 30, 23, 59, 59)
    elif mes_actual in [5, 6]:
        inicio_rango = datetime(año_actual, 5, 1)
        fin_rango = datetime(año_actual, 6, 30, 23, 59, 59)
    elif mes_actual in [7, 8]:
        inicio_rango = datetime(año_actual, 7, 1)
        fin_rango = datetime(año_actual, 8, 31, 23, 59, 59)
    elif mes_actual in [9, 10]:
        inicio_rango = datetime(año_actual, 9, 1)
        fin_rango = datetime(año_actual, 10, 31, 23, 59, 59)
    elif mes_actual in [11, 12]:
        inicio_rango = datetime(año_actual, 11, 1)
        fin_rango = datetime(año_actual, 12, 31, 23, 59, 59)

    # Filtrar facturas dentro del rango
    ventas = Factura.objects.filter(
        fecha__range=[inicio_rango, fin_rango]
    ).aggregate(sales=Sum('total_con_iva'))
    
    # Retornar el total de ventas o 0 si no hay ventas
    return ventas['sales'] if ventas['sales'] else 0
 



def calculateIBC(ingresosBrutos):

    return ingresosBrutos/100*40 #Formula para el IBC



# TODO Calculate heath
def calculateSalud(IBC):
    salud = float(IBC) / 100 * 8.5
    return salud



# TODO Calculate pesión
def calculatePension(IBC):
    pension = float(IBC) / 100 * 12
    return pension


# TODO Calculate caja de compensación familiar
def calculateCaja(IBC):
    caja = float(IBC) / 100 * 4
    return caja


# TODO Calculate nomine
def calculateNomine():
    
    nomine = 0

    return nomine 




# TODO Calculate taxes
def calculateTaxes():
    
    taxes = 0

    return taxes