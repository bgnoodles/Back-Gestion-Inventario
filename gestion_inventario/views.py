from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, serializers
from .permissions import IsAdmin
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Marca, TipoBebida, Producto, Ubicacion, ProductoUbicacion
from .serializers import MarcaSerializer, TipoBebidaSerializer, ProductoSerializer, UbicacionSerializer, ProductoUbicacionSerializer

# Create your views here.


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
    def get_queryset(self):
        
        return super().get_queryset()

class ProductoUbicacionViewSet(viewsets.ModelViewSet):
    queryset = ProductoUbicacion.objects.all()
    serializer_class = ProductoUbicacionSerializer
