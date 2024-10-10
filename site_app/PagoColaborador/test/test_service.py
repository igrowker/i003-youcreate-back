from django.test import TestCase
from datetime import date
from Colaborador.models import Colaborador
from Usuario.models import CustomUser
from PagoColaborador.models import PagoColaborador
from PagoColaborador.services import PagosColaboradoresService

class TestPagosColaboradoresService(TestCase):
    def setUp(self):
        self.usuario = CustomUser.objects.create(
            nombre='Juan',
            apellido='Pérez',
            email='juan.perez@example.com',
            telefono='123456789',
            password='password',
            pais_residencia='Argentina',
            redes_sociales={'facebook': 'facebook.com/juanperez'},
            numero_fiscal='123456789',
            monotributo=True
        )
        
        self.colaborador = Colaborador.objects.create(
            nombre="Colaborador Test",
            servicio="Servicio Test",
            monto=100.00,
            usuario=self.usuario
        )

    def test_registrar_pago_exitoso(self):
        pago = PagosColaboradoresService.registrar_pago(
            colaborador_id=self.colaborador.id,
            nombre='JuanCarlos',  
            apellido='Florentino',  
            monto=1000.00,
            fecha_pago=date.today(),
            descripcion="Pago por servicios",
            metodo_pago='Efectivo'
        )
        self.assertIsInstance(pago, PagoColaborador)
        self.assertEqual(pago.monto, 1000.00) 
        self.assertEqual(pago.nombre, 'JuanCarlos')  
        self.assertEqual(pago.apellido, 'Florentino')  

    def test_actualizar_pago_exitoso(self):
        pago = PagosColaboradoresService.registrar_pago(
            colaborador_id=self.colaborador.id,
            nombre='JuanCarlos',
            apellido='Florentino',
            monto=1000.00,
            fecha_pago=date.today(),
            descripcion="Pago inicial",
            metodo_pago='Transferencia'
        )
        
        actualizado = PagosColaboradoresService.actualizar_pago(
            pago_id=pago.id,
            monto=1500.00,
            descripcion="Pago actualizado",
            metodo_pago='Efectivo',
            nombre='NuevoNombre', 
            apellido='NuevoApellido'  
        )
        
        self.assertEqual(actualizado.monto, 1500.00)  
        self.assertEqual(actualizado.nombre, 'NuevoNombre') 
        self.assertEqual(actualizado.apellido, 'NuevoApellido')  

    def test_obtener_historial_pagos(self):
        PagosColaboradoresService.registrar_pago(
            colaborador_id=self.colaborador.id,
            nombre='JuanCarlos',
            apellido='Florentino',
            monto=1000.00,
            fecha_pago=date.today(),
            descripcion="Pago 1",
            metodo_pago='Efectivo'
        )
        pagos = PagosColaboradoresService.obtener_historial_pagos(self.colaborador.id)
        self.assertEqual(len(pagos), 1)
        self.assertEqual(pagos[0].descripcion, "Pago 1")  

    def test_eliminar_pago_exitoso(self):
        pago = PagosColaboradoresService.registrar_pago(
            colaborador_id=self.colaborador.id,
            nombre='JuanCarlos',
            apellido='Florentino',
            monto=1000.00,
            fecha_pago=date.today(),
            descripcion="Pago inicial",
            metodo_pago='Transferencia'
        )
        self.assertIsNotNone(PagoColaborador.objects.filter(id=pago.id).first())
        
        PagosColaboradoresService.eliminar_pago(pago.id)
        
        self.assertIsNone(PagoColaborador.objects.filter(id=pago.id).first())

    def tearDown(self):
        self.colaborador.delete()
        self.usuario.delete()
