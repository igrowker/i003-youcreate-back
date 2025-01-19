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
        
    def calcular_obligaciones(self, monotributo=True):
        """Calcula y guarda las obligaciones fiscales para Argentina."""
        print(monotributo)
        ingresos_mensuales = self.obtener_ingresos_mensuales()  # Obtiene los ingresos mensuales
        print(ingresos_mensuales)
        meses_registrados = self.contar_meses_registrados()  # Cuenta los meses con ingresos
        print(meses_registrados)
        
        # Determina si el usuario es monotributista según el argumento pasado
        if monotributo is not None:
            es_monotributista = monotributo
            print(es_monotributista)
        else:
            es_monotributista = self.usuario.monotributo

        if es_monotributista:
            if meses_registrados > 0:
                ingresos_anuales_estimados = (ingresos_mensuales / meses_registrados) * 12
                print(f"Ingresos anuales estimados: ${ingresos_anuales_estimados:.2f}")
                cuota_monotributo = self.calcular_cuota_monotributo(ingresos_anuales_estimados)
                print(f"Cuota Monotributo: ${cuota_monotributo:.2f}")
                if cuota_monotributo:
                    vencimiento_monotributo = self.calcular_vencimiento_monotributo()  # Calcula la fecha de vencimiento
                    print(f"Vencimiento Monotributo: {vencimiento_monotributo}")
                    self.repositorio.guardar_obligacion(
                        tipo_impuesto='Monotributo',
                        monto_a_pagar=cuota_monotributo,
                        fecha_vencimiento=vencimiento_monotributo
                    )

            # Calcular Ganancias
            ganancias = self.calcular_retencion_ganancias(ingresos_mensuales)
            if ganancias:
                vencimiento_ganancias = self.calcular_vencimiento_ganancias()
                self.repositorio.guardar_obligacion(
                    tipo_impuesto='Impuesto a las Ganancias',
                    monto_a_pagar=ganancias,
                    fecha_vencimiento=vencimiento_ganancias
                )
        else:
            # Si no es monotributista, calcular IVA y Ganancias
            if meses_registrados > 0:
                iva = self.calcular_iva(ingresos_mensuales)
                if iva:
                    vencimiento_iva = self.calcular_vencimiento_iva()
                    self.repositorio.guardar_obligacion(
                        tipo_impuesto='IVA',
                        monto_a_pagar=iva,
                        fecha_vencimiento=vencimiento_iva
                    )

                # Calcular Ganancias
                ganancias = self.calcular_retencion_ganancias(ingresos_mensuales)
                if ganancias:
                    vencimiento_ganancias = self.calcular_vencimiento_ganancias()
                    self.repositorio.guardar_obligacion(
                        tipo_impuesto='Impuesto a las Ganancias',
                        monto_a_pagar=ganancias,
                        fecha_vencimiento=vencimiento_ganancias
                    )

    # --- Métodos Auxiliares ---
    
    def obtener_ingresos_mensuales(self):
        """Obtiene los ingresos mensuales del usuario basado en los ingresos registrados en el año actual."""
        ingresos_totales = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year)
        if ingresos_totales.exists():
            total_ingresos = sum(ingreso.monto for ingreso in ingresos_totales)
            meses_registrados = self.contar_meses_registrados()
            if meses_registrados > 0:
                ingresos_mensuales_promedio = total_ingresos / meses_registrados
                return ingresos_mensuales_promedio
        return 0  # Si no hay ingresos registrados, retorna 0

    def contar_meses_registrados(self):
        """Cuenta los meses con ingresos registrados por el usuario en el año actual."""
        ingresos_totales = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year)  # Filtra ingresos del año actual
        meses_registrados = len(set(ingreso.fecha.month for ingreso in ingresos_totales))  # Cuenta los meses con ingresos
        return meses_registrados

    def calcular_cuota_monotributo(self, ingresos_anuales_estimados):
        """Calcula la cuota de monotributo en base a los ingresos anuales estimados."""
        print(f"Ingresos anuales estimados: ${ingresos_anuales_estimados:.2f}")
        if ingresos_anuales_estimados <= Decimal('6450000'):
            return Decimal('26000')  # Categoría A
        elif ingresos_anuales_estimados <= Decimal('9450000'):
            return Decimal('30280')  # Categoría B
        elif ingresos_anuales_estimados <= Decimal('13250000'):
            return Decimal('35458')  # Categoría C
        elif ingresos_anuales_estimados <= Decimal('16450000'):
            return Decimal('45443')  # Categoría D
        elif ingresos_anuales_estimados <= Decimal('19350000'):
            return Decimal('64348')  # Categoría E
        elif ingresos_anuales_estimados <= Decimal('24250000'):
            return Decimal('80983')  # Categoría F
        elif ingresos_anuales_estimados <= Decimal('29000000'):
            return Decimal('123696')  # Categoría G
        elif ingresos_anuales_estimados <= Decimal('44000000'):
            return Decimal('280734')  # Categoría H
        elif ingresos_anuales_estimados <= Decimal('49250000'):
            return Decimal('517608')  # Categoría I
        elif ingresos_anuales_estimados <= Decimal('56400000'):
            return Decimal('626931')  # Categoría J
        elif ingresos_anuales_estimados <= Decimal('68000000'):
            return Decimal('867931')  # Categoría K
        else:
            # Si excede el límite superior de la última categoría, se devuelve el valor de la Categoría K
            return Decimal('867931')  # Categoría K (última)

    def calcular_retencion_ganancias(self, ingresos_mensuales):
        """Calcula la retención de impuesto a las ganancias basado en los ingresos mensuales."""
        ganancia_neta_imponible = ingresos_mensuales * 12  # Proyectamos a la ganancia anual
        
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
        
        retencion = Decimal('0.00')
        for limite_inferior, limite_superior, cuota_fija, porcentaje in tramos:
            if ganancia_neta_imponible > limite_inferior:
                exceso = min(ganancia_neta_imponible, limite_superior) - limite_inferior
                retencion += cuota_fija + (exceso * porcentaje)
            else:
                break

        return retencion.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def calcular_iva(self, ingresos_mensuales):
        """Calcula el IVA en base a los ingresos mensuales."""
        iva = ingresos_mensuales * Decimal('0.21')
        return iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def ajustar_si_fin_de_semana(self, fecha):
        """Ajusta la fecha si cae en fin de semana (sábado o domingo)."""
        while fecha.weekday() > 4:  # 5 es sábado, 6 es domingo
            fecha -= timedelta(days=1)
        return fecha

    def calcular_vencimiento_ganancias(self):
        """Calcula la fecha de vencimiento ajustada para el impuesto a las ganancias."""
        hoy = date.today()
        ultimo_dia_mes = calendar.monthrange(hoy.year, hoy.month)[1]  # Último día del mes
        vencimiento = hoy.replace(day=min(30, ultimo_dia_mes))
        return self.ajustar_si_fin_de_semana(vencimiento)

    def calcular_vencimiento_monotributo(self):
        """Calcula la fecha de vencimiento del monotributo (día 20 de cada mes)."""
        vencimiento = date.today().replace(day=20)
        return self.ajustar_si_fin_de_semana(vencimiento)

    def calcular_vencimiento_iva(self):
        """Calcula la fecha de vencimiento del IVA (día 15 de cada mes)."""
        vencimiento = date.today().replace(day=15)
        return self.ajustar_si_fin_de_semana(vencimiento)