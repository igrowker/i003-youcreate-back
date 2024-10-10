from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
from PagoColaborador.models import PagoColaborador
from Colaborador.models import Colaborador
from Usuario.models import CustomUser
from rest_framework.test import APIClient

class TestPagoColaboradorViews(TestCase):
    def setUp(self):
        self.usuario = CustomUser.objects.create_user(
            username="andrec",
            nombre="André",
            apellido="Candeloro",
            correo="acnm8@gmail.com",
            password="ACNM0000",
            pais_residencia="AR",
            redes_sociales={"instagram": "@example"}
        )

        self.colaborador = Colaborador.objects.create(
            nombre="Colaborador Test",
            servicio="Servicio Test",
            monto=100.00,
            usuario=self.usuario
        )

        refresh = RefreshToken.for_user(self.usuario)
        self.token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_lista_pagos(self):
        PagoColaborador.objects.create(
            colaborador_id=self.colaborador,
            monto=2000.00,  
            fecha_pago=date.today(),
            descripcion='Pago Test 1',
            metodo_pago='Transferencia'  
        )
        PagoColaborador.objects.create(
            colaborador_id=self.colaborador,
            monto=1500.00,
            fecha_pago=date.today(),
            descripcion='Pago Test 2',
            metodo_pago='Efectivo'  
        )
        
        response = self.client.get(reverse('pagocolaborador-list'))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, "Pago Test 1")
        self.assertContains(response, "Pago Test 2")

    def test_crear_pago_view(self):
        response = self.client.post(reverse('pagocolaborador-list'), {
            'colaborador_id': self.colaborador.id,  
            'monto': 2000.00,
            'fecha_pago': date.today().strftime('%Y-%m-%d'),  
            'descripcion': 'Pago Test',
            'metodo_pago': 'Transferencia'
        })

        self.assertEqual(response.status_code, 201)

        self.assertEqual(PagoColaborador.objects.count(), 1)
        self.assertEqual(PagoColaborador.objects.first().descripcion, 'Pago Test')
        self.assertEqual(PagoColaborador.objects.first().metodo_pago, 'Transferencia')  

    def test_actualizar_pago(self):
        pago = PagoColaborador.objects.create(
            colaborador_id=self.colaborador,
            monto=2000.00,  
            fecha_pago=date.today(),
            descripcion='Pago Test',
            metodo_pago='Efectivo' 
        )

        response = self.client.patch(reverse('pagocolaborador-detail', args=[pago.id]), {
            'monto': 2500.00,
            'descripcion': 'Pago Actualizado',
            'metodo_pago': 'Transferencia'  
        })

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Pago Actualizado')

        pago.refresh_from_db() 
        self.assertEqual(pago.monto, 2500.00)
        self.assertEqual(pago.descripcion, 'Pago Actualizado')
        self.assertEqual(pago.metodo_pago, 'Transferencia')  

    def tearDown(self):
        PagoColaborador.objects.filter(colaborador_id=self.colaborador).delete()
        self.colaborador.delete()
        self.usuario.delete()
