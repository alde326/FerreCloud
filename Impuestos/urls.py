from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexTaxes, name='indexTaxes'),
]