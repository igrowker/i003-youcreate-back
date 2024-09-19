from django.db import models
from Usuario.models import CustomUser

# Create your models here.
class Colaborador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    servicio = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    usuario_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
