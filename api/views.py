from datetime import datetime
from venv import logger
from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction



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
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.estado:
            instance.estado = True
            instance.save()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({"message": f"Cliente '{instance.nombre} {instance.apellido}' deshabilitado correctamente."}, status=status.HTTP_200_OK)


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sucursal', 'vendedor', 'fecha']

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
        total = request.data.get('total')
        detalles_data = request.data.get('detalles')

        cliente_data['rut'] = rut_cliente
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

        # detalles_temp = CarroDeCompras.objects.filter(session_id=session_id)
        # if not detalles_temp.exists():
        #   return Response({"detail": "No hay productos en el carrito de compras."}, status=status.HTTP_400_BAD_REQUEST)
        
        fecha = request.data.get('fecha', timezone.now())

        venta = Venta.objects.create(
            cliente=cliente,
            sucursal=sucursal,
            vendedor=vendedor,
            fecha=fecha,
            total=0
        )

        total = 0
        # Determinar si se debe usar el carrito de compras o los detalles de la venta manual
        if 'session_id' in request.data:
            session_id = request.data.get('session_id')
            detalles_temp = CarroDeCompras.objects.filter(session_id=session_id)
            if not detalles_temp.exists():
                return Response({"detail": "No hay productos en el carrito de compras."}, status=status.HTTP_400_BAD_REQUEST)

            total = 0
            for detalle_temp in detalles_temp:
                producto = detalle_temp.producto
                cantidad = detalle_temp.cantidad
                precio_unitario = detalle_temp.precio_unitario
                descuento_aplicado = 0

                # Aplicar descuento si hay promociones vigentes
                promociones = producto.promociones.filter(estado=True, fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now())
                if promociones.exists():
                    promocion = promociones.first()
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
        else:
            # Manejo de venta manual sin carrito
            total = 0
            for detalle_data in detalles_data:
                producto_id = detalle_data.get('producto')
                cantidad = detalle_data.get('cantidad')
                precio_unitario = detalle_data.get('precio_unitario')

                producto = Producto.objects.get(id=producto_id)
                descuento_aplicado = 0

                # Aplicar descuento si hay promociones vigentes
                promociones = producto.promociones.filter(estado=True, fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now())
                if promociones.exists():
                    promocion = promociones.first()
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

        # Crear el documento tributario después de guardar la venta
        with transaction.atomic():
            if tipo_documento == 'boleta':
                correlativo, created = Correlativo.objects.get_or_create(tipo_documento='boleta')
                correlativo.ultimo_numero += 1
                correlativo.save()
                documento = Boleta.objects.create(venta=venta, numero=correlativo.ultimo_numero, fecha_emision=fecha)
                return Response(BoletaSerializer(documento).data, status=status.HTTP_201_CREATED)
            elif tipo_documento == 'factura':
                correlativo, created = Correlativo.objects.get_or_create(tipo_documento='factura')
                correlativo.ultimo_numero += 1
                correlativo.save()
                documento = Factura.objects.create(venta=venta, numero=correlativo.ultimo_numero, fecha_emision=fecha)
                return Response(FacturaSerializer(documento).data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Tipo de documento no válido."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='documento')
    def obtener_documento(self, request, pk=None):
        try:
            venta = self.get_object()
            if hasattr(venta, 'boleta'):
                documento = venta.boleta
                serializer = BoletaSerializer(documento)
            elif hasattr(venta, 'factura'):
                documento = venta.factura
                serializer = FacturaSerializer(documento)
            else:
                return Response({"detail": "No se encontró documento asociado."}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Venta.DoesNotExist:
            return Response({"detail": "Venta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='entregar')
    def entregar(self, request, pk=None):
        venta = self.get_object()
        venta.entregado = True
        venta.save()
        return Response({"message": "Productos entregados correctamente."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='por-entregar')
    def ventas_por_entregar(self, request):
        ventas = Venta.objects.filter(estado=True, entregado=False)
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='entregadas')
    def ventas_entregadas(self, request):
        ventas = Venta.objects.filter(estado=True, entregado=True)
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def historial_compras_cliente(request, rut):
    try:
        cliente = Cliente.objects.get(rut=rut)
        logger.info(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
        
        ventas = Venta.objects.filter(cliente=cliente, estado=True)
        logger.info(f"Ventas encontradas para el cliente {cliente.rut}: {ventas.count()}")

        if not ventas.exists():
            logger.info(f"No se encontraron ventas para el cliente con RUT {cliente.rut}")
            return Response({"detail": "No se encontraron ventas para el cliente."}, status=status.HTTP_404_NOT_FOUND)

        resultado = []
        for venta in ventas:
            detalles = DetalleVenta.objects.filter(venta=venta)
            logger.info(f"Detalles de venta encontrados para la venta {venta.id}: {detalles.count()}")

            for detalle in detalles:
                logger.info(f"Detalle de venta: Producto {detalle.producto.nombre}, Cantidad {detalle.cantidad}, Precio Unitario {detalle.precio_unitario}, Precio Total {detalle.precio_total}")
                resultado.append({
                    "venta_id": venta.id,
                    "fecha": venta.fecha,
                    "producto": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": detalle.precio_unitario,
                    "precio_total": detalle.precio_total
                })

        logger.info(f"Historial de compras construido: {len(resultado)} elementos encontrados.")
        return Response(resultado, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        logger.error(f"Cliente con RUT {rut} no encontrado.")
        return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return Response({"detail": "Error inesperado en el servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
@api_view(['GET'])
def historial_compras_cliente(request, rut):
    try:
        cliente = Cliente.objects.get(rut=rut)
        historial = HistorialCompras.objects.filter(cliente=cliente)
        serializer = HistorialComprasSerializer(historial, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)


class HistorialComprasViewSet(BaseViewSet):
    queryset = HistorialCompras.objects.filter(estado=True)
    serializer_class = HistorialComprasSerializer



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


class DocumentoViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def check_user_role(self, request):
        if not request.user.is_authenticated:
            return False
        try:
            profile = request.user.profile
            return profile.rol in ['contador', 'admin']
        except Profile.DoesNotExist:
            return False

    @action(detail=False, methods=['get'], url_path='listar-todos', url_name='listar_todos')
    def listar_todos(self, request):
        if not self.check_user_role(request):
            return Response({"detail": "No tiene permiso para ver esta información."}, status=status.HTTP_403_FORBIDDEN)
        facturas = Factura.objects.all()
        boletas = Boleta.objects.all()

        facturas_serializer = FacturaSerializer(facturas, many=True)
        boletas_serializer = BoletaSerializer(boletas, many=True)

        return Response({
            'facturas': facturas_serializer.data,
            'boletas': boletas_serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='boletas-mes', url_name='boletas_mes')
    def listar_boletas_mes(self, request):
        if not self.check_user_role(request):
            return Response({"detail": "No tiene permiso para ver esta información."}, status=status.HTTP_403_FORBIDDEN)
        
        mes = request.query_params.get('mes', None)
        año = request.query_params.get('año', None)
        sucursal_id = request.query_params.get('sucursal', None)
        vendedor_id = request.query_params.get('vendedor', None)

        if not mes or not año:
            return Response({"detail": "Mes y año son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mes = int(mes)
            año = int(año)
            start_of_month = datetime(año, mes, 1)
            if mes == 12:
                end_of_month = datetime(año + 1, 1, 1)
            else:
                end_of_month = datetime(año, mes + 1, 1)
        except ValueError:
            return Response({"detail": "Mes y año deben ser números válidos."}, status=status.HTTP_400_BAD_REQUEST)

        boletas = Boleta.objects.filter(fecha_emision__gte=start_of_month, fecha_emision__lt=end_of_month)
        if sucursal_id:
            boletas = boletas.filter(venta__sucursal_id=sucursal_id)
        if vendedor_id:
            boletas = boletas.filter(venta__vendedor_id=vendedor_id)

        serializer = BoletaSerializer(boletas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='facturas-mes', url_name='facturas_mes')
    def listar_facturas_mes(self, request):
        if not self.check_user_role(request):
            return Response({"detail": "No tiene permiso para ver esta información."}, status=status.HTTP_403_FORBIDDEN)
        mes = request.query_params.get('mes', None)
        año = request.query_params.get('año', None)
        sucursal_id = request.query_params.get('sucursal', None)
        vendedor_id = request.query_params.get('vendedor', None)

        if not mes or not año:
            return Response({"detail": "Mes y año son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mes = int(mes)
            año = int(año)
            start_of_month = datetime(año, mes, 1)
            if mes == 12:
                end_of_month = datetime(año + 1, 1, 1)
            else:
                end_of_month = datetime(año, mes + 1, 1)
        except ValueError:
            return Response({"detail": "Mes y año deben ser números válidos."}, status=status.HTTP_400_BAD_REQUEST)

        facturas = Factura.objects.filter(fecha_emision__gte=start_of_month, fecha_emision__lt=end_of_month)

        if sucursal_id:
            facturas = facturas.filter(venta__sucursal_id=sucursal_id)
        if vendedor_id:
            facturas = facturas.filter(venta__vendedor_id=vendedor_id)

        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='notas-credito-mes', url_name='notas_credito_mes')
    def listar_notas_credito_mes(self, request):
        mes = request.query_params.get('mes', None)
        año = request.query_params.get('año', None)

        if not mes or not año:
            return Response({"detail": "Mes y año son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mes = int(mes)
            año = int(año)
            start_of_month = datetime(año, mes, 1)
            if mes == 12:
                end_of_month = datetime(año + 1, 1, 1)
            else:
                end_of_month = datetime(año, mes + 1, 1)
        except ValueError:
            return Response({"detail": "Mes y año deben ser números válidos."}, status=status.HTTP_400_BAD_REQUEST)

        notas_credito = NotaCredito.objects.filter(fecha__gte=start_of_month, fecha__lt=end_of_month)
        serializer = NotaCreditoSerializer(notas_credito, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NotaCreditoViewSet(viewsets.ModelViewSet):
    queryset = NotaCredito.objects.all()
    serializer_class = NotaCreditoSerializer

    def check_user_role(self, request):
        if not request.user.is_authenticated:
            return False
        try:
            profile = request.user.profile
            return profile.rol in ['contador', 'admin']
        except Profile.DoesNotExist:
            return False

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'], url_path='listar-por-mes', url_name='listar_por_mes')
    def listar_por_mes(self, request):
        if not self.check_user_role(request):
            return Response({"detail": "No tiene permiso para ver esta información."}, status=status.HTTP_403_FORBIDDEN)

        mes = request.query_params.get('mes', None)
        año = request.query_params.get('año', None)
        sucursal_id = request.query_params.get('sucursal', None)
        vendedor_id = request.query_params.get('vendedor', None)

        if not mes or not año:
            return Response({"detail": "Mes y año son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mes = int(mes)
            año = int(año)
            start_of_month = datetime(año, mes, 1)
            if mes == 12:
                end_of_month = datetime(año + 1, 1, 1)
            else:
                end_of_month = datetime(año, mes + 1, 1)
        except ValueError:
            return Response({"detail": "Mes y año deben ser números válidos."}, status=status.HTTP_400_BAD_REQUEST)

        notas_credito = NotaCredito.objects.filter(fecha__gte=start_of_month, fecha__lt=end_of_month)

        if sucursal_id:
            notas_credito = notas_credito.filter(venta__sucursal_id=sucursal_id)

        if vendedor_id:
            notas_credito = notas_credito.filter(venta__vendedor_id=vendedor_id)

        serializer = NotaCreditoSerializer(notas_credito, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CorrelativoViewSet(viewsets.ModelViewSet):
    queryset = Correlativo.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CorrelativoSerializer


@api_view(['POST'])
def actualizar_stock(request):
    try:
        producto_id = request.data.get('producto_id')
        cantidad_a_sumar = request.data.get('cantidad')

        if not producto_id or not cantidad_a_sumar:
            return Response({"detail": "producto_id y cantidad son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        producto = Producto.objects.get(id=producto_id)
        producto.stock += int(cantidad_a_sumar)
        producto.save()

        return Response({"detail": f"Stock actualizado. Nuevo stock de {producto.nombre}: {producto.stock}"}, status=status.HTTP_200_OK)
    except Producto.DoesNotExist:
        return Response({"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def documentos_por_cliente(request, rut):
    try:
        cliente = Cliente.objects.get(rut=rut)
        boletas = Boleta.objects.filter(venta__cliente=cliente)
        facturas = Factura.objects.filter(venta__cliente=cliente)
        notas_credito = NotaCredito.objects.filter(venta__cliente=cliente)
        
        boletas_serializer = BoletaSerializer(boletas, many=True)
        facturas_serializer = FacturaSerializer(facturas, many=True)
        notas_credito_serializer = NotaCreditoSerializer(notas_credito, many=True)
        
        return Response({
            'boletas': boletas_serializer.data,
            'facturas': facturas_serializer.data,
            'notas_credito': notas_credito_serializer.data
        }, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)