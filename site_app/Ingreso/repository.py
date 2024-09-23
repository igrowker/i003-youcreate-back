from .models import Ingreso
from django.db.models import Sum

#El repositorio es el encargado de interactuar con la base de datos
class IngresosRepository:
    #Devolver todos los ingresos asociados a un usuario
    @staticmethod
    def obtener_ingresos_usuario(usuario_id):
        #retorno un QuerySet, una lista de objetos Ingreso que corresponden a un usuario_id
        return Ingreso.objects.filter(usuario_id=usuario_id)

    #Devolver la suma total de los montos de ingresos para un usuario
    @staticmethod
    def obtener_ingresos_totales(usuario_id):
        #primero se filtran los ingresos correspondientes a un usuario_id, luego aggregate permite calcular la suma total de la columna monto
        return Ingreso.objects.filter(usuario_id=usuario_id)\
            .aggregate(total=Sum('monto'))  
    
    #Devolver los ingresos agrupados por fecha 
    @staticmethod
    def obtener_ingresos_por_fecha(usuario_id):
        #primero se filtran los ingresos correspondientes a un usuario_id, luego seleeccina la columna 'fecha', calcula la suma de los montos por cada fecha y por ultimo ordena por fecha
        return Ingreso.objects.filter(usuario_id=usuario_id) \
            .values('fecha') \
            .annotate(total=Sum('monto')) \
            .order_by('fecha')
    
    #Devolver los ingresos agrupados por mes y año
    @staticmethod
    def obtener_ingresos_por_mes_y_anio(usuario_id, mes, anio):
        #primero se filtran los ingresos correspondientes a un usuario_id por año y por fecha
        return Ingreso.objects.filter(usuario_id=usuario_id, fecha__month=mes, fecha__year=anio)


