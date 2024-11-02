from django.db import models
from django.utils import timezone

class Experimento(models.Model):
    id_experimento = models.AutoField(primary_key=True)
    nombre_experimento = models.CharField(max_length=100)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre_experimento} - {self.fecha_inicio.strftime('%Y-%m-%d')}"

class Mediciones(models.Model):
    id_medicion = models.AutoField(primary_key=True)
    id_experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE, related_name='mediciones')
    valor = models.FloatField()
    voltaje = models.FloatField()
    voltaje_corregido = models.FloatField()
    concentracion = models.FloatField()
    absorbancia = models.FloatField(default=0.0)
    fecha = models.DateTimeField(default=timezone.now)
    unidad_valor = models.CharField(max_length=20, default='V')

    def __str__(self):
        return (f"ID Experimento: {self.id_experimento}, Valor: {self.valor} {self.unidad_valor}, "
                f"Voltaje: {self.voltaje}, Voltaje corregido: {self.voltaje_corregido}, "
                f"Absorbancia: {self.absorbancia}, Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
