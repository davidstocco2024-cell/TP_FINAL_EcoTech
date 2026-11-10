from django.db import models

class ConsumoPlanta(models.Model):
    nombre = models.CharField(max_length=100)
    consumo_kwh = models.FloatField()

    def __str__(self):
        return f"{self.nombre} - {self.consumo_kwh} kWh"