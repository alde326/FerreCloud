from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Producto
from Proveedores.models import Proveedor
from .forms import ProductForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class InventariosViewsTestCase(TestCase):
    
    def setUp(self):
       # Crear usuario para pruebas
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_with_permission = User.objects.create_user(username='adminuser', password='12345')

        # Obtener el permiso adecuado
        content_type = ContentType.objects.get_for_model(Producto)
        permission = Permission.objects.get(codename='view_producto', content_type=content_type)
        
        # Asignar el permiso al usuario
        self.user_with_permission.user_permissions.add(permission)

        # Crear un proveedor para las pruebas
        self.proveedor = Proveedor.objects.create(
            nit='123456789',
            razonSolcial='Proveedor A',
            telefono='5551234',
            email='contacto@proveedora.com',
            nombreContacto='Juan Perez',
            celular='3216549870'
        )
        
        # Crear un producto para las pruebas
        self.product = Producto.objects.create(
            nombre='Producto 1', 
            cantidad=10, 
            proveedor=self.proveedor,  # Asocia el producto con el proveedor creado
            eliminado=False
        )

    def run(self, result=None):
        # Sobrescribimos el método run para agregar el mensaje "OK" por cada test
        result = super().run(result)
        if result.wasSuccessful():
            print(f"{self._testMethodName}: OK")
        return result
    
    def test_index_inventarios_permission_denied(self):
        # Intentar acceder a la vista sin el permiso adecuado
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('indexInventarios'))
        self.assertEqual(response.status_code, 302)  # Redirige debido a la falta de permiso
        self.assertRedirects(response, '/')

    def test_index_inventarios_with_permission(self):
        # Intentar acceder a la vista con el permiso adecuado
        self.client.login(username='adminuser', password='12345')
        response = self.client.get(reverse('indexInventarios'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto 1')
    
    def test_new_product_post_valid(self):
        # Probar crear un nuevo producto con datos válidos
        self.client.login(username='adminuser', password='12345')

        # Asegúrate de pasar el ID del proveedor en lugar de su nombre
        data = {
            'nombre': 'Producto Nuevo', 
            'cantidad': 5, 
            'presentacion': 'Caja', 
            'proveedor': self.proveedor.id  # Pasar el ID del proveedor
        }
        response = self.client.post(reverse('newProduct'), data)

        # Verificar que la respuesta sea un 200
        self.assertEqual(response.status_code, 200)

 

    def test_eliminar_producto(self):
        # Probar eliminación lógica de un producto
        self.client.login(username='adminuser', password='12345')
        response = self.client.get(reverse('eliminarProducto', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirige a la lista de productos
        self.product.refresh_from_db()
        self.assertTrue(self.product.eliminado)

    def test_product_search(self):
        # Probar búsqueda de productos con filtros
        self.client.login(username='adminuser', password='12345')
        response = self.client.get(reverse('product_search'), {'query': 'Producto 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto 1')

    def test_edit_product_post_valid(self):
        # Probar la edición de un producto con datos válidos
        self.client.login(username='adminuser', password='12345')

        # Usar el ID del proveedor y asegurarnos de pasar los datos correctos
        data = {
            'nombre': 'Producto Editado', 
            'cantidad': 20, 
            'presentacion': 'Caja', 
            'proveedor': self.proveedor.id  # Pasar el ID del proveedor
        }

        # Enviar la solicitud POST para editar el producto
        response = self.client.post(reverse('edit_product', args=[self.product.id]), data)

        # Verificar que la respuesta sea un 200 y no una redirección
        self.assertEqual(response.status_code, 200)

        # Volver a cargar el producto desde la base de datos para comprobar que se actualizó
        self.product.refresh_from_db()





