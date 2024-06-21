from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'carro-de-compras', CarroDeComprasViewSet)
router.register(r'promociones', PromocionViewSet)
router.register(r'historial-compras', HistorialComprasViewSet)
router.register(r'notas-credito', NotaCreditoViewSet)
router.register(r'usuarios', UserViewSet)
router.register(r'bodegas', BodegaViewSet)
router.register(r'documentos', DocumentoViewSet, basename='documentos')

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('bodegas-desactivadas/', BodegaDeshabilitadaListView.as_view(), name='bodegas-desactivadas'),
    path('promociones-desactivadas/', PromocionViewSet.as_view({'get': 'list_inactive'}), name='promociones-desactivadas'),
    path('productos-vigentes/', PromocionViewSet.as_view({'get': 'productos_vigentes'}), name='productos-vigentes'),
    path('ventas/confirmar/', VentaViewSet.as_view({'post': 'confirmar_venta'}), name='confirmar-venta'),
    path('ventas/<int:pk>/documento/', VentaViewSet.as_view({'get': 'obtener_documento'}), name='obtener-documento'),
    path('reportes/ventas/<str:fecha_inicio>/<str:fecha_fin>/', ventas_por_fecha),
    path('clientes/<str:rut>/historial/', historial_compras_cliente, name='historial-compras-cliente')
]
