from .base import Base
from excepciones import DatoInvalidoError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .producto import Producto

class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: "Producto") -> None:
        super().__init__()
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = self.producto.precio * cantidad

    @property
    def producto(self) -> "Producto":
        return self.__producto

    @producto.setter
    def producto(self, valor: "Producto") -> None:
        from .producto import Producto
        if not isinstance(valor, Producto) or valor.eliminado:
            raise DatoInvalidoError("El producto no existe o está eliminado.")
        self.__producto = valor

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DatoInvalidoError("La cantidad debe ser un entero mayor que cero.")
        self.__cantidad = valor

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @subtotal.setter
    def subtotal(self, valor: float) -> None:
        if valor < 0:
            raise DatoInvalidoError("El subtotal no puede ser negativo.")
        self.__subtotal = float(valor)

    def __str__(self) -> str:
        return f"{self.producto.nombre} x {self.cantidad} = ${self.subtotal:.2f}"
