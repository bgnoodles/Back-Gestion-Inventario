from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

# Create your models here.
class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField()

    def __str__(self):
        return self.nombre_cliente
    
class Usuario(AbstractUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False,blank=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="usuarios")
    rol = models.CharField(max_length=50, choices=[("admin", "Admin"),("trabajador","Trabajador")])
    groups = models.ManyToManyField(Group,related_name="usuario_set",blank=True)

    user_permissions = models.ManyToManyField(Permission, related_name="usuario_set", blank=True)

    def __str__(self):
        return self.username

class Marca(models.Model):
    nombre_marca = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="marcas")
    
    def __str__(self):
        return self.nombre_marca

class TipoBebida(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="tipos_bebida")
    
    def __str__(self):
        return self.nombre_tipo

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=45)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="productos")
    tipo_bebida = models.ForeignKey(TipoBebida, on_delete=models.CASCADE, related_name="productos")
    stock = models.IntegerField(default=0) 
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="productos")
        
    def __str__(self):
        return self.nombre_producto

class Ubicacion(models.Model):
    numero_pasillo = models.CharField(max_length=15)
    numero_repisa = models.CharField(max_length=15)
    capacidad_maxima = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ubicacion")

    def __str__(self):
        return self.numero_pasillo, self.numero_repisa

class ProductoUbicacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    cantidad = models.IntegerField()


