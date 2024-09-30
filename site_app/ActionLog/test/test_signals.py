from django.test import TestCase
from django.contrib.auth import get_user_model
from ActionLog.models import ActionLog

User = get_user_model()

class UserActionLogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            nombre='Test',
            apellido='User',
            correo='test@example.com',
            telefono='123456789',
            redes_sociales='twitter',
            pais_residencia='Argentina'
        )
    def test_update_user_nombre_action_log(self):
        self.user.nombre = 'UpdatedName'
        self.user.save()  
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')  

    def test_update_user_apellido_action_log(self):
        self.user.apellido = 'UpdatedLastName'
        self.user.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_email_action_log(self):
        self.user.correo = 'updated@example.com'
        self.user.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_telefono_action_log(self):
        self.user.telefono = '987654321'
        self.user.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_redes_action_log(self):
        self.user.redes_sociales = 'instagram'
        self.user.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_pais_residencia_action_log(self):
        self.user.pais_residencia = 'Brasil'
        self.user.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')