from django.test import TestCase
from django.contrib.auth import get_user_model
from ActionLog.models import ActionLog
from Usuario.models import CustomUser

User = get_user_model()

class UserActionLogTests(TestCase):
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

    def test_update_user_nombre_action_log(self):
        self.usuario.nombre = 'UpdatedName'  # Cambié de self.user a self.usuario
        self.usuario.save()  
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')  

    def test_update_user_apellido_action_log(self):
        self.usuario.apellido = 'UpdatedLastName'
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_email_action_log(self):
        self.usuario.email = 'updated@example.com'  
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_telefono_action_log(self):
        self.usuario.telefono = '987654321'
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_redes_action_log(self):
        self.usuario.redes_sociales = {'instagram': 'instagram.com/juanperez'}  
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_pais_residencia_action_log(self):
        self.usuario.pais_residencia = 'Brasil'
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_password_action_log(self):
        self.usuario.set_password('newtestpass') 
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_numero_fiscal_action_log(self):
        self.usuario.numero_fiscal = '87654321'
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')

    def test_update_user_monotributo_action_log(self):
        self.usuario.monotributo = False 
        self.usuario.save()
        action_log = ActionLog.objects.last()
        self.assertEqual(action_log.action, 'User Updated')
