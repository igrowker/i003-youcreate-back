from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ActionLog
from django.core.cache import cache

User = get_user_model()

@receiver(pre_save, sender=User)
def cache_old_user_state(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        cache.set(f'user_{instance.pk}_old_state', old_instance)

@receiver(post_save, sender=User)
def user_action_log(sender, instance, created, **kwargs):
    if created:
        ActionLog.objects.create(
            user=instance,
            action='User Created',
            details=f'Usuario {instance.nombre} {instance.apellido} creado.'
        )
    else:
        changes = []
        old_instance = cache.get(f'user_{instance.pk}_old_state')

        if old_instance and old_instance.nombre != instance.nombre:
            changes.append({
                'field': 'nombre',
                'old_value': old_instance.nombre,
                'new_value': instance.nombre
            })
        if old_instance and old_instance.apellido != instance.apellido:
            changes.append({
                'field': 'apellido',
                'old_value': old_instance.apellido,
                'new_value': instance.apellido
            })
        if old_instance and old_instance.correo != instance.correo:
            changes.append({
                'field': 'correo',
                'old_value': old_instance.correo,
                'new_value': instance.correo
            })
        if old_instance and old_instance.telefono != instance.telefono:
            changes.append({
                'field': 'telefono',
                'old_value': old_instance.telefono,
                'new_value': instance.telefono
            })
        if old_instance and old_instance.pais_residencia != instance.pais_residencia:
            changes.append({
                'field': 'pais_residencia',
                'old_value': old_instance.pais_residencia,
                'new_value': instance.pais_residencia
            })
        if old_instance and old_instance.redes_sociales != instance.redes_sociales:
            changes.append({
                'field': 'redes_sociales',
                'old_value': old_instance.redes_sociales,
                'new_value': instance.redes_sociales
            })

        if changes:
            details = "; ".join([f"Campo '{change['field']}' cambiado de '{change['old_value']}' a '{change['new_value']}'"
                                 for change in changes])

            ActionLog.objects.create(
                user=instance,
                action='User Updated',
                details=f'Perfil de usuario {instance.nombre} {instance.apellido} actualizado. Cambios: {details}'
            )