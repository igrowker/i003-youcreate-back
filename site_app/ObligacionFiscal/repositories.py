from .models import ObligacionFiscal
from datetime import date

class ObligacionesFiscalesRepository:
    
    def __init__(self, usuario):
        self.usuario = usuario
    
    def obtener_obligaciones_fiscales(self):
        """Obtiene las obligaciones fiscales del usuario"""
        return ObligacionFiscal.objects.filter(usuario_id=self.usuario.id)

    def guardar_obligacion(self, tipo_impuesto, monto_a_pagar, fecha_vencimiento):
        """Guarda una nueva obligación fiscal o verifica si se debe crear una nueva tras el vencimiento"""
        # Verificar si ya existe una obligación del mismo tipo y mes
        obligaciones_existentes = ObligacionFiscal.objects.filter(
            usuario_id=self.usuario,
            tipo_impuesto=tipo_impuesto,
            fecha_vencimiento__year=fecha_vencimiento.year,
            fecha_vencimiento__month=fecha_vencimiento.month
        )
        
        # Verificar si ya pasó la fecha de vencimiento
        hoy = date.today()
        if obligaciones_existentes.exists():
            obligacion_actual = obligaciones_existentes.first()
            
            if hoy <= obligacion_actual.fecha_vencimiento:
                # Si la fecha actual es antes o el mismo día del vencimiento, reutilizamos la obligación existente
                return obligacion_actual
            else:
                # Si la fecha actual ya pasó el vencimiento, ajustamos al siguiente mes
                if fecha_vencimiento <= hoy:
                    # Ajustar el vencimiento al próximo 20 del mes siguiente
                    if hoy.month == 12:
                        fecha_vencimiento = hoy.replace(year=hoy.year + 1, month=1, day=20)
                    else:
                        fecha_vencimiento = hoy.replace(month=hoy.month + 1, day=20)

        # Si no existe o se ajusta al mes siguiente, creamos un nuevo registro
        nueva_obligacion = ObligacionFiscal.objects.create(
            usuario_id=self.usuario,
            tipo_impuesto=tipo_impuesto,
            monto_a_pagar=monto_a_pagar,
            fecha_vencimiento=fecha_vencimiento
        )
        
        return nueva_obligacion