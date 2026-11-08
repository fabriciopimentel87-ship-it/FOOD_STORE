from .base_servicio import BaseServicio
from entidades.producto import Producto
from excepciones import DatoInvalidoError

class ProductoServicio(BaseServicio):
    def crear(self, nombre: str, precio: float, descripcion: str, stock: int,
            imagen: str, disponible: bool, categoria) -> Producto:
        producto = Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        self._coleccion.append(producto)
        return producto

    def editar(self, identificador: int, nombre: str, precio: float, descripcion: str,
            stock: int, imagen: str, disponible: bool, categoria) -> Producto:
        producto = self.buscar_por_id(identificador)
        producto.nombre = nombre
        producto.precio = precio
        producto.descripcion = descripcion
        producto.stock = stock
        producto.imagen = imagen
        producto.disponible = disponible
        producto.categoria = categoria
        return producto

    def listar_disponibles(self) -> list[Producto]:
        return [p for p in self.listar() if p.disponible and p.stock > 0]