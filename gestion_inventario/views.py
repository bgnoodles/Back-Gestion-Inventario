from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cliente, Usuario, Marca, TipoBebida, Producto, Ubicacion, ProductoUbicacion
from .serializers import ClienteSerializer, UsuarioSerializer, MarcaSerializer, TipoBebidaSerializer, ProductoSerializer, UbicacionSerializer, ProductoUbicacionSerializer, RegistroUsuarioSerializer

# Create your views here.
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class RegistroUsuarioView(generics.CreateAPIView):
    serializer_class = RegistroUsuarioSerializer

    def perform_create(self, serializer):
        # El usuario se asignará automáticamente a la empresa del admin que lo crea
        cliente = self.request.user.usuario.cliente  # Obtén la empresa del admin
        # Se asume que 'admin' es el rol que debe tener el primer usuario (admin de la empresa)
        rol = "admin" if Usuario.objects.filter(cliente=cliente).count() == 0 else "trabajador"
        
        usuario = serializer.save()
        # Asignamos la empresa y el rol al usuario
        usuario.cliente = cliente
        usuario.rol = rol
        usuario.save()

        return usuario

class CrearTrabajadorView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Solo los administradores pueden crear trabajadores

    def perform_create(self, serializer):
        # El trabajador será asignado a la empresa del admin
        cliente = self.request.user.usuario.cliente  # Obtener la empresa del admin
        usuario = serializer.save(cliente=cliente, rol="trabajador")
        return usuario

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class TipoBebidaViewSet(viewsets.ModelViewSet):
    queryset = TipoBebida.objects.all()
    serializer_class = TipoBebidaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class ProductoUbicacionViewSet(viewsets.ModelViewSet):
    queryset = ProductoUbicacion.objects.all()
    serializer_class = ProductoUbicacionSerializer

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Esta es una vista protegida, sólo accesible para usuarios autenticados"})