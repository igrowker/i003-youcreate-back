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
        # Crear un pago antes de listar
        PagoColaborador.objects.create(
            colaborador_id=self.colaborador,  # Usa la instancia de Colaborador
            monto=2000.00,
            fecha_pago=date.today(),
            descripcion='Pago Test'
        )
        
        response = self.client.get(reverse('pagocolaborador-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pago Test")  # Verifica que el pago esté en la respuesta

    def test_crear_pago_view(self):
        response = self.client.post(reverse('pagocolaborador-list'), {
            'colaborador_id': self.colaborador.id,  # Asegúrate de usar 'colaborador' y no 'colaborador_id'
            'monto': 2000.00,
            'fecha_pago': date.today().strftime('%Y-%m-%d'),
            'descripcion': 'Nuevo pago'
        })
        self.assertEqual(response.status_code, 201)  # Verifica que el estado sea 201

    def tearDown(self):
        self.colaborador.delete()
        self.usuario.delete()
