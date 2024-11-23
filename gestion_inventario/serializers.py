from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Producto,Marca,TipoBebida,Ubicacion,ProductoUbicacion

#class ClienteSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Cliente
#        fields = ['id', 'nombre_cliente', 'email', 'telefono', 'direccion']



class MarcaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Marca
        fields = ['id', 'nombre_marca']

class TipoBebidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoBebida
        fields = ['id', 'nombre_tipo']

class ProductoSerializer(serializers.ModelSerializer):
    stock_asignado = serializers.SerializerMethodField()
    get_stock_total = serializers.SerializerMethodField()

    marca = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all())
    tipo_bebida = serializers.PrimaryKeyRelatedField(queryset=TipoBebida.objects.all())

    class Meta:
        model = Producto
        fields = ['id', 'nombre_producto', 'marca', 'tipo_bebida', 'precio_base', 'stock', 'stock_asignado', 'stock_total']

    def get_stock_asignado(self, obj):
        # Calcula el stock asignado sumando las cantidades en ProductoUbicacion
        return ProductoUbicacion.objects.filter(producto=obj).aggregate(total_asignado=Sum('cantidad'))['total_asignado'] or 0

    def get_stock_total(self, obj):
        # Calcula el stock disponible restando el stock asignado del stock total
        return obj.stock + self.get_stock_asignado(obj)


class UbicacionSerializer(serializers.ModelSerializer):
    espacio_disponible = serializers.SerializerMethodField()
    class Meta:
        model = Ubicacion
        fields = ['id','numero_pasillo','numero_repisa','capacidad_maxima','espacio_disponible']
    
    def get_espacio_disponible(self, obj):
        return obj.espacio_disponible

class ProductoUbicacionSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())  # Producto usando PrimaryKeyRelatedField
    ubicacion = serializers.PrimaryKeyRelatedField(queryset=Ubicacion.objects.all())  # Ubicacion usando PrimaryKeyRelatedField

    class Meta:
        model = ProductoUbicacion
        fields = ['id', 'producto', 'ubicacion', 'cantidad']


