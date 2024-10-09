from django.db import models

from Usuario.models import CustomUser


# El modelo nos permite representar la entidad, sus atributos y relaciones
class Ingreso(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    origen = models.CharField(max_length=255)
    fecha = models.DateField()
    usuario_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
