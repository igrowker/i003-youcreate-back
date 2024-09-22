from .models import ObligacionFiscal

class ObligacionesFiscalesRepository:
    
    def __init__(self, usuario):
        self.usuario = usuario
    
    def obtener_obligaciones_fiscales(self):
        """Obtiene las obligaciones fiscales del usuario"""
        return ObligacionFiscal.objects.filter(usuario_id=self.usuario.id)

    def guardar_obligacion(self, tipo_impuesto, monto_a_pagar, fecha_vencimiento):
        # Verificar si ya existe una obligación del mismo tipo en el mes actual
        obligaciones_existentes = ObligacionFiscal.objects.filter(
            usuario_id=self.usuario,
            tipo_impuesto=tipo_impuesto,
            fecha_vencimiento__year=fecha_vencimiento.year,
            fecha_vencimiento__month=fecha_vencimiento.month
        )
        
        if obligaciones_existentes.exists():
            print(f"Obligación fiscal para {tipo_impuesto} ya existe para este mes.")
            return obligaciones_existentes.first()  # Retorna el registro existente
        
        # Si no existe, crea un nuevo registro
        obligacion = ObligacionFiscal.objects.create(
            usuario_id=self.usuario,
            tipo_impuesto=tipo_impuesto,
            monto_a_pagar=monto_a_pagar,
            fecha_vencimiento=fecha_vencimiento
        )
        print(f"Obligación fiscal guardada: {obligacion}")
        return obligacion