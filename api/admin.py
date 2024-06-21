# /mnt/data/admin.py

from django.contrib import admin
from .models import Profile, Sucursal

# admin.py
from django.contrib import admin
from .models import Profile, Sucursal, Categoria, Producto, Cliente, Venta, DetalleVenta, Promocion, HistorialCompras, NotaCredito

admin.site.register(Profile)
admin.site.register(Sucursal)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Promocion)
admin.site.register(HistorialCompras)
admin.site.register(NotaCredito)
