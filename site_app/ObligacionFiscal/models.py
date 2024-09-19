from django.db import models
from Usuario.models import CustomUser


# Create your models here.
class ObligacionFiscal(models.Model):
    tipo_impuesto = models.CharField(max_length=255)
    monto_a_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    usuario_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_impuesto} - {self.monto_a_pagar} - {self.fecha_vencimiento}"
