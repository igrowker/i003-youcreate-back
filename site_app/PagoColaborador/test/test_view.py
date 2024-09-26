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
        # Crear el usuario
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

        # Obtener un token para el usuario
        refresh = RefreshToken.for_user(self.usuario)
        self.token = str(refresh.access_token)

        # Inicializar el cliente de API
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_lista_pagos(self):
        # Crear dos pagos antes de listar
        PagoColaborador.objects.create(
            colaborador_id=self.colaborador,
            monto=2000.00,  
            fecha_pago=date.today(),
            descripcion='Pago Test 1'
        )
        PagoColaborador.objects.create(
            colaborador_id=self.colaborador,
            monto=1500.00,
            fecha_pago=date.today(),
            descripcion='Pago Test 2'
        )
        
        response = self.client.get(reverse('pagocolaborador-list'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar que ambos pagos están en la respuesta
        self.assertContains(response, "Pago Test 1")
        self.assertContains(response, "Pago Test 2")

    def test_crear_pago_view(self):
        response = self.client.post(reverse('pagocolaborador-list'), {
            'colaborador_id': self.colaborador.id,  # Usa el ID del colaborador que ya existe
            'monto': 2000.00,
            'fecha_pago': date.today().strftime('%Y-%m-%d'),  # Formato adecuado para la fecha
            'descripcion': 'Pago Test',
        })

        # Verifica que la respuesta tenga un código de estado 201 (creado)
        self.assertEqual(response.status_code, 201)

        # Verifica que el pago se ha creado en la base de datos
        self.assertEqual(PagoColaborador.objects.count(), 1)
        self.assertEqual(PagoColaborador.objects.first().descripcion, 'Pago Test')

    def test_actualizar_pago(self):
        # Crear un pago para actualizar
        pago = PagoColaborador.objects.create(
            colaborador_id=self.colaborador,
            monto=2000.00,  
            fecha_pago=date.today(),
            descripcion='Pago Test'
        )

        response = self.client.patch(reverse('pagocolaborador-detail', args=[pago.id]), {
            'monto': 2500.00,
            'descripcion': 'Pago Actualizado'
        })

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Pago Actualizado')

        pago.refresh_from_db() 
        self.assertEqual(pago.monto, 2500.00)
        self.assertEqual(pago.descripcion, 'Pago Actualizado')

    def tearDown(self):
        # Eliminar todos los pagos relacionados con el colaborador
        PagoColaborador.objects.filter(colaborador_id=self.colaborador).delete()
        # Eliminar el colaborador y el usuario
        self.colaborador.delete()
        self.usuario.delete()
