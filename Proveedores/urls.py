from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.indexProveedores, name='indexProveedores'),
    path('crearProveedor/', views.crearProveedor, name='crearProveedor'),
    path('editar/<int:proveedorID>/', views.editProveedor, name='editProveedor'),
    path('eliminar/<int:proveedorID>/', views.eliminarProveedor, name='eliminarProveedor'),
    path('reabastecerProductos/', views.reabastecerProductos, name='reabastecerProductos'),

]