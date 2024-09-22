from .strategy import ObligacionesFiscalesStrategy
from ..repositories import ObligacionesFiscalesRepository
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
import calendar
from Ingreso.models import Ingreso

class ArgentinaFiscalStrategy(ObligacionesFiscalesStrategy):
    """Estrategia para las obligaciones fiscales en Argentina."""

    def __init__(self, usuario):
        self.usuario = usuario
        self.repositorio = ObligacionesFiscalesRepository(usuario)

    def calcular_obligaciones(self):
        """Calcula y guarda las obligaciones fiscales para Argentina."""
        # Calculamos Monotributo
        monotributo = self.calcular_monotributo()
        if monotributo:
            print(f"Monotributo guardado: {monotributo}")

        # Calculamos Impuesto a las Ganancias
        ingresos_mensuales = self.obtener_ingresos_mensuales()
        ganancias = self.calcular_retencion_ganancias(ingresos_mensuales)
        if ganancias:
            vencimiento_ganancias = self.calcular_vencimiento_ganancias()
            obligacion_ganancias = self.repositorio.guardar_obligacion(
                tipo_impuesto='Impuesto a las Ganancias',
                monto_a_pagar=ganancias,
                fecha_vencimiento=vencimiento_ganancias
            )
            print(f"Impuesto a las ganancias guardado: {obligacion_ganancias}")

    # --- Métodos Auxiliares ---

    def calcular_monotributo(self):
        """Calcula y guarda la cuota de monotributo."""
        ingresos_anuales = self.obtener_ingresos_anuales()
        print(f"Ingresos anuales del usuario: {ingresos_anuales}")
        cuota_monotributo = self.calcular_cuota_monotributo(ingresos_anuales)
        vencimiento_monotributo = self.calcular_vencimiento_monotributo()

        # Guardar la obligación en la base de datos
        obligacion = self.repositorio.guardar_obligacion(
            tipo_impuesto='Monotributo',
            monto_a_pagar=cuota_monotributo,
            fecha_vencimiento=vencimiento_monotributo
        )
        return obligacion

    def obtener_ingresos_anuales(self):
        """Obtiene los ingresos anuales del usuario."""
        ingresos = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year)
        return sum(ingreso.monto for ingreso in ingresos)

    def obtener_ingresos_mensuales(self):
        """Obtiene los ingresos mensuales del usuario."""
        mes_actual = date.today().month
        ingresos = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year, fecha__month=mes_actual)
        return sum(ingreso.monto for ingreso in ingresos)

    def calcular_cuota_monotributo(self, ingresos_anuales):
        """Calcula la cuota de monotributo en base a los ingresos anuales."""
        if ingresos_anuales <= Decimal('370000'):
            return Decimal('2500.00')
        elif ingresos_anuales <= Decimal('550000'):
            return Decimal('5000.00')
        else:
            return Decimal('10000.00')

    def calcular_retencion_ganancias(self, ingresos_mensuales):
        """Calcula la retención de impuesto a las ganancias basado en los ingresos mensuales."""
        if ingresos_mensuales < Decimal('50000'):
            retencion = ingresos_mensuales * Decimal('0.05')
            print("Retención de ganancias calculada al 5%")
        elif ingresos_mensuales < Decimal('100000'):
            retencion = ingresos_mensuales * Decimal('0.10')
            print("Retención de ganancias calculada al 10%")
        else:
            retencion = ingresos_mensuales * Decimal('0.15')
            print("Retención de ganancias calculada al 15%")
        
        # Redondear el resultado a 2 decimales
        retencion = retencion.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        print(f"Retención de ganancias después del redondeo: {retencion}")
        return retencion

    def calcular_vencimiento_ganancias(self):
        """Calcula la fecha de vencimiento ajustando al último día del mes si es necesario."""
        hoy = date.today()
        ultimo_dia_mes = calendar.monthrange(hoy.year, hoy.month)[1]  # Último día del mes
        vencimiento = hoy.replace(day=min(30, ultimo_dia_mes))  # Si el mes tiene menos de 30 días, ajusta al último día

        # Ajustar si cae en fin de semana
        while vencimiento.weekday() > 4:  # Si el vencimiento cae en sábado o domingo
            vencimiento -= timedelta(days=1)
        return vencimiento

    def calcular_vencimiento_monotributo(self):
        """Calcula la fecha de vencimiento del monotributo (día 20 de cada mes)."""
        vencimiento = date.today().replace(day=20)
        # Ajustar si el 20 cae en fin de semana
        while vencimiento.weekday() > 4:
            vencimiento += timedelta(days=1)
        return vencimiento