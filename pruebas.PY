from enums import Rol, FormaPago, Estado
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from excepciones import StockInsuficienteError, DuplicadoError, OperacionNoPermitidaError

def ejecutar_pruebas() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio()
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio()

    categoria = categorias.crear("Bebidas", "Bebidas frías")
    print("OK categoría:", categoria)
    try:
        categorias.crear("bebidas", "Duplicada")
    except DuplicadoError as error:
        print("ERROR ESPERADO duplicado:", error)

    producto = productos.crear("Agua", 800, "Botella 500 ml", 5, "", True, categoria)
    usuario = usuarios.crear("Juan", "Gomez", "juan@mail.com", "2611111111", "clave123", Rol.USUARIO)

    pedido = pedidos.crear(usuario, FormaPago.EFECTIVO, [(2, producto)])
    print("OK pedido:", pedido)
    print("OK detalle:", pedido.detalles[0])
    print("Stock luego de comprar 2:", producto.stock)

    try:
        pedidos.crear(usuario, FormaPago.EFECTIVO, [(99, producto)])
    except StockInsuficienteError as error:
        print("ERROR ESPERADO stock:", error)

    pedidos.actualizar(pedido.id, Estado.CANCELADO)
    print("Pedido cancelado:", pedido.estado.value)
    print("Stock luego de cancelar:", producto.stock)

    try:
        pedidos.actualizar(pedido.id, Estado.TERMINADO)
    except OperacionNoPermitidaError as error:
        print("ERROR ESPERADO transición:", error)

if __name__ == "__main__":
    ejecutar_pruebas()
