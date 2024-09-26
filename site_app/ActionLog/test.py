from django.test import TestCase
from yourapp.models import CustomUser, ActionLog

class UserSignalsTest(TestCase):
    def test_user_creation_signal(self):
        user = CustomUser.objects.create(
            username='testuser',
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            password='testpassword',
            pais_residencia='Argentina',
            redes_sociales={}
        )
        log = ActionLog.objects.get(user=user)
        self.assertEqual(log.action, 'User Created')

    def test_user_update_signal(self):
        user = CustomUser.objects.create(
            username='testuser2',
            nombre='Another',
            apellido='User',
            correo='anotheruser@example.com',
            password='testpassword',
            pais_residencia='Argentina',
            redes_sociales={}
        )
        user.nombre = 'Updated Name'
        user.save()
        log = ActionLog.objects.get(user=user, action='User Updated')
        self.assertIn('Nombre cambiado de Another a Updated Name', log.details)
