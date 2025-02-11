from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    estado = models.BooleanField(default=True, verbose_name="Estado")

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    estado = models.BooleanField(default=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    estado = models.BooleanField(default=True, verbose_name="Estado")

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)  # Relación con Bodega
    estado = models.BooleanField(default=True)
    descuento = models.ForeignKey('Promocion', on_delete=models.SET_NULL, null=True)
    


class Profile(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='admin', verbose_name="Rol")
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, verbose_name="Sucursal")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return self.user.username


class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    estado = models.BooleanField(default=True)

class CarroDeCompras(models.Model):
    session_id = models.CharField(max_length=255)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=True, blank=True, verbose_name="Fecha")  # Permitir null y blank
    total = models.DecimalField(max_digits=10, decimal_places=2)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    entregado = models.BooleanField(default=False, verbose_name="Entregado")  # Nuevo campo para estado de entrega

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = timezone.now()
        super(Venta, self).save(*args, **kwargs)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class Factura(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    fecha_emision = models.DateTimeField(null=True)
    estado = models.BooleanField(default=True)

class Boleta(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    fecha_emision = models.DateTimeField(null=True)
    estado = models.BooleanField(default=True)

class Promocion(models.Model):
    descripcion = models.TextField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField(default='2024-01-01')
    fecha_fin = models.DateField(default='2024-01-01')
    productos = models.ManyToManyField('Producto', related_name='promociones')
    estado = models.BooleanField(default=True)

class HistorialCompras(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    estado = models.BooleanField(default=True, verbose_name="Estado")

# models.py

class NotaCredito(models.Model):
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    numero = models.CharField(max_length=20, unique=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.numero:
            last_nota = NotaCredito.objects.all().order_by('id').last()
            if last_nota:
                last_number = int(last_nota.numero.split('-')[1])
                self.numero = f'NC-{last_number + 1:05d}'
            else:
                self.numero = 'NC-00001'
        super(NotaCredito, self).save(*args, **kwargs)

    def __str__(self):
        return f"Nota de Crédito #{self.numero} - Venta #{self.venta.id}"


class DetalleNotaCredito(models.Model):
    nota_credito = models.ForeignKey(NotaCredito, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    





class Correlativo(models.Model):
    tipo_documento = models.CharField(max_length=20, unique=True)
    ultimo_numero = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.tipo_documento}: {self.ultimo_numero}"
