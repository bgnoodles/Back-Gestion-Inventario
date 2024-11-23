from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Producto,Cliente,Usuario,Marca,TipoBebida,Ubicacion,ProductoUbicacion

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_cliente', 'email', 'telefono', 'direccion']

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Obtener el cliente (empresa) que se pasa en el registro
        cliente = validated_data['cliente']

        # Comprobar si es el primer usuario, asignando el rol de "admin" si lo es
        if Usuario.objects.filter(cliente=cliente).count() == 0:
            rol = "admin"  # Asignar rol de administrador al primer usuario
        else:
            rol = "trabajador"  # Asignar rol de trabajador a los demás usuarios

        # Crear el usuario en el modelo Usuario con el rol correspondiente
        usuario = Usuario.objects.create(
            user=user,
            cliente=cliente, 
            rol=rol
        )

        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True) 
    class Meta:
        model = Usuario
        fields = ['id', 'user', 'rol', 'cliente']

class MarcaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Marca
        fields = ['id', 'nombre_marca']

class TipoBebidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoBebida
        fields = ['id', 'nombre_tipo']

class ProductoSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer()
    tipo_bebida = TipoBebidaSerializer()
    class Meta:
        model = Producto
        fields = ['id','nombre_producto','marca','tipo_bebida','stock','precio_base']

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = ['id','numero_pasillo','numero_repisa','capacidad_maxima']

class ProductoUbicacionSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    ubicacion = UbicacionSerializer()
    class Meta:
        model = ProductoUbicacion
        fields = ['id','producto','ubicacion','cantidad']

