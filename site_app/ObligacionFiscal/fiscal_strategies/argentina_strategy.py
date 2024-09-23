from .strategy import ObligacionesFiscalesStrategy  # Importa la estrategia base para obligaciones fiscales
from ..repositories import ObligacionesFiscalesRepository  # Importa el repositorio de obligaciones fiscales
from decimal import Decimal, ROUND_HALF_UP  # Importa Decimal para manejar cálculos monetarios
from datetime import date, timedelta  # Importa funciones para trabajar con fechas
import calendar  # Importa el módulo para trabajar con calendarios
from Ingreso.models import Ingreso  # Importa el modelo de ingresos

class ArgentinaFiscalStrategy(ObligacionesFiscalesStrategy):
    """Estrategia para las obligaciones fiscales en Argentina."""

    def __init__(self, usuario):
        # Inicializa la estrategia con un usuario y un repositorio asociado
        self.usuario = usuario
        self.repositorio = ObligacionesFiscalesRepository(usuario)  # Crea un repositorio para el usuario
        

    def calcular_obligaciones(self):
        """Calcula y guarda las obligaciones fiscales para Argentina."""
        # Calculamos Monotributo
        ingresos_anuales = self.estimar_ingresos_anuales()  # Estima los ingresos anuales
        cuota_monotributo = self.calcular_cuota_monotributo(ingresos_anuales)  # Calcula la cuota
        if cuota_monotributo:
            vencimiento_monotributo = self.calcular_vencimiento_monotributo()  # Calcula la fecha de vencimiento
            obligacion = self.repositorio.guardar_obligacion(
                tipo_impuesto='Monotributo',  # Especifica el tipo de impuesto
                monto_a_pagar=cuota_monotributo,  # Monto a pagar
                fecha_vencimiento=vencimiento_monotributo  # Fecha de vencimiento
            )

        # Calculamos Impuesto a las Ganancias
        ingresos_mensuales = self.obtener_ingresos_mensuales()  # Obtiene ingresos mensuales
        ganancias = self.calcular_retencion_ganancias(ingresos_mensuales)  # Calcula retención de ganancias
        if ganancias:
            vencimiento_ganancias = self.calcular_vencimiento_ganancias()  # Calcula la fecha de vencimiento
            obligacion_ganancias = self.repositorio.guardar_obligacion(
                tipo_impuesto='Impuesto a las Ganancias',  # Especifica el tipo de impuesto
                monto_a_pagar=ganancias,  # Monto a pagar
                fecha_vencimiento=vencimiento_ganancias  # Fecha de vencimiento
            )

        # Calculamos el IVA
        iva = self.calcular_iva(ingresos_mensuales)  # Calcula el IVA
        if iva:
            vencimiento_iva = self.calcular_vencimiento_iva()  # Calcula la fecha de vencimiento del IVA
            obligacion_iva = self.repositorio.guardar_obligacion(
                tipo_impuesto='IVA',  # Especifica el tipo de impuesto
                monto_a_pagar=iva,  # Monto a pagar
                fecha_vencimiento=vencimiento_iva  # Fecha de vencimiento
            )

    # --- Métodos Auxiliares ---

    def estimar_ingresos_anuales(self):
        """Estima los ingresos anuales del usuario en base a los ingresos registrados."""
        ingresos_mensuales = self.obtener_ingresos_mensuales()  # Obtiene los ingresos mensuales
        mes_actual = date.today().month  # Obtiene el mes actual
        
        # Si el usuario lleva menos de un año registrado, estima los ingresos anuales
        ingresos_totales = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year)  # Filtra ingresos del año actual
        meses_registrados = len(set(ingreso.fecha.month for ingreso in ingresos_totales))  # Cuenta los meses registrados
        
        if meses_registrados > 0:
            ingresos_anuales_estimados = ingresos_mensuales * 12  # Estima ingresos anuales
        else:
            ingresos_anuales_estimados = 0  # Si no hay ingresos registrados, retorna 0

        return ingresos_anuales_estimados  # Retorna la estimación

    def obtener_ingresos_mensuales(self):
        """Obtiene los ingresos mensuales del usuario."""
        mes_actual = date.today().month  # Obtiene el mes actual
        ingresos = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year, fecha__month=mes_actual)  # Filtra ingresos del mes actual
        return sum(ingreso.monto for ingreso in ingresos)  # Suma y retorna los ingresos

    def calcular_cuota_monotributo(self, ingresos_anuales):
        """Calcula la cuota de monotributo en base a los ingresos anuales."""
        # Determina la cuota según los ingresos anuales
        if ingresos_anuales <= Decimal('2108288.22'):
            return Decimal('12128.39')
        elif ingresos_anuales <= Decimal('3133941.71'):
            return Decimal('13571.75')
        elif ingresos_anuales <= Decimal('4387518.35'):
            return Decimal('15241.42')
        elif ingresos_anuales <= Decimal('5449094.70'):
            return Decimal('19066.46')
        elif ingresos_anuales <= Decimal('6416528.89'):
            return Decimal('24526.43')
        elif ingresos_anuales <= Decimal('8020661.11'):
            return Decimal('29223.11')
        elif ingresos_anuales <= Decimal('9624793.31'):
            return Decimal('33439.61')
        elif ingresos_anuales <= Decimal('11916410.77'):
            return Decimal('56402.68')
        elif ingresos_anuales <= Decimal('13337213.57'):
            return Decimal('81121.96')
        elif ingresos_anuales <= Decimal('15285088.45'):
            return Decimal('93619.47')
        else:
            return Decimal('106964.65')

    def calcular_retencion_ganancias(self, ingresos_mensuales):
        """Calcula la retención de impuesto a las ganancias basado en los ingresos mensuales."""
        
        # Convertir ingresos mensuales a ganancia neta imponible acumulada
        ganancia_neta_imponible = ingresos_mensuales * 12  # Proyectamos a la ganancia anual
        
        # Definir la escala de retenciones
        tramos = [
            (0, 1200000, 0, Decimal('0.05')),
            (1200000, 2400000, 60000, Decimal('0.09')),
            (2400000, 3600000, 168000, Decimal('0.12')),
            (3600000, 5400000, 312000, Decimal('0.15')),
            (5400000, 10800000, 582000, Decimal('0.19')),
            (10800000, 16200000, 1608000, Decimal('0.23')),
            (16200000, 24300000, 2850000, Decimal('0.27')),
            (24300000, 36450000, 5037000, Decimal('0.31')),
            (36450000, float('inf'), 8803500, Decimal('0.35'))
        ]
        
        retencion = Decimal('0.00') # Inicializa retención

        for limite_inferior, limite_superior, cuota_fija, porcentaje in tramos:
            if ganancia_neta_imponible > limite_inferior:
                # Calcular el exceso sobre el límite inferior
                exceso = min(ganancia_neta_imponible, limite_superior) - limite_inferior
                retencion += cuota_fija + (exceso * porcentaje) # Calcula retención
            else:
                break # Sale del bucle si se alcanza el límite

        # Redondear el resultado a 2 decimales
        retencion = retencion.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Redondea la retención
        return retencion  # Retorna la retención calculada
    
    def calcular_iva(self, ingresos_mensuales):
        """Calcula el IVA en base a los ingresos mensuales."""
        # Suponiendo que el IVA es del 21%
        iva = ingresos_mensuales * Decimal('0.21')
        iva = iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Redondear a 2 decimales
        return iva

    def calcular_vencimiento_ganancias(self):
        """Calcula la fecha de vencimiento ajustando al último día del mes si es necesario."""
        hoy = date.today() # Obtiene la fecha actual
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
    
    def calcular_vencimiento_iva(self):
        """Calcula la fecha de vencimiento del IVA (día 15 de cada mes)."""
        vencimiento = date.today().replace(day=15)
        while vencimiento.weekday() > 4:
            vencimiento += timedelta(days=1)
        return vencimiento
