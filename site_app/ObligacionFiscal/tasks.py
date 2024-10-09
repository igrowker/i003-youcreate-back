from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone

from .models import ObligacionFiscal


# Tarea compartida para Celery

def enviar_notificacion_vencimiento():
    hoy = timezone.now().date()
    fecha_inicio = hoy
    fecha_limite = hoy + timedelta(days=5) # Notificar 5 días antes del vencimiento
    
    # Filtrar obligaciones que vencen pronto, no han sido pagadas, y no se notificaron hoy
    obligaciones = ObligacionFiscal.objects.filter(
        fecha_vencimiento__range=(fecha_inicio, fecha_limite),
        estado_pago=False,
        email_automatico=True
    ).exclude(fecha_notificacion=hoy)  # Excluir las que ya fueron notificadas hoy

    print(f"Obligaciones por vencer en 3 días: {obligaciones.count()}")

    for obligacion in obligaciones:
        usuario = obligacion.usuario
        print(f"Enviando correo a {usuario.email} por obligación : {obligacion.tipo_impuesto}")
        enviar_correo_vencimiento(usuario.email, obligacion)

        # Actualizar la fecha de notificación a hoy
        obligacion.fecha_notificacion = hoy
        obligacion.save()

# Función para enviar el correo
def enviar_correo_vencimiento(correo, obligacion):
    try:
        asunto = f"Recordatorio de vencimiento de su obligación fiscal: {obligacion.tipo_impuesto}"
        mensaje = f"""
        Estimado/a {obligacion.usuario.first_name},\n
        Le recordamos que su obligación fiscal correspondiente al impuesto {obligacion.tipo_impuesto}, por un monto de {obligacion.monto_a_pagar}, vence el día {obligacion.fecha_vencimiento}.\n\n
        Para evitar cualquier penalidad, le solicitamos que realice el pago antes de la fecha de vencimiento. Agradecemos su atención a este asunto.\n\n
        Si ya ha realizado el pago, por favor ignore este mensaje.\n\n
        Quedamos a su disposición para cualquier consulta o asistencia que necesite.\n\n
        Atentamente,\n
        YOUCREATE
        """
        send_mail(asunto, mensaje, 'igrowker.you.create@gmail.com', [correo])
        print(f"Correo enviado a {correo}")
    except Exception as e:
        print(f"Error al enviar correo a {correo}: {str(e)}")

