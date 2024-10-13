from Colaborador.models import Colaborador
from .models import PagoColaborador
from Colaborador.views import ColaboradorViewSet 
from django.http import Request
from django.contrib.auth import get_user


class PagosColaboradoresService:
    @staticmethod
    def registrar_pago(
        request, colaborador_id, nombre, monto, fecha_pago, descripcion, metodo_pago
    ):
        
        user = get_user(request)
        name = user.nombre 

        try:
            colaborador = Colaborador.objects.get(id=colaborador_id)
        except Colaborador.DoesNotExist:
            colaborador_data = {
                "id": colaborador_id,
                "nombre": name,
            }
            colaborador_view = ColaboradorViewSet.as_view({'post': 'create'})
            simulated_request = Request(data=colaborador_data, method='POST', user=user)

            response = colaborador_view(simulated_request)

            #if response.status_code != status.HTTP_201_CREATED:
           #     raise ValueError("No se pudo crear el colaborador")

            colaborador = Colaborador.objects.get(id=colaborador_id)

            
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

    @staticmethod
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

    @staticmethod
    def obtener_historial_pagos(colaborador_id):
        return PagoColaborador.objects.filter(colaborador_id=colaborador_id).order_by(
            "-fecha_pago"
        )

    @staticmethod
    def eliminar_pago(pago_id):
        try:
            pago = PagoColaborador.objects.get(id=pago_id)
            pago.delete()
            return True
        except PagoColaborador.DoesNotExist:
            return False
