from django.db import models
from django.utils import timezone

class SensorData(models.Model):
    id = models.IntegerField(primary_key=True)
    valor = models.FloatField()
    voltaje = models.FloatField()
    voltaje_corregido = models.FloatField()
    absorbancia = models.FloatField(default=0.0)  # Nuevo campo para almacenar la absorbancia
    fecha = models.DateTimeField(default=timezone.now)
    unidad_valor = models.CharField(max_length=20, default='V')

    def __str__(self):
        return f"Valor: {self.valor} {self.unidad_valor}, Voltaje: {self.voltaje}, Voltaje corregido: {self.voltaje_corregido}, Absorbancia: {self.absorbancia}, Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
