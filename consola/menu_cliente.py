from .menu import Menu


class MenuCliente(Menu):

    def mostrar(self) -> bool:

        while True:
            print(
                f"\n=== FOOD STORE - CLIENTE "
                f"({self._usuario.nombre} {self._usuario.apellido}) ==="
            )

            opcion = self._seleccionar(
                "¿Qué desea hacer?",
                [
                    "Ver categorías",
                    "Ver productos disponibles",
                    "Mis pedidos",
                    "Mis datos",
                    "Cerrar sesión",
                    "Salir"
                ]
            )

            try:
                if opcion == "Ver categorías":
                    self._mostrar(
                        self._servicios["categorias"].listar(),
                        "No hay categorías cargadas."
                    )

                elif opcion == "Ver productos disponibles":
                    self._mostrar(
                        self._servicios["productos"].listar_disponibles(),
                        "No hay productos disponibles."
                    )

                elif opcion == "Mis pedidos":
                    pedidos = self._servicios["pedidos"].listar_de_usuario(
                        self._usuario
                    )

                    self._mostrar(pedidos, "No tiene pedidos.")

                    if pedidos:
                        ver_detalles = self._seleccionar(
                            "¿Desea ver los detalles de un pedido?",
                            ["Sí", "No"]
                        )

                        if ver_detalles == "Sí":
                            identificador = int(input("ID pedido: "))

                            pedido = next(
                                (p for p in pedidos if p.id == identificador),
                                None
                            )

                            if pedido is None:
                                print("Pedido inexistente.")
                            else:
                                self._mostrar(
                                    pedido.detalles,
                                    "El pedido no tiene detalles."
                                )

                elif opcion == "Mis datos":
                    print(
                        f"{self._usuario.nombre} "
                        f"{self._usuario.apellido} | "
                        f"{self._usuario.mail} | "
                        f"{self._usuario.celular} | "
                        f"{self._usuario.rol.value}"
                    )

                elif opcion == "Cerrar sesión":
                    return True

                elif opcion == "Salir":
                    return False

            except (ValueError, Exception) as error:
                print(f"Error: {error}")

            input("\nPresione Enter para continuar...")

    def _mostrar(self, elementos, mensaje: str):

        if not elementos:
            print(mensaje)

        else:
            for elemento in elementos:
                print(elemento)