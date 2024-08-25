from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexInventarios, name='indexInventarios'), 
    path('newProduct', views.newProduct, name='newProduct'), 
    path('eliminar/<int:productoID>/', views.eliminarProducto, name='eliminarProducto'),
    path('buscar/', views.product_search, name='product_search'),
    path('editar/<int:product_id>/', views.edit_product, name='edit_product'),

]