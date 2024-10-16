from datetime import date, datetime

from .models import Ingreso
from .repository import IngresosRepository


# Servicio que va ser utilizado por el controlador
class IngresosService:
    def crear_ingreso(
        self, usuario_id, monto, origen, categoria, descripcion="", fecha=None
    ):
        if fecha is None:
            fecha = date.today()

        nuevo_ingreso = Ingreso(
            usuario_id=usuario_id,
            monto=monto,
            origen=origen,
            fecha=fecha,
            categoria=categoria,
            descripcion=descripcion,
        )
        return IngresosRepository.guardar_ingreso(nuevo_ingreso)

    def obtener_ingresos_usuario(self, usuario_id) -> dict:
        return IngresosRepository.obtener_ingresos_usuario(usuario_id)

    def obtener_ingresos_totales(self, usuario_id) -> dict:
        return IngresosRepository.obtener_ingresos_totales(usuario_id)

    def obtener_ingresos_de_un_mes(self, usuario_id, mes, anio) -> dict:
        return IngresosRepository.obtener_ingresos_de_un_mes(usuario_id, mes, anio)

    def obtener_ingresos_de_un_anio(self, usuario_id, anio) -> dict:
        return IngresosRepository.obtener_ingresos_de_un_anio(usuario_id, anio)

    def obtener_ingreso_usuario(self, usuario_id, ingreso_id):
        return IngresosRepository.obtener_ingreso_usuario(usuario_id, ingreso_id)

    def obtener_ingreso_total_en_un_anio(self, usuario_id, anio) -> dict:
        return IngresosRepository.obtener_ingreso_total_en_un_anio(usuario_id, anio)

    def obtener_ingreso_total_en_un_mes(self, usuario_id, mes, anio) -> dict:
        return IngresosRepository.obtener_ingreso_total_en_un_mes(usuario_id, mes, anio)
