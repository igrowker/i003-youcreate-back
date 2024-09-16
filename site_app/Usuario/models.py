from django.db import models
# from django.contrib.auth.hashers import make_password

# TODO: Check possibility of using the django make_password() function to encrypt passwords
#  check_password() function to verify them


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(unique=True, max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    verificado = models.BooleanField(default=False)
    pais_residencia = models.CharField(max_length=255)
    redes_sociales = models.JSONField()
