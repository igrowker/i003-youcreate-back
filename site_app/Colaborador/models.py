from django.db import models

from Usuario.models import CustomUser


class Colaborador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    servicio = models.CharField(max_length=255, null=True, blank=True)
    monto = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.servicio}"
