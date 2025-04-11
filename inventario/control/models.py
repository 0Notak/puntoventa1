from django.db import models

class Jugo(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    @property
    def total(self):
        return sum(detalle.subtotal for detalle in self.detalleventa_set.all())

    def __str__(self):
        return f'Venta {self.id} - {self.sucursal.nombre} - {self.fecha}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    jugo = models.ForeignKey(Jugo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        return f'{self.jugo.nombre} - {self.cantidad} unidades'
