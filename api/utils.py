
import requests
from .models import Producto, Categoria, Bodega

# URL de la API externa
EXTERNAL_API_URL = "http://207.231.108.32:8009/api/"

def obtener_productos_externos():
    url = f"{EXTERNAL_API_URL}ice/"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def enviar_producto_externo(producto):
    url = f"{EXTERNAL_API_URL}ice/"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "nombre": producto.nombre,
        "Precio": float(producto.precio),  # Convertir Decimal a float
        "cantidad": producto.stock,
        "descripcion": producto.descripcion,
        "imagen_url": "https://www.servicioruedas.cl/wp-content/uploads/2020/07/Auto-Repuestos-e1595295670370.png"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text  # Retornar también el texto de la respuesta
