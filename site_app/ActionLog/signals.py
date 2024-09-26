from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ActionLog, PagoColaborador
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def user_log(sender, instance, created, **kwargs):
    if created:
        ActionLog.objects.create(
            user=instance,
            action='User Created',
            details=f'Usuario {instance.nombre} {instance.apellido} creado.'
        )
    else:
# Obtenemos los valores originales del objeto antes de la edición
old_instance = sender.objects.get(pk=instance.pk)
changes = []

# Comparar cada campo que desees rastrear
if old_instance.nombre != instance.nombre:
    changes.append({
        'field': 'nombre',
        'old_value': old_instance.nombre,
        'new_value': instance.nombre
    })
if old_instance.apellido != instance.apellido:
    changes.append({
        'field': 'apellido',
        'old_value': old_instance.apellido,
        'new_value': instance.apellido
    })
if old_instance.correo != instance.correo:
    changes.append({
        'field': 'correo',
        'old_value': old_instance.correo,
        'new_value': instance.correo
    })
if old_instance.telefono != instance.telefono:
    changes.append({
        'field': 'telefono',
        'old_value': old_instance.telefono,
        'new_value': instance.telefono
    })
if old_instance.password != instance.password:
    changes.append({
        'field': 'password',
        'old_value': '*******', 
        'new_value': '*******'   
    })
if old_instance.pais_residencia != instance.pais_residencia:
    changes.append({
        'field': 'pais_residencia',
        'old_value': old_instance.pais_residencia,
        'new_value': instance.pais_residencia
    })
if old_instance.redes_sociales != instance.redes_sociales:
    changes.append({
        'field': 'redes_sociales',
        'old_value': old_instance.redes_sociales,
        'new_value': instance.redes_sociales
    })

# Si hay cambios, los registramos en ActionLog
if changes:
    details = "; ".join([f"Campo '{change['field']}' cambiado de '{change['old_value']}' a '{change['new_value']}'" for change in changes])
    
    ActionLog.objects.create(
        user=instance,
        action='User Updated',
        details=f'Perfil de usuario {instance.nombre} {instance.apellido} actualizado. Cambios: {details}'
    )


@receiver(post_save, sender=PagoColaborador)
def create_payment_log(sender, instance, created, **kwargs):
    if created:  
        ActionLog.objects.create(
            user=instance.colaborador_id.usuario,  
            action='Payment Made to collaborator',
            details=f'Pago de {instance.monto} realizado a {instance.colaborador_id.nombre} en fecha {instance.fecha_pago}.'
        )
