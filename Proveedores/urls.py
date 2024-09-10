from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.indexOrdenes, name='indexOrdenes'),
    path('crearProveedor/', views.crearProveedor, name='crearProveedor'),
    path('editar/<int:proveedorID>/', views.editProveedor, name='editProveedor'),
    path('eliminar/<int:proveedorID>/', views.eliminarProveedor, name='eliminarProveedor'),
    path('proveedores/', views.indexProveedores, name='indexProveedores'),
    path('crear-reabastecimiento/', views.crearReabastecimiento, name='crearReabastecimiento'),

]