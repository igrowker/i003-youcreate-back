from .models import Ingreso
from django.db.models import Sum,F

#El repositorio es el encargado de interactuar con la base de datos
class IngresosRepository:

    #Cargo en la base de datos el ingreso pasado por parametro
    @staticmethod
    def guardar_ingreso(ingreso):
        ingreso.save()
        return ingreso

    #Devolver todos los ingresos asociados a un usuario
    @staticmethod
    def obtener_ingresos_usuario(usuario_id):
        #retorno un QuerySet, una lista de objetos Ingreso que corresponden a un usuario_id
        return (Ingreso.objects.filter(usuario_id=usuario_id)
                .values('origen')  # Agrupar por origen
                .annotate(total=Sum('monto'))  # Calcular la suma de los montos
                .order_by('origen'))  # Ordenar por origen

    #Devolver la suma total de los montos de ingresos para un usuario
    @staticmethod
    def obtener_ingresos_totales(usuario_id):
        #primero se filtran los ingresos correspondientes a un usuario_id, luego aggregate permite calcular la suma total de la columna monto
        return (Ingreso.objects.filter(usuario_id=usuario_id)
                .aggregate(total=Sum('monto')) ) 
    
    # Devolver los ingresos agrupados por mes 
    @staticmethod
    def obtener_ingresos_por_mes(usuario_id, mes):
        # Se filtran los ingresos correspondientes a un usuario_id por mes
        return Ingreso.objects.filter(usuario_id=usuario_id, fecha__month=mes)

    # Devolver los ingresos agrupados por año
    @staticmethod
    def obtener_ingresos_por_anio(usuario_id, anio):
    # Agrupar los ingresos por año y calcular el total, renombrando 'fecha__year' a 'anio'
        return (Ingreso.objects.filter(usuario_id=usuario_id, fecha__year=anio)
                .values(anio=F('fecha__year'))
                .annotate(total=Sum('monto'))
                .order_by('anio'))