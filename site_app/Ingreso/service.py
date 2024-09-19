from .repository import IngresosRepository
#Servicio que va ser utilizado por el controlador
class IngresosService:
    def obtener_ingresos_usuario(self, usuario_id) -> dict:
        ingresos = self.ingresos_repository.obtener_ingresos_usuario(usuario_id)
        #inicializo dict para agregar ingresos por origen 
        ingresos_por_origen = {}
        #par cada uno de los ingresos del array 
        for ingreso in ingresos:
            #si el origen del ingreso actual no esta en el dict 
            if ingreso.origen not in ingresos_por_origen:
                #si no esta se inicializa con valor 0
                ingresos_por_origen[ingreso.origen] = 0
            #sumo el monto del ingreso al valor actual de dict 
            ingresos_por_origen[ingreso.origen] += ingreso.monto
        return ingresos_por_origen

    def obtener_ingresos_totales(self, usuario_id) -> dict:
        return self.ingresos_repository.obtener_ingresos_totales(usuario_id)
    
    def obtener_ingresos_por_fecha(self, usuario_id) -> dict:
        return self.ingresos_repository.obtener_ingresos_por_fecha(usuario_id)