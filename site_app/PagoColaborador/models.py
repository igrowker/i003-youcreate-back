from django.db import models

from Colaborador.models import Colaborador


class PagoColaborador(models.Model):
    id = models.AutoField(primary_key=True)
    colaborador_id = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)  # models.TextField(null=True)
    # apellido = models.TextField(null=True)
    monto = models.DecimalField(max_digits=100, decimal_places=2)
    fecha_pago = models.DateField()
    descripcion = models.TextField(null=True)
    metodo_pago = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.colaborador_id} - {self.colaborador_id.nombre} - - {self.nombre} - {self.apellido} - {self.fecha_pago} - {self.monto} - {self.metodo_pago}"
