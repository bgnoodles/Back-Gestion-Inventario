from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission, User

# Create your models here.


class Marca(models.Model):
    nombre_marca = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_marca

class TipoBebida(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_tipo

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=45)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="productos")
    tipo_bebida = models.ForeignKey(TipoBebida, on_delete=models.CASCADE, related_name="productos")
    stock = models.IntegerField(default=0) 
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
        
    def __str__(self):
        return self.nombre_producto


class Ubicacion(models.Model):
    numero_pasillo = models.CharField(max_length=15)
    numero_repisa = models.CharField(max_length=15)
    capacidad_maxima = models.IntegerField()

    def __str__(self):
        return f"Pasillo {self.numero_pasillo}, Repisa {self.numero_repisa}"
    
    @property
    def espacio_disponible(self):
        ocupacion_total = ProductoUbicacion.objects.filter(ubicacion=self).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        return self.capacidad_maxima - ocupacion_total

class ProductoUbicacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def save(self, *args, **kwargs):
        # Valida el espacio disponible en la ubicación
        espacio_disponible = self.ubicacion.espacio_disponible
        if self.cantidad > espacio_disponible:
            raise ValidationError(
                f"No se puede asignar {self.cantidad} unidades a esta ubicación. "
                f"Espacio disponible: {espacio_disponible} unidades."
            )

        # Calcula la suma actual de las cantidades en ubicaciones para este producto
        total_asignado = ProductoUbicacion.objects.filter(producto=self.producto).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        # Calcula el nuevo total después de esta asignación
        nuevo_total = total_asignado + self.cantidad

        # Valida que no exceda el stock disponible del producto
        if nuevo_total > self.producto.stock:
            raise ValidationError(
                f"La cantidad total asignada ({nuevo_total}) supera el stock disponible ({self.producto.stock})."
            )
        
        # Reduce el stock del producto antes de guardar
        self.producto.stock -= self.cantidad
        self.producto.save()

        # Si todo está bien, guarda el registro
        super().save(*args, **kwargs)

