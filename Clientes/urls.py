from django.urls import path
from . import views
from Ventas.views import verFactura


urlpatterns = [
    path('', views.indexClientes, name='indexClientes'),
    path('crearCliente/', views.crearCliente, name='crearCliente'),
    path('editar/<int:clienteID>/', views.editCliente, name='editCliente'),
    path('eliminar/<int:clienteID>/', views.eliminarCliente, name='eliminarCliente'),
    path('compras/<int:clienteID>/', views.comprasCliente, name='comprasCliente'),
    path('fatura/<int:facturaID>/', verFactura, name='verFactura'),
]