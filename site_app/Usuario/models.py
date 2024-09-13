from django.db import models

# Create your models here.
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    password = models.CharField(max_length=255)
    verificado = models.BooleanField(default=False)
    pais_residencia = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)