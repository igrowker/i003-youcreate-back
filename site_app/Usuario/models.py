from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(unique=True, max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    verificado = models.BooleanField(default=False)
    pais_residencia = models.CharField(max_length=255)
    redes_sociales = models.JSONField()
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["username", "nombre", "apellido", "pais_residencia", "password", "redes_sociales"]

    class Meta:
        db_table = "auth_user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
