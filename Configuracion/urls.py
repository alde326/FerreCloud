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


    path('reporte-costos/', views.analisis_costos, name='reporteCostos'), 
    


    path('parametrizacion/', views.indexParametrizacion, name='indexParametrizacion'),

    path('parametros/', views.indexParametros, name='indexParametros'),
    path('crearParametro/', views.crearParametro, name='crearParametro'),
    path('editarParametro/<int:parametroID>/', views.editParametro, name='editParametro'), 
    path('eliminarParametro/<int:parametroID>/', views.eliminarParametro, name='eliminarParametro'), 


    path('organizacion/', views.indexOrganizacion, name='indexOrganizacion'),
    path('editarOrganizacion/', views.editOrganizacion, name='editOrganizacion'),

    path('reportes/', views.indexReportes, name='indexReportes'),
    path('reporte-ventas/', views.reporte_ventas, name='reporte_ventas'),

]