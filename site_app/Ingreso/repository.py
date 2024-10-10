from django.db.models import Sum

from .models import Ingreso


# El repositorio es el encargado de interactuar con la base de datos
class IngresosRepository:
    # Cargo en la base de datos el ingreso pasado por parametro
    @staticmethod
    def guardar_ingreso(ingreso):
        ingreso.save()
        return ingreso

    # Devolver todos los ingresos asociados a un usuario
    @staticmethod
    def obtener_ingresos_usuario(usuario_id):
        # retorno un QuerySet, una lista de objetos Ingreso que corresponden a un usuario_id
        return Ingreso.objects.filter(usuario_id=usuario_id)

    # Devolver la suma total de los montos de ingresos para un usuario
    @staticmethod
    def obtener_ingresos_totales(usuario_id):
        # primero se filtran los ingresos correspondientes a un usuario_id, luego aggregate permite calcular la suma total de la columna monto
        return Ingreso.objects.filter(usuario_id=usuario_id).aggregate(
            total=Sum("monto")
        )

    # Devolver los ingresos agrupados de un mes especifico
    @staticmethod
    def obtener_ingresos_de_un_mes(usuario_id, mes, anio):
        return Ingreso.objects.filter(
            usuario_id=usuario_id, fecha__year=anio, fecha__month=mes
        )

    # Devolver los ingresos agrupados de un año especifico
    @staticmethod
    def obtener_ingresos_de_un_anio(usuario_id, anio):
        return Ingreso.objects.filter(usuario_id=usuario_id, fecha__year=anio)

    # Devolver un ingreso especifico de un usuario
    @staticmethod
    def obtener_ingreso_usuario(usuario_id, ingreso_id):
        return Ingreso.objects.get(usuario_id=usuario_id, id=ingreso_id)

    # Devolver el total de ingresos en un mes
    def obtener_ingreso_total_en_un_mes(usuario_id, mes, anio):
        # Se filtran los ingresos correspondientes a un usuario_id por mes y anio (es anio es necesario para no considerar meses de otros anios)
        resultado = Ingreso.objects.filter(
            usuario_id=usuario_id, fecha__month=mes, fecha__year=anio
        ).aggregate(total=Sum("monto"))
        # Verificar si se encontraron ingresos y devolver el resultado en el formato deseado
        total_monto = resultado["total"] if resultado["total"] is not None else 0
        return {mes: total_monto}

    # Devolver el total de ingresos en un anio
    def obtener_ingreso_total_en_un_anio(usuario_id, anio):
        # Filtrar los ingresos por año y sumar los montos
        resultado = Ingreso.objects.filter(
            usuario_id=usuario_id, fecha__year=anio
        ).aggregate(total=Sum("monto"))

        # Verificar si se encontraron ingresos y devolver el resultado en el formato deseado
        total_monto = resultado["total"] if resultado["total"] is not None else 0
        return {anio: total_monto}
