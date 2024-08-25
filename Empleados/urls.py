from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexEmpleados, name='indexEmpleados'),
    path('crearEmpleado/', views.crearEmpleado, name='crearEmpleado'),
    path('editar/<int:empleadoID>/', views.editEmpleado, name='editEmpleado'),
    path('eliminar/<int:empleadoID>/', views.eliminarEmpleado, name='eliminarEmpleado'),


]