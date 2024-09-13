from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

class ObligacionFiscal(models.Model):
    tipo_impuesto = models.CharField(max_length=255)
    monto_a_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    usuario_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_impuesto} - {self.monto_a_pagar} - {self.fecha_vencimiento}"