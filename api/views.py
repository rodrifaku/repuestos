from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.estado = False
        instance.save()

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SucursalSerializer

    def get_queryset(self):
        return Sucursal.objects.filter(estado=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({"message": f"Sucursal '{instance.nombre}' deshabilitada correctamente."}, status=status.HTTP_200_OK)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        estado = self.request.query_params.get('estado', 'true').lower() == 'true'
        return Categoria.objects.filter(estado=estado)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            estado = self.request.query_params.get('estado', 'true').lower() == 'true'
            mensaje = "No existe registro activo de categorías." if estado else "No existen categorías deshabilitadas."
            return Response({"message": mensaje}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({"message": f"Categoría '{instance.nombre}' deshabilitada correctamente."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='desactivadas', url_name='desactivadas')
    def list_inactive(self, request):
        queryset = Categoria.objects.filter(estado=False)
        if not queryset.exists():
            return Response({"message": "No existen categorías deshabilitadas."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BodegaSerializer

    def get_queryset(self):
        return Bodega.objects.filter(estado=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No existe registro activo de bodegas."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({"message": f"Bodega '{instance.nombre}' deshabilitada correctamente."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='desactivadas', url_name='desactivadas')
    def list_inactive(self, request):
        queryset = Bodega.objects.filter(estado=False)
        if not queryset.exists():
            return Response({"message": "No existen bodegas deshabilitadas."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class BodegaDeshabilitadaListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BodegaSerializer

    def get_queryset(self):
        return Bodega.objects.filter(estado=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No existen bodegas deshabilitadas."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductoSerializer

    def get_queryset(self):
        estado = self.request.query_params.get('estado', 'true').lower() == 'true'
        return Producto.objects.filter(estado=estado)

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            estado = self.request.query_params.get('estado', 'true').lower() == 'true'
            mensaje = "No existe registro activo de productos." if estado else "No existen productos deshabilitados."
            return Response({"message": mensaje}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({"message": f"Producto '{instance.nombre}' deshabilitado correctamente."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='desactivados', url_name='desactivados')
    def list_inactive(self, request):
        queryset = Producto.objects.filter(estado=False)
        if not queryset.exists():
            return Response({"message": "No existen productos deshabilitados."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='categoria/(?P<categoria_id>\d+)', url_name='list_by_category')
    def list_by_category(self, request, categoria_id=None):
        try:
            categoria = Categoria.objects.get(id=categoria_id)
        except Categoria.DoesNotExist:
            return Response({"message": "Categoría no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = Producto.objects.filter(categoria=categoria, estado=True)
        if not queryset.exists():
            return Response({"message": f"No existen productos activos en la categoría '{categoria.nombre}'."}, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='productos-vigentes', url_name='productos_vigentes')
    def productos_vigentes(self, request):
        today = timezone.now().date()
        promociones = Promocion.objects.filter(fecha_inicio__lte=today, fecha_fin__gte=today, estado=True)
        productos = Producto.objects.filter(promociones__in=promociones).distinct()
        
        if not productos.exists():
            return Response({"message": "No hay productos en promociones vigentes."}, status=status.HTTP_200_OK)
        
        serializer = ProductoPromocionSerializer(productos, many=True)
        return Response(serializer.data)
    
class ClienteViewSet(BaseViewSet):
    queryset = Cliente.objects.filter(estado=True)
    serializer_class = ClienteSerializer




class CarroDeComprasViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CarroDeCompras.objects.all()
    serializer_class = CarroDeComprasSerializer

    def create(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        producto_id = request.data.get('producto')
        cantidad = request.data.get('cantidad')
        producto = Producto.objects.get(id=producto_id)
        precio_unitario = producto.precio

        if producto.stock < cantidad:
            return Response({"detail": f"Producto {producto.nombre} no tiene suficiente stock."}, status=status.HTTP_400_BAD_REQUEST)

        detalle_temp = CarroDeCompras(
            session_id=session_id,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        detalle_temp.save()
        return Response(CarroDeComprasSerializer(detalle_temp).data, status=status.HTTP_201_CREATED)

class VentaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Venta.objects.filter(estado=True)
    serializer_class = VentaSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({"message": "Venta deshabilitada correctamente."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='confirmar')
    def confirmar_venta(self, request):
        session_id = request.data.get('session_id')
        rut_cliente = request.data.get('rut')
        cliente_data = request.data.get('cliente')
        sucursal_id = request.data.get('sucursal')
        vendedor_id = request.data.get('vendedor')
        tipo_documento = request.data.get('tipo_documento')
        numero_documento = request.data.get('numero_documento')

        # Verifica si el cliente ya está registrado por su RUT
        try:
            cliente = Cliente.objects.get(rut=rut_cliente)
            # Actualizar la información del cliente existente si es necesario
            for key, value in cliente_data.items():
                setattr(cliente, key, value)
            cliente.save()
        except Cliente.DoesNotExist:
            cliente_serializer = ClienteSerializer(data=cliente_data)
            if cliente_serializer.is_valid():
                cliente = cliente_serializer.save()
            else:
                return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sucursal = Sucursal.objects.get(id=sucursal_id)
        vendedor = User.objects.get(id=vendedor_id)

        detalles_temp = CarroDeCompras.objects.filter(session_id=session_id)
        if not detalles_temp.exists():
            return Response({"detail": "No hay productos en el carrito de compras."}, status=status.HTTP_400_BAD_REQUEST)

        venta = Venta.objects.create(
            cliente=cliente,
            sucursal=sucursal,
            vendedor=vendedor,
            total=0
        )

        total = 0
        for detalle_temp in detalles_temp:
            producto = detalle_temp.producto
            cantidad = detalle_temp.cantidad
            precio_unitario = detalle_temp.precio_unitario
            descuento_aplicado = 0

            # Aplicar descuento si hay promociones vigentes
            promociones = producto.promociones.filter(estado=True, fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now())
            if promociones.exists():
                promocion = promociones.first()  # Suponiendo que aplicamos solo la primera promoción activa
                descuento_aplicado = promocion.descuento
                precio_unitario -= (precio_unitario * (descuento_aplicado / 100))

            if producto.stock < cantidad:
                return Response({"detail": f"Producto {producto.nombre} no tiene suficiente stock."}, status=status.HTTP_400_BAD_REQUEST)

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                precio_total=precio_unitario * cantidad,
                descuento_aplicado=descuento_aplicado
            )

            producto.stock -= cantidad
            producto.save()
            total += precio_unitario * cantidad

        venta.total = total
        venta.save()
        detalles_temp.delete()

        if tipo_documento == 'boleta':
            documento = Boleta.objects.create(venta=venta, numero=numero_documento)
            return Response(BoletaSerializer(documento).data, status=status.HTTP_201_CREATED)
        else:
            documento = Factura.objects.create(venta=venta, numero=numero_documento)
            return Response(FacturaSerializer(documento).data, status=status.HTTP_201_CREATED)



class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PromocionSerializer

    def get_queryset(self):
        estado = self.request.query_params.get('estado', 'true').lower() == 'true'
        return Promocion.objects.filter(estado=estado)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            estado = self.request.query_params.get('estado', 'true').lower() == 'true'
            mensaje = "No existe registro activo de promociones." if estado else "No existen promociones deshabilitadas."
            return Response({"message": mensaje}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({"message": f"Promoción '{instance.descripcion}' deshabilitada correctamente."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='desactivadas', url_name='desactivadas')
    def list_inactive(self, request):
        queryset = Promocion.objects.filter(estado=False)
        if not queryset.exists():
            return Response({"message": "No existen promociones deshabilitadas."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='productos-vigentes', url_name='productos_vigentes')
    def productos_vigentes(self, request):
        today = timezone.now().date()
        promociones = Promocion.objects.filter(fecha_inicio__lte=today, fecha_fin__gte=today, estado=True)
        productos = Producto.objects.filter(promociones__in=promociones).distinct()
        
        if not productos.exists():
            return Response({"message": "No hay productos en promociones vigentes."}, status=status.HTTP_200_OK)
        
        serializer = ProductoPromocionSerializer(productos, many=True)
        return Response(serializer.data)


class HistorialComprasViewSet(BaseViewSet):
    queryset = HistorialCompras.objects.filter(estado=True)
    serializer_class = HistorialComprasSerializer

class NotaCreditoViewSet(BaseViewSet):
    queryset = NotaCredito.objects.filter(estado=True)
    serializer_class = NotaCreditoSerializer

class RegistroUsuarioView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Usuario creado correctamente."
        }, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserListSerializer
        return UserSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False  # Cambiar el campo `is_active` a False
        instance.save()
        return Response({"message": f"Usuario '{instance.username}' deshabilitado correctamente."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def ventas_por_fecha(request, fecha_inicio, fecha_fin):
    ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin], estado=True)
    serializer = VentaSerializer(ventas, many=True)
    return Response(serializer.data)
