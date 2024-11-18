from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Producto, Cliente, Factura, DetalleFactura
from Configuracion.models import Parametros, Costos, Tipos
from Proveedores.models import Proveedor
from .views import obtener_parametro_iva, procesar_carrito, registrar_cliente, crear_factura, crear_detalles_factura, registrar_ingreso

class FuncionesTests(TestCase):

    def setUp(self):
        # Crear un parámetro de IVA
        self.iva_parametro = Parametros.objects.create(nombre="IVA", porcentaje=0.19)

        # Crear un proveedor para los productos
        self.proveedor = Proveedor.objects.create(
            nit="123456789",
            razonSolcial="Proveedor Ejemplo",
            telefono="123456789",
            email="proveedor@ejemplo.com",
            direccion="Calle Falsa 123",
            nombreContacto="Juan Pérez",
            celular="987654321"
        )

        # Crear productos de prueba con proveedor
        self.producto1 = Producto.objects.create(
            nombre="Producto 1",
            cantidad=10,
            precio=Decimal('100.00'),
            proveedor=self.proveedor
        )
        self.producto2 = Producto.objects.create(
            nombre="Producto 2",
            cantidad=5,
            precio=Decimal('50.00'),
            proveedor=self.proveedor
        )

        # Crear un tipo para ingresos
        self.tipo_ingreso = Tipos.objects.create(id=6, nombre="Venta")

    def test_obtener_parametro_iva(self):
        iva_tasa = obtener_parametro_iva()
        self.assertEqual(iva_tasa, Decimal('0.19'))
        print("OK: test_obtener_parametro_iva pasó exitosamente")

        # Prueba cuando no hay parámetro IVA
        Parametros.objects.filter(nombre="IVA").delete()
        iva_tasa = obtener_parametro_iva()
        self.assertIsNone(iva_tasa)
        print("OK: test_obtener_parametro_iva (sin parámetro IVA) pasó exitosamente")

    def test_procesar_carrito(self):
        carrito = [
            {'id': self.producto1.id, 'cantidad': '2'},
            {'id': self.producto2.id, 'cantidad': '3'}
        ]
        resultado, error = procesar_carrito(carrito, Decimal('0.19'))
        self.assertIsNone(error)
        self.assertEqual(resultado['total'], Decimal('350.00'))
        self.assertEqual(len(resultado['detalles']), 2)
        print("OK: test_procesar_carrito pasó exitosamente")

        # Prueba con inventario insuficiente
        carrito = [{'id': self.producto1.id, 'cantidad': '20'}]
        resultado, error = procesar_carrito(carrito, Decimal('0.19'))
        self.assertIsNotNone(error)
        self.assertIsNone(resultado)

        # Prueba con producto inexistente
        carrito = [{'id': 999, 'cantidad': '1'}]
        resultado, error = procesar_carrito(carrito, Decimal('0.19'))
        self.assertIsNotNone(error)
        self.assertIsNone(resultado)
        print("OK: test_procesar_carrito con inventario insuficiente o producto inexistente pasó exitosamente")

    def test_registrar_cliente(self):
        documento = "123456789"
        nombre = "Cliente Prueba"
        telefono = "123456"
        email = "cliente@prueba.com"
        direccion = "Calle Falsa 123"

        cliente, creado = registrar_cliente(documento, nombre, telefono, email, direccion)
        self.assertTrue(creado)
        self.assertEqual(cliente.nombre, nombre)
        print("OK: test_registrar_cliente pasó exitosamente")

        # Prueba con cliente existente
        cliente, creado = registrar_cliente(documento, nombre, telefono, email, direccion)
        self.assertFalse(creado)
        print("OK: test_registrar_cliente (cliente existente) pasó exitosamente")

    def test_crear_factura(self):
        cliente = Cliente.objects.create(documento="123456789", nombre="Cliente Test")
        total = Decimal('350.00')
        iva = Decimal('66.50')
        total_con_iva = Decimal('416.50')
        observacion = "Factura de prueba"

        factura = crear_factura(cliente, total, iva, total_con_iva, observacion)
        self.assertIsNotNone(factura)
        self.assertEqual(factura.total, total)
        self.assertEqual(factura.iva, iva)
        self.assertEqual(factura.total_con_iva, total_con_iva)
        print("OK: test_crear_factura pasó exitosamente")

    def test_crear_detalles_factura(self):
        cliente = Cliente.objects.create(documento="123456789", nombre="Cliente Test")
        factura = Factura.objects.create(cliente=cliente, total=Decimal('350.00'), iva=Decimal('66.50'), total_con_iva=Decimal('416.50'))

        detalles = [
            {'producto': self.producto1, 'cantidad': Decimal('2'), 'precio_unitario': self.producto1.precio},
            {'producto': self.producto2, 'cantidad': Decimal('3'), 'precio_unitario': self.producto2.precio}
        ]
        crear_detalles_factura(factura, detalles)

        self.assertEqual(DetalleFactura.objects.filter(factura=factura).count(), 2)
        print("OK: test_crear_detalles_factura pasó exitosamente")

    def test_registrar_ingreso(self):
        total_con_iva = Decimal('416.50')
        factura_id = 1
        registrar_ingreso(total_con_iva, factura_id)

        ingreso = Costos.objects.filter(nombre="Venta", valor=total_con_iva).first()
        self.assertIsNotNone(ingreso)
        self.assertEqual(ingreso.descripcion, f"Factura #{factura_id}")
        print("OK: test_registrar_ingreso pasó exitosamente")
