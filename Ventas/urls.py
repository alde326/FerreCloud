from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexVentas, name='indexVentas'), 
    path('procesar_formulario/', views.procesar_formulario, name='procesar_formulario'),
]