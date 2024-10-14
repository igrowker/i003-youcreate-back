from django.contrib.auth import get_user

from Colaborador.models import Colaborador
from Colaborador.views import crear_colaborador
from .models import PagoColaborador


class PagosColaboradoresService:
    def registrar_pago(
        self,
        request,
        colaborador_id,
        nombre,
        monto,
        fecha_pago,
        descripcion,
        metodo_pago,
    ):
        user = request.user
        name = user.nombre

        colaborador = Colaborador.objects.filter(id=colaborador_id).first()
        # Si no existe el colaborador, lo crea
        if colaborador is None:
            colaborador_data = {
                # "id": colaborador_id, # ID es creado por la BD
                "nombre": name,
                "usuario": user,
            }

            # Crea el nuevo colaborador y lo asigna como el colaborador para el pago
            nuevo_colaborador = crear_colaborador(colaborador_data, request.user, context={"request": request})
            print("nuevo colaborador", nuevo_colaborador)
            colaborador = nuevo_colaborador

        pago = PagoColaborador(
            colaborador_id=colaborador,
            nombre=nombre,
            monto=monto,
            fecha_pago=fecha_pago,
            descripcion=descripcion,
            metodo_pago=metodo_pago,
        )
        pago.save()
        return pago

    def actualizar_pago(
        pago_id,
        nombre=None,
        monto=None,
        fecha_pago=None,
        descripcion=None,
        metodo_pago=None,
    ):
        try:
            pago = PagoColaborador.objects.get(id=pago_id)
            if nombre is not None:
                pago.nombre = nombre
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

    def obtener_historial_pagos(colaborador_id):
        return PagoColaborador.objects.filter(colaborador_id=colaborador_id).order_by(
            "-fecha_pago"
        )

    def eliminar_pago(pago_id):
        try:
            pago = PagoColaborador.objects.get(id=pago_id)
            pago.delete()
            return True
        except PagoColaborador.DoesNotExist:
            return False
