from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ActionLog

User = get_user_model()

class UserActionLogTests(TestCase):
    def setUp(self):
        # Configuración inicial: creación de un usuario
        self.user_data = {
            "nombre": "Test",
            "apellido": "User",
            "correo": "testuser@example.com",
            "password": "testpassword123",
            "pais_residencia": "Argentina",
        }
        self.user = User.objects.create_user(
            nombre=self.user_data["nombre"],
            apellido=self.user_data["apellido"],
            correo=self.user_data["correo"],
            password=self.user_data["password"],
            pais_residencia=self.user_data["pais_residencia"],
        )

    def test_create_user_action_log(self):
        # Crear un nuevo usuario
        new_user = User.objects.create_user(
            nombre="New",
            apellido="User",
            correo="newuser@example.com",
            password="newpassword123",
            pais_residencia="Argentina",
        )

        # Verificar que se creó un registro en ActionLog
        action_log = ActionLog.objects.filter(user=new_user).first()
        self.assertIsNotNone(action_log)
        self.assertEqual(action_log.action, 'User Created')
        self.assertIn('Usuario New User creado.', action_log.details)

    def test_update_user_action_log(self):
        # Actualizar el usuario
        self.user.nombre = "Updated"
        self.user.save()  # Guarda los cambios

        # Verificar que se creó un registro en ActionLog
        action_log = ActionLog.objects.filter(user=self.user).last()
        self.assertIsNotNone(action_log)
        self.assertEqual(action_log.action, 'User Updated')
        self.assertIn("Campo 'nombre' cambiado de 'Test' a 'Updated'", action_log.details)

    def test_update_user_email_action_log(self):
        old_email = self.user.correo
        self.user.correo = "updateduser@example.com"
        self.user.save()

        # Verificar que se creó un registro en ActionLog
        action_log = ActionLog.objects.filter(user=self.user).last()
        self.assertIsNotNone(action_log)
        self.assertEqual(action_log.action, 'User Updated')
        self.assertIn(f"Campo 'correo' cambiado de '{old_email}' a '{self.user.correo}'", action_log.details)
