from django.db import models
from Colaborador.models import Colaborador


# Create your models here.
class PagoColaborador(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    colaborador_id = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
   
    def __str__(self):
        return f'{self.colaborador} - {self.monto}'



