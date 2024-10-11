from .models import PagoColaborador
from Colaborador.models import Colaborador

class PagosColaboradoresService:

    @staticmethod
    def registrar_pago(colaborador_id, nombre, apellido, monto, fecha_pago, descripcion, metodo_pago):
        try:
            colaborador = Colaborador.objects.get(id=colaborador_id)
        except Colaborador.DoesNotExist:
            raise ValueError("El colaborador no existe")

        pago = PagoColaborador(
            colaborador_id=colaborador,
            nombre=nombre,
            apellido=apellido,  
            monto=monto,
            fecha_pago=fecha_pago,
            descripcion=descripcion,
            metodo_pago=metodo_pago  
        )
        pago.save()
        return pago

    @staticmethod
    def actualizar_pago(pago_id, nombre=None, apellido=None, monto=None, fecha_pago=None, descripcion=None, metodo_pago=None):
        try:
            pago = PagoColaborador.objects.get(id=pago_id)
            if nombre is not None:
                pago.nombre = nombre
            if apellido is not None:
                pago.apellido = apellido
            if monto is not None:
                pago.monto = monto
            if fecha_pago is not None:
                pago.fecha_pago = fecha_pago
            if descripcion is not None:
                pago.descripcion = descripcion
            if metodo_pago is not None:
                pago.metodo_pago = metodo_pago
            pago.save()
            return pago
        except PagoColaborador.DoesNotExist:
            return None

    @staticmethod
    def obtener_historial_pagos(colaborador_id):
        return PagoColaborador.objects.filter(colaborador_id=colaborador_id).order_by('-fecha_pago')

    @staticmethod
    def eliminar_pago(pago_id):
        try:
            pago = PagoColaborador.objects.get(id=pago_id)
            pago.delete()
            return True
        except PagoColaborador.DoesNotExist:
            return False
