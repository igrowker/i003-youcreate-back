from .repository import IngresosRepository


# Servicio que va ser utilizado por el controlador
class IngresosService:
    def obtener_ingresos_usuario(self, usuario_id) -> dict:
        return IngresosRepository.obtener_ingresos_usuario(usuario_id)

    def obtener_ingresos_totales(self, usuario_id) -> dict:
        return IngresosRepository.obtener_ingresos_totales(usuario_id)

    def obtener_ingresos_por_mes(self, usuario_id, mes) -> dict:
        return IngresosRepository.obtener_ingresos_por_mes(usuario_id, mes)

    def obtener_ingresos_por_anio(self, usuario_id, anio) -> dict:
        return IngresosRepository.obtener_ingresos_por_anio(usuario_id, anio)
