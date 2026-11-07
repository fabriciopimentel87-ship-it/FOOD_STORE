from .base_servicio import BaseServicio
from entidades.pedido import Pedido
from enums import Estado
from excepciones import DatoInvalidoError, OperacionNoPermitidaError

class PedidoServicio(BaseServicio):
    def __init__(self) -> None:
        super().__init__()
        self._stock_devuelto: set[int] = set()

    def crear(self, usuario, forma_pago, detalles: list[tuple[int, object]]) -> Pedido:
        pedido = Pedido(usuario, forma_pago)
        # Primero se valida todo sin modificar el stock.
        acumulado: dict[int, int] = {}
        for cantidad, producto in detalles:
            if producto.id not in acumulado:
                acumulado[producto.id] = 0
            acumulado[producto.id] += cantidad
            if cantidad <= 0 or acumulado[producto.id] > producto.stock:
                from excepciones import StockInsuficienteError
                raise StockInsuficienteError(f"Stock insuficiente de {producto.nombre}.")
        for cantidad, producto in detalles:
            pedido.agregar_detalle(cantidad, producto)
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad
        self._coleccion.append(pedido)
        return pedido

    def actualizar(self, identificador: int, estado: Estado | None = None, forma_pago=None):
        pedido = self.buscar_por_id(identificador)
        if estado is not None and estado != pedido.estado:
            estado_anterior = pedido.estado
            pedido.estado = estado
            if estado == Estado.CANCELADO and estado_anterior != Estado.TERMINADO:
                self._devolver_stock(pedido)
        if forma_pago is not None:
            pedido.forma_pago = forma_pago
        return pedido

    def _devolver_stock(self, pedido: Pedido) -> None:
        if pedido.id not in self._stock_devuelto:
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
            self._stock_devuelto.add(pedido.id)

    def eliminar(self, identificador: int) -> None:
        pedido = self.buscar_por_id(identificador)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self._devolver_stock(pedido)
        pedido.eliminado = True
        for detalle in pedido.detalles:
            detalle.eliminado = True

    def listar_de_usuario(self, usuario) -> list[Pedido]:
        return [p for p in self.listar() if p.usuario == usuario]
