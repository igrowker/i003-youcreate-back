from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ingreso, Usuario  # Asegúrate de importar el modelo Usuario


class IngresosControllerTests(APITestCase):
    def setUp(self):
        # Crea un usuario para las pruebas (usa el campo correcto aquí)
        self.usuario = Usuario.objects.create(
            nombre="Test User",
            correo="testuser@example.com",
            password="testpassword",
            pais_residencia="Argentina",
        )

        # Crea algunos ingresos para el usuario
        self.ingreso1 = Ingreso.objects.create(
            monto=Decimal("100"),
            origen="Trabajo",
            fecha="2024-09-01",
            usuario_id=self.usuario,
        )
        self.ingreso2 = Ingreso.objects.create(
            monto=Decimal("150"),
            origen="Inversiones",
            fecha="2024-04-05",
            usuario_id=self.usuario,
        )
        self.ingreso3 = Ingreso.objects.create(
            monto=Decimal("50"),
            origen="Trabajo",
            fecha="2023-09-10",
            usuario_id=self.usuario,
        )

    def test_obtener_ingresos_usuario(self):
        # Define la URL usando el ID del usuario
        url = reverse("ingresos-usuario", args=[self.usuario.id])

        # Realiza la solicitud GET
        response = self.client.get(url)

        # Verifica que la respuesta sea correcta
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que los datos devueltos sean correctos
        expected_data = [
            {"origen": "Trabajo", "monto": "150"},  # Total para "Trabajo"
            {"origen": "Inversiones", "monto": "150"},
        ]

        # Convierte los montos a cadenas para la comparación
        response_data = [
            {"origen": ingreso["origen"], "monto": str(ingreso["total"])}
            for ingreso in response.data
        ]

        # Ordenar la respuesta y el esperado para facilitar la comparación
        self.assertEqual(
            sorted(response_data, key=lambda x: x["origen"]),
            sorted(expected_data, key=lambda x: x["origen"]),
        )

    def test_obtener_ingresos_totales(self):
        url = reverse("ingresos-totales", args=[self.usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que el total de ingresos devuelto sea correcto con sus valores borde
        total_ingresos_esperado = str(Decimal("300"))
        total_ingresos_cero = str(Decimal("0"))
        total_ingresos_negativos = str(Decimal("-1"))
        self.assertEqual(str(response.data["total"]), total_ingresos_esperado)
        self.assertNotEqual(str(response.data["total"]), total_ingresos_cero)
        self.assertNotEqual(str(response.data["total"]), total_ingresos_negativos)

    def test_obtener_ingresos_por_anio(self):
        url = reverse(
            "ingresos-por-anio", kwargs={"usuario_id": self.usuario.id, "anio": 2024}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotEqual(str(response.data[0]["total"]), str(Decimal("-1")))
        self.assertEqual(str(response.data[0]["total"]), str(Decimal("250.00")))

    def test_obtener_ingresos_por_mes(self):
        url = reverse(
            "ingresos-por-mes", kwargs={"usuario_id": self.usuario.id, "mes": 4}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]["mes"], "April")
        self.assertNotEqual(str(response.data[0]["total"]), str(Decimal("-1")))
        self.assertEqual(str(response.data[0]["total"]), str(Decimal("150.00")))
