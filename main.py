from entidades.categoria import Categoria
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums import Rol
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from consola.lectura import seleccionar_opcion
from excepciones import CredencialesInvalidasError


def crear_menu(usuario: Usuario, servicios: dict):
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, servicios)
    return MenuCliente(usuario, servicios)


def main() -> None:
    servicios = {
        "categorias": CategoriaServicio(),
        "productos": ProductoServicio(),
        "usuarios": UsuarioServicio(),
        "pedidos": PedidoServicio()
    }

    # Administrador inicial para permitir el primer ingreso.
    servicios["usuarios"].crear(
        "Ana",
        "Perez",
        "admin@foodstore.com",
        "2610000000",
        "admin123",
        Rol.ADMIN
    )

    # Datos iniciales de ejemplo.
    categoria = servicios["categorias"].crear(
        "Hamburguesas",
        "Hamburguesas y combos"
    )

    servicios["productos"].crear(
        "Hamburguesa completa",
        4500,
        "Carne, queso y vegetales",
        10,
        "",
        True,
        categoria
    )

    while True:
        print("\n=== FOOD STORE – INICIO DE SESIÓN ===")

        sesion = None
        intentos = 0

        while sesion is None and intentos < 3:
            mail = input("Mail: ").strip()
            contrasenia = input("Contraseña: ")

            try:
                sesion = servicios["usuarios"].autenticar(
                    mail,
                    contrasenia
                )

            except CredencialesInvalidasError:
                intentos += 1
                print("Mail o contraseña incorrectos.")

                if intentos == 3:
                    print("Se agotaron los 3 intentos. Fin del programa.")
                    return

        print(
            f"\nBienvenido/a, {sesion.nombre} "
            f"{sesion.apellido} [{sesion.rol.value}]"
        )

        menu = crear_menu(sesion, servicios)
        continuar = menu.mostrar()

        if not continuar:
            print("\nGracias por utilizar Food Store.")
            break

        opcion = seleccionar_opcion(
            "¿Qué desea hacer ahora?",
            [
                "Iniciar sesión con otro usuario",
                "Salir del programa"
            ]
        )

        if opcion is None or opcion == "Salir del programa":
            print("\nGracias por utilizar Food Store.")
            break


if __name__ == "__main__":
    main()