from .models import ObligacionFiscal


class ObligacionesFiscalesRepository:
    def __init__(self, usuario):
        self.usuario = usuario

    def obtener_obligaciones_fiscales(self):
        """Obtiene las obligaciones fiscales del usuario"""
        return ObligacionFiscal.objects.filter(usuario_id=self.usuario)

    def guardar_obligacion(self, tipo_impuesto, monto_a_pagar, fecha_vencimiento):
        """Almacena una nueva obligación fiscal"""
        obligacion = ObligacionFiscal(
            usuario_id=self.usuario,
            tipo_impuesto=tipo_impuesto,
            monto_a_pagar=monto_a_pagar,
            fecha_vencimiento=fecha_vencimiento,
        )
        obligacion.save()
        return obligacion
