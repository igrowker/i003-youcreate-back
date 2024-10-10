from rest_framework.test import APITestCase
from .models import Ingreso, CustomUser 
from decimal import Decimal
from .service import IngresosService


class IngresosControllerTests(APITestCase):
    def setUp(self):
        # Crea un usuario para las pruebas (usa el campo correcto aquí)
        self.usuario = CustomUser.objects.create(
            nombre='Juan',
            apellido='Pérez',
            email='juan.perez@example.com',
            telefono='123456789',
            password='password',  # Asegúrate de manejar el hash de la contraseña si es necesario
            pais_residencia='Argentina',
            redes_sociales={'facebook': 'facebook.com/juanperez'},
            numero_fiscal='123456789',
            monotributo=True
        )
        # Instancia de IngresosService
        self.servicio_ingreso = IngresosService()

        # Crea algunos ingresos para el usuario
        self.ingreso1 = self.servicio_ingreso.crear_ingreso(
            monto=Decimal('100'),
            origen='Trabajo', 
            fecha='2024-04-01', 
            usuario_id=self.usuario
        )
        self.ingreso2 = self.servicio_ingreso.crear_ingreso(
            monto=Decimal('150'), 
            origen='Inversiones', 
            fecha='2023-04-05', 
            usuario_id=self.usuario
        )

        self.ingreso3 = self.servicio_ingreso.crear_ingreso(
            monto=Decimal('150'), 
            origen='Youtube', 
            fecha='2024-07-05', 
            usuario_id=self.usuario
        )

        self.ingreso4 = self.servicio_ingreso.crear_ingreso(
            monto=Decimal('150'), 
            origen='Colaborador', 
            fecha='2024-04-05', 
            usuario_id=self.usuario
        )
   
    def test_crear_ingreso(self):
        self.ingreso = self.servicio_ingreso.crear_ingreso(
            usuario_id=self.usuario,
            monto=2000,
            fecha='2023-10-20',
            origen='Prueba'
        )
        ingreso_usuario = self.servicio_ingreso.obtener_ingreso_usuario(self.usuario,self.ingreso.id)
        self.assertEqual(ingreso_usuario.monto,2000)
        self.assertEqual(ingreso_usuario.origen,'Prueba')

    def test_obtener_ingresos_usuario(self):
        ingresos_usuario = self.servicio_ingreso.obtener_ingresos_usuario(self.usuario)
        cant = len(ingresos_usuario) #Obtengo la cantidad total de ingresos 
        self.assertEqual(cant,4)
        self.assertNotEqual(cant,-1)
        self.assertNotEqual(cant,999999)
        
    def test_obtener_ingresos_totales(self):
        total_ingresos = self.servicio_ingreso.obtener_ingresos_totales(self.usuario)
        self.assertEqual(total_ingresos['total'], Decimal('550'))
        self.assertNotEqual(total_ingresos['total'], Decimal('-999'))
        self.assertNotEqual(total_ingresos['total'], Decimal('0'))
        
    def test_obtener_ingresos_de_un_mes(self):
        ingresos = self.servicio_ingreso.obtener_ingresos_de_un_mes(self.usuario,4,2024)
        cant = len(ingresos)
        self.assertEqual(cant,2)
        self.assertNotEqual(cant,-1)
        self.assertNotEqual(cant,999999)
        
        ingreso = ingresos[0]
        self.assertEqual(ingreso.monto,Decimal('100'))
        self.assertEqual(ingreso.origen,'Trabajo')

        ingreso = ingresos[1]
        self.assertEqual(ingreso.monto,Decimal('150'))
        self.assertEqual(ingreso.origen,'Colaborador')

    def test_obtener_ingresos_de_un_anio(self):
        ingresos = self.servicio_ingreso.obtener_ingresos_de_un_anio(self.usuario,2024)
        cant = len(ingresos)
        self.assertEqual(cant,3)
        self.assertNotEqual(cant,-1)
        self.assertNotEqual(cant,999999)

        ingreso = ingresos[0]
        self.assertEqual(ingreso.monto,Decimal('100'))
        self.assertEqual(ingreso.origen,'Trabajo')

        ingreso = ingresos[1]
        self.assertEqual(ingreso.monto,Decimal('150'))
        self.assertEqual(ingreso.origen,'Youtube')

        ingreso = ingresos[2]
        self.assertEqual(ingreso.monto,Decimal('150'))
        self.assertEqual(ingreso.origen,'Colaborador')

    def test_obtener_ingreso_total_en_un_anio(self):
        ingresos_2024 = self.servicio_ingreso.obtener_ingreso_total_en_un_anio(self.usuario,2024)
        self.assertEqual(ingresos_2024, {2024: Decimal('400')})  
        self.assertNotEqual(ingresos_2024, {2024: Decimal('-999')})    
        self.assertNotEqual(ingresos_2024, {2024: Decimal('0')}) 

    def test_obtener_ingreso_total_en_un_mes(self):
        ingresos_abril = self.servicio_ingreso.obtener_ingreso_total_en_un_mes(self.usuario,4,2023)
        self.assertEqual(ingresos_abril, {4: Decimal('150')})
        self.assertNotEqual(ingresos_abril, {4: Decimal('-999')})
        self.assertNotEqual(ingresos_abril, {4: Decimal('0')})