from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .views import MarcaViewSet, TipoBebidaViewSet, ProductoViewSet, UbicacionViewSet, ProductoUbicacionViewSet

router = DefaultRouter()
#router.register(r'clientes', ClienteViewSet)
#router.register(r'usuarios', UsuarioViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'tipos_bebida', TipoBebidaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ubicaciones', UbicacionViewSet)
router.register(r'producto_ubicaciones', ProductoUbicacionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    #path('api/crear-trabajador/', CrearTrabajadorView.as_view(), name='crear_trabajador'),

]
