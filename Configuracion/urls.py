from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexConfiguracion, name='indexConfiguracion'),

    path('costos/', views.indexCostos, name='indexCostos'),
    path('crearCosto/', views.crearCosto, name='crearCosto'),
    path('editar/<int:costoID>/', views.editCosto, name='editCosto'), 
    path('eliminar/<int:costoID>/', views.eliminarCosto, name='eliminarCosto'), 

    path('tipos/', views.indexTipos, name='indexTipos'),
    path('crearTipo/', views.crearTipo, name='crearTipo'),
    path('editartipo/<int:tipoID>/', views.editTipo, name='editTipo'), 
    path('eliminartipo/<int:tipoID>/', views.eliminarTipo, name='eliminarTipo'), 


    path('reporte-costos/', views.reporteCostos, name='reporteCostos'), 
]