from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.utils import timezone

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields =  ['id','nombre','direccion','estado']
    def validate_nombre(self, value):
        request = self.context.get('request')
        if request and request.method == 'PUT':
            # Obtener la instancia actual
            instance = self.instance
            # Si el nombre ha cambiado
            if instance.nombre != value:
                if Sucursal.objects.filter(nombre=value, estado=True).exists():
                    raise serializers.ValidationError("Una sucursal con este nombre ya existe.")
        else:
            if Sucursal.objects.filter(nombre=value, estado=True).exists():
                raise serializers.ValidationError("Una sucursal con este nombre ya existe.")
        return value

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
    def validate_nombre(self, value):
        request = self.context.get('request')
        if request and request.method in 'PUT':
            instance = self.instance
            if instance.nombre != value:
                if Categoria.objects.filter(nombre=value, estado=True).exists():
                    raise serializers.ValidationError("Una categoría con este nombre ya existe.")
        else:
            if Categoria.objects.filter(nombre=value, estado=True).exists():
                raise serializers.ValidationError("Una categoría con este nombre ya existe.")
        return value

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'

    def validate_nombre(self, value):
        request = self.context.get('request')
        if request and request.method == 'PUT':
            # Obtener la instancia actual
            instance = self.instance
            # Si el nombre ha cambiado
            if instance.nombre != value:
                if Bodega.objects.filter(nombre=value, estado=True).exists():
                    raise serializers.ValidationError("Una bodega con este nombre ya existe.")
        else:
            if Bodega.objects.filter(nombre=value, estado=True).exists():
                raise serializers.ValidationError("Una bodega con este nombre ya existe.")
        return value
class ProductoSerializer(serializers.ModelSerializer):
    nombre_categoria = serializers.CharField(source='categoria.nombre', read_only=True)
    nombre_bodega = serializers.CharField(source='bodega.nombre', read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), source='categoria')
    bodega_id = serializers.PrimaryKeyRelatedField(queryset=Bodega.objects.all(), source='bodega')

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'nombre_categoria', 'nombre_bodega', 'categoria_id', 'bodega_id', 'stock', 'estado']

    def validate_nombre(self, value):
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            instance = self.instance
            if instance.nombre != value:
                if Producto.objects.filter(nombre=value, estado=True).exists():
                    raise serializers.ValidationError("Un producto con este nombre ya existe.")
        else:
            if Producto.objects.filter(nombre=value, estado=True).exists():
                raise serializers.ValidationError("Un producto con este nombre ya existe.")
        return value
    


class PromocionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = ['descripcion', 'descuento', 'fecha_inicio', 'fecha_fin']

class ProductoPromocionSerializer(serializers.ModelSerializer):
    promociones = PromocionDetailSerializer(many=True, read_only=True)
    precio_con_descuento = serializers.SerializerMethodField()
    nombre_categoria = serializers.CharField(source='categoria.nombre', read_only=True)
    nombre_bodega = serializers.CharField(source='bodega.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'estado', 'promociones', 'precio_con_descuento', 'nombre_categoria', 'nombre_bodega']

    def get_promociones(self, obj):
        today = timezone.now().date()
        promociones_vigentes = obj.promociones.filter(fecha_inicio__lte=today, fecha_fin__gte=today, estado=True)
        return PromocionDetailSerializer(promociones_vigentes, many=True).data
    
    def get_precio_con_descuento(self, obj):
        today = timezone.now().date()
        promociones_vigentes = obj.promociones.filter(fecha_inicio__lte=today, fecha_fin__gte=today, estado=True)
        if promociones_vigentes.exists():
            descuento = max(promociones_vigentes.values_list('descuento', flat=True))
            return obj.precio * (1 - descuento / 100)
        return obj.precio


    

class ClienteSerializer(serializers.ModelSerializer):
    rut = serializers.CharField(max_length=12)
    class Meta:
        model = Cliente
        fields = ['id', 'rut', 'nombre', 'apellido', 'email', 'telefono', 'estado']

    def validate_rut(self, value):
        if Cliente.objects.filter(rut=value).exists():
            raise serializers.ValidationError("Ya existe un cliente con este RUT.")
        return value


class CarroDeComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarroDeCompras
        fields = ['session_id', 'producto', 'cantidad', 'precio_unitario', 'precio_total']

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'precio_total', 'descuento_aplicado']


class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_apellido = serializers.CharField(source='cliente.apellido', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    vendedor_nombre = serializers.CharField(source='vendedor.username', read_only=True)  # Añadir nombre del vendedor
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'cliente_nombre', 'cliente_apellido', 'sucursal', 'sucursal_nombre', 'fecha', 'total', 'vendedor', 'vendedor_nombre', 'estado', 'detalles', 'entregado']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)
        return venta

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.sucursal = validated_data.get('sucursal', instance.sucursal)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.total = validated_data.get('total', instance.total)
        instance.vendedor = validated_data.get('vendedor', instance.vendedor)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.entregado = validated_data.get('entregado', instance.entregado)
        instance.save()

        if detalles_data:
            instance.detalles.all().delete()
            for detalle_data in detalles_data:
                DetalleVenta.objects.create(venta=instance, **detalle_data)

        return instance

class FacturaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer()  # Incluir detalles de la venta
    class Meta:
        model = Factura
        fields = ['id','venta', 'numero', 'fecha_emision', 'estado']

class BoletaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer()  # Incluir detalles de la venta
    class Meta:
        model = Boleta
        fields = ['id','venta', 'numero', 'fecha_emision', 'estado']

class DetalleNotaCreditoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetalleNotaCredito
        fields = ['producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'precio_total']
        read_only_fields = ['precio_total']

    def create(self, validated_data):
        validated_data['precio_total'] = validated_data['cantidad'] * validated_data['precio_unitario']
        return super().create(validated_data)

class NotaCreditoSerializer(serializers.ModelSerializer):
    detalles = DetalleNotaCreditoSerializer(many=True)

    class Meta:
        model = NotaCredito
        fields = ['venta', 'numero', 'monto_total', 'descripcion', 'fecha', 'estado', 'detalles']
        read_only_fields = ['numero', 'monto_total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        nota_credito = NotaCredito.objects.create(**validated_data)
        
        monto_total = 0
        for detalle_data in detalles_data:
            detalle_data['nota_credito'] = nota_credito
            detalle_data['precio_total'] = detalle_data['cantidad'] * detalle_data['precio_unitario']
            producto = Producto.objects.get(id=detalle_data['producto'].id)
            producto.stock += detalle_data['cantidad']  # Incrementar el stock del producto devuelto
            producto.save()
            
            detalle = DetalleNotaCredito.objects.create(**detalle_data)
            monto_total += detalle.precio_total

        nota_credito.monto_total = monto_total
        nota_credito.save()
        
        return nota_credito



class PromocionSerializer(serializers.ModelSerializer):
    productos = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), many=True)

    class Meta:
        model = Promocion
        fields = '__all__'




class HistorialComprasSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = HistorialCompras
        fields = ['id', 'cliente', 'producto', 'producto_nombre', 'fecha', 'cantidad', 'precio_total', 'estado']


class ProfileSerializer(serializers.ModelSerializer):
    sucursal = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all())

    class Meta:
        model = Profile
        fields = ['rol', 'sucursal']

class ProfileDetailSerializer(serializers.ModelSerializer):
    sucursal = SucursalSerializer()

    class Meta:
        model = Profile
        fields = ['rol', 'sucursal']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'profile','is_active']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        # Crear el perfil del usuario
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'rol': profile_data['rol'],
                'sucursal': profile_data.get('sucursal'),
                'estado': profile_data.get('estado', True)
            }
        )
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        if profile_data:
            profile = instance.profile
            profile.rol = profile_data.get('rol', profile.rol)
            profile.sucursal = profile_data.get('sucursal', profile.sucursal)
            profile.estado = profile_data.get('estado', profile.estado)
            profile.save()

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        
        instance.save()
        return instance

class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()  # Usar el serializador detallado para la salida

    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'profile','is_active']




class CorrelativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correlativo
        fields = ['id','tipo_documento', 'ultimo_numero']
