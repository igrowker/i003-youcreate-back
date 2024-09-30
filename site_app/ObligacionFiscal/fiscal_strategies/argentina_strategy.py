from .strategy import ObligacionesFiscalesStrategy  # Importa una clase base que establece cómo se deben calcular las obligaciones fiscales.
from ..repositories import ObligacionesFiscalesRepository  # Importa algo que maneja cómo guardar información de las obligaciones fiscales.
from decimal import Decimal, ROUND_HALF_UP  # Importa herramientas para manejar números con decimales y redondearlos correctamente.
from datetime import date, timedelta  # Importa funciones para manejar fechas y periodos de tiempo.
import calendar  # Importa una herramienta que trabaja con los calendarios.
from Ingreso.models import Ingreso  # Importa el modelo de ingresos del usuario.


class ArgentinaFiscalStrategy(ObligacionesFiscalesStrategy):
    """Estrategia para las obligaciones fiscales en Argentina."""

    def __init__(self, usuario):
        # Inicializa la estrategia con un usuario y crea un repositorio para manejar las obligaciones fiscales de ese usuario
        self.usuario = usuario
        self.repositorio = ObligacionesFiscalesRepository(usuario)  # Asocia un repositorio para el manejo de obligaciones fiscales del usuario

    def calcular_obligaciones(self, monotributo=False):
        """Calcula y guarda las obligaciones fiscales del usuario según si es monotributista o no."""
        ingresos_mensuales = self.obtener_ingresos_mensuales()  # Calcula los ingresos mensuales promedio del usuario
        meses_registrados = self.contar_meses_registrados()  # Cuenta cuántos meses del año se han registrado ingresos

        
        # Verifica si el usuario es monotributista basado en el argumento monotributo o en el perfil del usuario
        if monotributo is not None:
            es_monotributista = monotributo
        else:
            es_monotributista = self.usuario.monotributo

        if es_monotributista:
            # Si el usuario es monotributista y tiene meses registrados con ingresos, calcula sus obligaciones de monotributo
            if meses_registrados > 0:
                ingresos_anuales_estimados = (ingresos_mensuales / meses_registrados) * 12  # Estima los ingresos anuales a partir de los ingresos mensuales
                cuota_monotributo = self.calcular_cuota_monotributo(ingresos_anuales_estimados)  # Calcula cuánto debe pagar de monotributo según sus ingresos anuales
                if cuota_monotributo:
                    vencimiento_monotributo = self.calcular_vencimiento_monotributo()
                    # Verificar si la obligación ya existe
                    if not self.repositorio.obtener_obligaciones_fiscales().filter(tipo_impuesto='Monotributo', fecha_vencimiento=vencimiento_monotributo).exists():
                        self.repositorio.guardar_obligacion(
                            tipo_impuesto='Monotributo',
                            monto_a_pagar=cuota_monotributo,
                            fecha_vencimiento=vencimiento_monotributo
                        )


            # También calcula y guarda el impuesto a las ganancias si aplica
            ganancias = self.calcular_retencion_ganancias(ingresos_mensuales)  # Calcula la retención de ganancias
            if ganancias:
                vencimiento_ganancias = self.calcular_vencimiento_ganancias()  # Calcula la fecha de vencimiento para el pago de ganancias
                if not self.repositorio.obtener_obligaciones_fiscales().filter(tipo_impuesto='Impuesto a las Ganancias', fecha_vencimiento=vencimiento_ganancias).exists():
                    self.repositorio.guardar_obligacion(
                        tipo_impuesto='Impuesto a las Ganancias',
                        monto_a_pagar=ganancias,
                        fecha_vencimiento=vencimiento_ganancias
                    )
        else:
            # Si el usuario no es monotributista, calcular IVA y Ganancias
            if meses_registrados > 0:
                iva = self.calcular_iva(ingresos_mensuales)  # Calcula el IVA sobre los ingresos mensuales
                if iva:
                    vencimiento_iva = self.calcular_vencimiento_iva()  # Calcula la fecha de vencimiento del IVA
                    if not self.repositorio.obtener_obligaciones_fiscales().filter(tipo_impuesto='IVA', fecha_vencimiento=vencimiento_iva).exists():
                        self.repositorio.guardar_obligacion(
                            tipo_impuesto='IVA',
                            monto_a_pagar=iva,
                            fecha_vencimiento=vencimiento_iva
                        )

                #También calcula y guarda el impuesto a las ganancias
                ganancias = self.calcular_retencion_ganancias(ingresos_mensuales)
                if ganancias:
                    vencimiento_ganancias = self.calcular_vencimiento_ganancias()
                    if not self.repositorio.obtener_obligaciones_fiscales().filter(tipo_impuesto='Impuesto a las Ganancias', fecha_vencimiento=vencimiento_ganancias).exists():
                        self.repositorio.guardar_obligacion(
                            tipo_impuesto='Impuesto a las Ganancias',
                            monto_a_pagar=ganancias,
                            fecha_vencimiento=vencimiento_ganancias
                        )

    # --- Métodos Auxiliares ---
    
    def obtener_ingresos_mensuales(self):
        """Calcula los ingresos mensuales promedio del usuario, sumando los ingresos registrados en el año actual y dividiendo entre los meses con ingresos."""
        ingresos_totales = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year)  # Filtra los ingresos del año actual
        if ingresos_totales.exists():  # Si hay ingresos registrados
            total_ingresos = sum(ingreso.monto for ingreso in ingresos_totales)  # Suma todos los ingresos
            meses_registrados = self.contar_meses_registrados()  # Cuenta los meses con ingresos
            if meses_registrados > 0:
                ingresos_mensuales_promedio = total_ingresos / meses_registrados  # Calcula el promedio mensual
                return ingresos_mensuales_promedio
        return 0  # Si no hay ingresos registrados, retorna 0


    def contar_meses_registrados(self):
        """Cuenta cuántos meses del año actual tienen ingresos registrados."""
        ingresos_totales = Ingreso.objects.filter(usuario_id=self.usuario, fecha__year=date.today().year)  # Filtra los ingresos del año actual
        meses_registrados = len(set(ingreso.fecha.month for ingreso in ingresos_totales))  # Crea un conjunto con los meses y cuenta cuántos diferentes hay
        return meses_registrados


    def calcular_cuota_monotributo(self, ingresos_anuales_estimados):
        """Calcula la cuota de monotributo en base a los ingresos anuales estimados."""
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
        
        escala = [
            (1900000, Decimal('54149.99')),
            (2000000, Decimal('10939.98')),
            (2100000, Decimal('19879.97')),
            (2200000, Decimal('30799.96')),
            (2300000, Decimal('44141.80')),
            (2400000, Decimal('61979.36')),
            (2500000, Decimal('80979.36')),
            (2600000, Decimal('100079.35')),
            (2700000, Decimal('118979.36')),
            (2800000, Decimal('138817.12')),
            (2900000, Decimal('158654.88')),
            (3000000, Decimal('178492.64')),
            (3100000, Decimal('198330.40')),
            (3200000, Decimal('218168.16')),
            (3300000, Decimal('238005.92')),
            (3400000, Decimal('257843.68')),
            (3500000, Decimal('277681.44')),
        ]
        
        # Encontramos el importe según la escala de ingresos mensuales
        retencion = Decimal('0.00')# Inicializa la retención como 0
        for ingreso_bruto, importe in escala:
            if ingresos_mensuales <= ingreso_bruto:# Si los ingresos mensuales caen en un tramo de la escala
                retencion = importe
                break
        else:
            # Si los ingresos superan el último rango, tomamos la última retención
            retencion = escala[-1][1]
        
        # Redondeamos la retención a dos decimales
        return retencion.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def calcular_iva(self, ingresos_mensuales):
        """Calcula el IVA en base a los ingresos mensuales."""
        # El IVA se calcula como el 21% de los ingresos mensuales
        iva = ingresos_mensuales * Decimal('0.21')
        return iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)# Redondea el valor del IVA a dos decimales usando la regla de redondeo estándar

    def ajustar_si_fin_de_semana(self, fecha):
        """Ajusta la fecha de vencimiento si cae en fin de semana. Mueve la fecha al último día hábil anterior si cae en sábado o domingo."""
        # Si la fecha es un sábado (weekday() devuelve 5) o un domingo (weekday() devuelve 6),
        # resta días hasta que sea un día de semana (lunes a viernes, weekday() <= 4)
        while fecha.weekday() > 4:  # 5 es sábado, 6 es domingo
            fecha += timedelta(days=1)# Avanza un día hasta que sea lunes (día hábil)
        return fecha

    def calcular_vencimiento_ganancias(self):
        """Calcula la fecha de vencimiento del impuesto a las ganancias, que es el día 20 de cada mes. Si el día 20 cae en fin de semana, ajusta la fecha al día hábil siguiente."""
        # Fija el vencimiento en el día 20 del mes actual
        if date.today().day > 20:
            # Si hoy es después del día 20, establece el vencimiento para el mes siguiente
            vencimiento = (date.today().replace(day=1) + timedelta(days=32)).replace(day=20)  # Primer día del siguiente mes
        else:
            vencimiento = date.today().replace(day=20)

        # Ajusta la fecha si cae en fin de semana
        return self.ajustar_si_fin_de_semana(vencimiento)


    def calcular_vencimiento_monotributo(self):
        """Calcula la fecha de vencimiento del monotributo, que es el día 20 de cada mes. Si el día 20 cae en fin de semana, ajusta la fecha al día hábil siguiente."""
        # Fija el vencimiento en el día 20 del mes actual
        if date.today().day > 20:
            # Si hoy es después del día 20, establece el vencimiento para el mes siguiente
            vencimiento = (date.today().replace(day=1) + timedelta(days=32)).replace(day=20)
        else:
            vencimiento = date.today().replace(day=20)

        # Ajusta la fecha si cae en fin de semana
        return self.ajustar_si_fin_de_semana(vencimiento)


    def calcular_vencimiento_iva(self):
        """Calcula la fecha de vencimiento del IVA, que es el día 20 de cada mes. Si el día 20 cae en fin de semana, ajusta la fecha al día hábil siguiente."""
        # Fija el vencimiento en el día 20 del mes actual
        if date.today().day > 20:
            # Si hoy es después del día 20, establece el vencimiento para el mes siguiente
            vencimiento = (date.today().replace(day=1) + timedelta(days=32)).replace(day=20)
        else:
            vencimiento = date.today().replace(day=20)

        # Ajusta la fecha si cae en fin de semana
        return self.ajustar_si_fin_de_semana(vencimiento)
