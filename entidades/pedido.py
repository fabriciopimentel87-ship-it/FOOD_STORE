from datetime import date
from .base import Base
from .calculable import Calculable
from .detalle_pedido import DetallePedido
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, StockInsuficienteError, OperacionNoPermitidaError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import Usuario
    from .producto import Producto

class Pedido(Base, Calculable):
    def __init__(self, usuario: "Usuario", forma_pago: FormaPago) -> None:
        super().__init__()
        from .usuario import Usuario
        if not isinstance(usuario, Usuario) or usuario.eliminado:
            raise DatoInvalidoError("No se puede crear un pedido para un usuario eliminado.")
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.forma_pago = forma_pago
        self.__total: float = 0.0
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> "Usuario":
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, valor: Estado) -> None:
        if not isinstance(valor, Estado):
            raise DatoInvalidoError("Estado inválido.")
        permitidas: dict[Estado, list[Estado]] = {
            Estado.PENDIENTE: [Estado.CONFIRMADO, Estado.CANCELADO],
            Estado.CONFIRMADO: [Estado.TERMINADO, Estado.CANCELADO],
            Estado.TERMINADO: [],
            Estado.CANCELADO: []
        }
        if valor != self.__estado and valor not in permitidas[self.__estado]:
            raise OperacionNoPermitidaError("La transición de estado no está permitida.")
        self.__estado = valor

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("Forma de pago inválida.")
        self.__forma_pago = valor

    @property
    def total(self) -> float:
        return self.__total

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    def buscar_detalle_por_producto(self, producto: "Producto") -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def agregar_detalle(self, cantidad: int, producto: "Producto") -> None:
        from .producto import Producto
        if not isinstance(producto, Producto) or producto.eliminado or not producto.disponible:
            raise DatoInvalidoError("El producto no está disponible.")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        detalle_existente = self.buscar_detalle_por_producto(producto)
        cantidad_actual = detalle_existente.cantidad if detalle_existente else 0
        if cantidad_actual + cantidad > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente de {producto.nombre}. Disponible: {producto.stock}."
            )
        if detalle_existente:
            detalle_existente.cantidad += cantidad
            detalle_existente.subtotal = detalle_existente.cantidad * producto.precio
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()

    def eliminar_detalle_por_producto(self, producto: "Producto") -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is not None:
            self.__detalles.remove(detalle)
            self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(detalle.subtotal for detalle in self.__detalles)

    def __str__(self) -> str:
        return (f"ID: {self.id} | {self.usuario.nombre} {self.usuario.apellido} | "
                f"{self.estado.value} | {self.forma_pago.value} | ${self.total:.2f} | {self.fecha}")
