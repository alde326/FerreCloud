from django.test import TestCase
from django.urls import reverse
from .models import Costos, Tipos
from datetime import date

class CostosViewsTests(TestCase):
    def setUp(self):
        # Crear un tipo para usar en los costos
        self.tipo = Tipos.objects.create(nombre="Operativo")
        
        # Crear un costo inicial para editar y eliminar
        self.costo = Costos.objects.create(
            nombre="Costo 1",
            ingreso_egreso=True,
            tipo=self.tipo,
            valor=1000.50,
            fecha=date.today(),
            descripcion="Descripción de prueba",
        )
    
    def run(self, result=None):
        result = super().run(result)
        if result.wasSuccessful():
            print(f"{self._testMethodName}: OK")
        return result

    def test_crear_costo(self):
        response = self.client.post(reverse('crearCosto'), {
            'nombre': 'Nuevo Costo',
            'ingreso_egreso': False,
            'tipo': self.tipo.id,
            'valor': 5000.00,
            'fecha': date.today(),
            'descripcion': 'Descripción del nuevo costo',
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.assertEqual(Costos.objects.count(), 2)
        self.assertTrue(Costos.objects.filter(nombre="Nuevo Costo").exists())

    def test_edit_costo(self):
        response = self.client.post(reverse('editCosto', args=[self.costo.id]), {
            'nombre': 'Costo Editado',
            'ingreso_egreso': True,
            'tipo': self.tipo.id,
            'valor': 2000.00,
            'fecha': date.today(),
            'descripcion': 'Descripción editada',
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.costo.refresh_from_db()
        self.assertEqual(self.costo.nombre, 'Costo Editado')
        self.assertEqual(self.costo.valor, 2000.00)

    def test_eliminar_costo(self):
        response = self.client.get(reverse('eliminarCosto', args=[self.costo.id]))
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.costo.refresh_from_db()
        self.assertTrue(self.costo.eliminado)

class TiposViewsTests(TestCase):
    def setUp(self):
        # Crear un tipo inicial para editar y eliminar
        self.tipo = Tipos.objects.create(nombre="Operativo")

    def run(self, result=None):
        result = super().run(result)
        if result.wasSuccessful():
            print(f"{self._testMethodName}: OK")
        return result

    def test_crear_tipo(self):
        response = self.client.post(reverse('crearTipo'), {
            'nombre': 'Nuevo Tipo',
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.assertEqual(Tipos.objects.count(), 2)
        self.assertTrue(Tipos.objects.filter(nombre="Nuevo Tipo").exists())

    def test_edit_tipo(self):
        response = self.client.post(reverse('editTipo', args=[self.tipo.id]), {
            'nombre': 'Tipo Editado',
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.tipo.refresh_from_db()
        self.assertEqual(self.tipo.nombre, 'Tipo Editado')

    def test_eliminar_tipo(self):
        response = self.client.get(reverse('eliminarTipo', args=[self.tipo.id]))
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.tipo.refresh_from_db()
        self.assertTrue(self.tipo.eliminado)
