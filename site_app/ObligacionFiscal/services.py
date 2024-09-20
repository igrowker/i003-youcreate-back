# ObligacionFiscal/services.py
from datetime import date, timedelta
from .repositories import ObligacionesFiscalesRepository
from Ingreso.models import Ingreso

class ObligacionesFiscalesService:

    def __init__(self, usuario):
        self.usuario = usuario
        self.pais = usuario.pais_residencia
        self.repositorio = ObligacionesFiscalesRepository(usuario)
    
    def manejar_obligaciones(self):
        """Maneja las obligaciones según el país del usuario"""
        if self.pais == "Argentina":
            self.calcular_monotributo()
            self.calcular_retencion_ganancias()

    def calcular_monotributo(self):
        ingresos_anuales = self.obtener_ingresos_anuales()
        cuota_monotributo = self.calcular_cuota_monotributo(ingresos_anuales)
        vencimiento_monotributo = self.calcular_vencimiento_monotributo()

        self.repositorio.guardar_obligacion(
            tipo_impuesto='Monotributo',
            monto_a_pagar=cuota_monotributo,
            fecha_vencimiento=vencimiento_monotributo
        )

    def calcular_retencion_ganancias(self):
        ingresos_mensuales = self.obtener_ingresos_mensuales()
        retencion_ganancias = self.calcular_retencion_ganancias(ingresos_mensuales)

        self.repositorio.guardar_obligacion(
            tipo_impuesto='Impuesto a las Ganancias',
            monto_a_pagar=retencion_ganancias,
            fecha_vencimiento=date.today().replace(day=30)  # Vencimiento al final del mes
        )

    # Métodos auxiliares: obtener ingresos, calcular vencimientos y cuotas
    def obtener_ingresos_anuales(self):
        ingresos = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year)
        return sum(ingreso.monto for ingreso in ingresos)

    def obtener_ingresos_mensuales(self):
        mes_actual = date.today().month
        ingresos = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year, fecha__month=mes_actual)
        return sum(ingreso.monto for ingreso in ingresos)

    def calcular_vencimiento_monotributo(self):
        vencimiento = date.today().replace(day=20)
        while vencimiento.weekday() > 4:  # Ajustar si es fin de semana
            vencimiento += timedelta(days=1)
        return vencimiento

    def calcular_cuota_monotributo(self, ingresos_anuales):
        if ingresos_anuales <= 370000:
            return 2500.00
        elif ingresos_anuales <= 550000:
            return 5000.00
        else:
            return 10000.00

    def calcular_retencion_ganancias(self, ingresos_mensuales):
        if ingresos_mensuales < 50000:
            return ingresos_mensuales * 0.05
        elif ingresos_mensuales < 100000:
            return ingresos_mensuales * 0.10
        else:
            return ingresos_mensuales * 0.15
