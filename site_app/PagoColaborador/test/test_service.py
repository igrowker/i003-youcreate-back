from django.test import TestCase
from django.urls import reverse
from datetime import date
from Colaborador.models import Colaborador
from Usuario.models import CustomUser
from PagoColaborador.models import PagoColaborador
from PagoColaborador.services import PagosColaboradoresService 

class TestPagosColaboradoresService(TestCase):
    def setUp(self):
        self.usuario = CustomUser.objects.create(      
            nombre= "André",
            apellido= "Candeloro",
            correo = "acnm8@gmail.com",
            password = "ACNM0000",
            pais_residencia =  "AR",
            redes_sociales =  {
                "instagram": "@example"
            }
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
            monto=1000.00,
            fecha_pago=date.today(),
            descripcion="Pago por servicios"
        )
        self.assertIsInstance(pago, PagoColaborador)
        self.assertEqual(pago.monto, 1000.00) 

    def test_actualizar_pago_exitoso(self):
        pago = PagosColaboradoresService.registrar_pago(
            colaborador_id=self.colaborador.id,
            monto=1000.00,
            fecha_pago=date.today(),
            descripcion="Pago inicial"
        )
        actualizado = PagosColaboradoresService.actualizar_pago(
            pago_id=pago.id,
            monto=1500.00,
            descripcion="Pago actualizado"
        )
        self.assertEqual(actualizado.monto, 1500.00)  

    def test_obtener_historial_pagos(self):
        PagosColaboradoresService.registrar_pago(self.colaborador.id, 1000.00, date.today(), "Pago 1")
        pagos = PagosColaboradoresService.obtener_historial_pagos(self.colaborador.id)
        self.assertEqual(len(pagos), 1)
        self.assertEqual(pagos[0].descripcion, "Pago 1")  

    def tearDown(self):
        self.colaborador.delete()
        self.usuario.delete()
