from datetime import date

from .models import ObligacionFiscal


class ObligacionesFiscalesRepository:
    def __init__(self, usuario):
        self.usuario = usuario

    def obtener_obligaciones_fiscales(self):
        """Obtiene las obligaciones fiscales del usuario."""
        return ObligacionFiscal.objects.filter(usuario=self.usuario)

    def guardar_obligacion(
        self,
        tipo_impuesto,
        monto_a_pagar,
        fecha_vencimiento,
        estado_pago=False,
        email_automatico=False,
    ):
        """
        Guarda o actualiza una obligación fiscal según las siguientes reglas:
        1. Crea un registro si no hay registro en el mes.
        2. Si ya hay un registro, verifica la fecha de vencimiento y crea un nuevo registro si se ha pasado de la fecha.
        3. Si cambia el estado de 'estado_pago' o 'email_automatico', actualiza el registro existente.
        """
        # Verificar si ya existe una obligación del mismo tipo en el mes actual
        obligaciones_existentes = ObligacionFiscal.objects.filter(
            usuario=self.usuario,
            tipo_impuesto=tipo_impuesto,
            fecha_vencimiento__year=fecha_vencimiento.year,
            fecha_vencimiento__month=fecha_vencimiento.month,
        )

        # Si hay obligaciones existentes
        if obligaciones_existentes.exists():
            obligacion = obligaciones_existentes.first()

            # Verificar si se ha pasado la fecha de vencimiento
            if obligacion.fecha_vencimiento < date.today():
                # Se ha pasado la fecha de vencimiento, crear nuevo registro y mantener el anterior
                nueva_obligacion = ObligacionFiscal.objects.create(
                    usuario=self.usuario,
                    tipo_impuesto=tipo_impuesto,
                    monto_a_pagar=monto_a_pagar,
                    fecha_vencimiento=fecha_vencimiento,
                    estado_pago=estado_pago,
                    email_automatico=email_automatico,
                )
                return nueva_obligacion

            # Si el estado_pago cambia, actualizar la obligación existente
            if obligacion.estado_pago != estado_pago:
                obligacion.estado_pago = estado_pago
                obligacion.save(update_fields=["estado_pago"])

            # Si el email_automatico cambia, actualizar la obligación existente
            if obligacion.email_automatico != email_automatico:
                obligacion.email_automatico = email_automatico
                obligacion.save(update_fields=["email_automatico"])

            return obligacion

        # Si no existe, crear un nuevo registro
        nueva_obligacion = ObligacionFiscal.objects.create(
            usuario=self.usuario,
            tipo_impuesto=tipo_impuesto,
            monto_a_pagar=monto_a_pagar,
            fecha_vencimiento=fecha_vencimiento,
            estado_pago=estado_pago,
            email_automatico=email_automatico,
        )

        return nueva_obligacion
