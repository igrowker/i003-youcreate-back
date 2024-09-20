from django.db import models
from Usuario.models import CustomUser



# Modelo ObligacionFiscal, que almacenará la información sobre los impuestos a pagar
class ObligacionFiscal(models.Model):
    tipo_impuesto = models.CharField(max_length=255) # Tipo de impuesto (ej: IVA, Ganancias)
    monto_a_pagar = models.DecimalField(max_digits=10, decimal_places=2)# Monto a pagar
    fecha_vencimiento = models.DateField()# Fecha límite para el pago del impuesto
    usuario_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)# Relación con el usuario

def __str__(self):
        return f"{self.tipo_impuesto} - {self.monto_a_pagar}
