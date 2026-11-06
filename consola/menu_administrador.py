from .menu import Menu
from .lectura import (
    leer_entero,
    leer_float,
    leer_texto,
    leer_opcion_enum,
    leer_sn
)
from enums import Rol, Estado, FormaPago

class MenuAdministrador(Menu):

    def mostrar(self) -> bool:

        while True:
            print(
                f"\n=== FOOD STORE - ADMINISTRADOR "
                f"({self._usuario.nombre} {self._usuario.apellido}) ==="
            )

            opcion = self._seleccionar(
                "¿Qué desea administrar?",
                [
                    "Categorías",
                    "Productos",
                    "Usuarios",
                    "Pedidos",
                    "Cerrar sesión",
                    "Salir"
                ]
            )

            if opcion == "Categorías":
                self._ejecutar_seguro(self._menu_categorias)

            elif opcion == "Productos":
                self._ejecutar_seguro(self._menu_productos)

            elif opcion == "Usuarios":
                self._ejecutar_seguro(self._menu_usuarios)

            elif opcion == "Pedidos":
                self._ejecutar_seguro(self._menu_pedidos)

            elif opcion == "Cerrar sesión":
                return True

            elif opcion == "Salir":
                return False

    # CATEGORÍAS

    def _menu_categorias(self):

        servicio = self._servicios["categorias"]

        while True:

            op = self._seleccionar(
                "--- CATEGORÍAS ---",
                [
                    "Listar categorías",
                    "Crear categoría",
                    "Editar categoría",
                    "Eliminar categoría",
                    "Volver"
                ]
            )

            if op == "Listar categorías":
                self._mostrar_lista(
                    servicio.listar(),
                    "No hay categorías cargadas."
                )

            elif op == "Crear categoría":
                obj = servicio.crear(
                    leer_texto("Nombre: "),
                    leer_texto("Descripción: ")
                )

                print(f"Categoría creada. ID: {obj.id}")

            elif op == "Editar categoría":
                self._mostrar_lista(
                    servicio.listar(),
                    "No hay categorías cargadas."
                )

                obj = servicio.buscar_por_id(
                    leer_entero("ID a editar: ")
                )

                nombre = (
                    input(f"Nombre [{obj.nombre}]: ").strip()
                    or obj.nombre
                )

                descripcion = (
                    input(f"Descripción [{obj.descripcion}]: ").strip()
                    or obj.descripcion
                )

                servicio.editar(
                    obj.id,
                    nombre,
                    descripcion
                )

                print("Categoría actualizada.")

            elif op == "Eliminar categoría":
                self._mostrar_lista(
                    servicio.listar(),
                    "No hay categorías cargadas."
                )

                identificador = leer_entero("ID a eliminar: ")

                if leer_sn("¿Confirma la eliminación?"):
                    servicio.eliminar(
                        identificador,
                        self._servicios["productos"]
                    )

                    print("Categoría eliminada.")

            elif op == "Volver":
                return

    # PRODUCTOS
    def _menu_productos(self):

        servicio = self._servicios["productos"]
        categorias = self._servicios["categorias"]

        while True:

            op = self._seleccionar(
                "--- PRODUCTOS ---",
                [
                    "Listar productos",
                    "Crear producto",
                    "Editar producto",
                    "Eliminar producto",
                    "Volver"
                ]
            )

            if op == "Listar productos":
                self._mostrar_lista(
                    servicio.listar(),
                    "No hay productos cargados."
                )

            elif op == "Crear producto":

                self._mostrar_lista(
                    categorias.listar(),
                    "Primero debe crear una categoría."
                )

                categoria = categorias.buscar_por_id(
                    leer_entero("ID categoría: ")
                )

                obj = servicio.crear(
                    leer_texto("Nombre: "),
                    leer_float("Precio: "),
                    leer_texto("Descripción: "),
                    leer_entero("Stock: "),
                    input("Imagen (texto/ruta): "),
                    leer_sn("¿Disponible?"),
                    categoria
                )

                print(f"Producto creado. ID: {obj.id}")

            elif op == "Editar producto":

                self._mostrar_lista(
                    servicio.listar(),
                    "No hay productos cargados."
                )

                obj = servicio.buscar_por_id(
                    leer_entero("ID a editar: ")
                )

                self._mostrar_lista(
                    categorias.listar(),
                    "No hay categorías."
                )

                categoria_id = input(
                    f"ID categoría [{obj.categoria.id}]: "
                ).strip()

                categoria = (
                    categorias.buscar_por_id(int(categoria_id))
                    if categoria_id
                    else obj.categoria
                )

                nombre = (
                    input(f"Nombre [{obj.nombre}]: ").strip()
                    or obj.nombre
                )

                precio_txt = input(
                    f"Precio [{obj.precio}]: "
                ).strip()

                descripcion = (
                    input(f"Descripción [{obj.descripcion}]: ").strip()
                    or obj.descripcion
                )

                stock_txt = input(
                    f"Stock [{obj.stock}]: "
                ).strip()

                imagen = (
                    input(f"Imagen [{obj.imagen}]: ").strip()
                    or obj.imagen
                )

                disponible_txt = input(
                    f"Disponible S/N "
                    f"[{'S' if obj.disponible else 'N'}]: "
                ).strip().upper()

                disponible = (
                    obj.disponible
                    if not disponible_txt
                    else disponible_txt == "S"
                )

                servicio.editar(
                    obj.id,
                    nombre,
                    float(precio_txt.replace(",", "."))
                    if precio_txt else obj.precio,
                    descripcion,
                    int(stock_txt) if stock_txt else obj.stock,
                    imagen,
                    disponible,
                    categoria
                )

                print("Producto actualizado.")

            elif op == "Eliminar producto":

                self._mostrar_lista(
                    servicio.listar(),
                    "No hay productos cargados."
                )

                identificador = leer_entero("ID a eliminar: ")

                if leer_sn("¿Confirma la eliminación?"):
                    servicio.eliminar(identificador)
                    print("Producto eliminado.")

            elif op == "Volver":
                return


    # USUARIOS
    def _menu_usuarios(self):
        
        servicio = self._servicios["usuarios"]
        
        while True:
            
            op = self._seleccionar(
                "--- USUARIOS ---",
                [
                    "Listar usuarios",
                    "Crear usuario",
                    "Editar usuario",
                    "Eliminar usuario",
                    "Volver"
                ]
            )
            
            if op == "Listar usuarios":
                
                self._mostrar_lista(
                    servicio.listar(),
                    "No hay usuarios cargados."
                )
                
            elif op == "Crear usuario":
                
                obj = servicio.crear(
                    leer_texto("Nombre: "),
                    leer_texto("Apellido: "),
                    leer_texto("Mail: "),
                    leer_texto("Celular: "),
                    leer_texto("Contraseña: "),
                    leer_opcion_enum(Rol, "Seleccione el rol:")
                )

                print(f"Usuario creado. ID: {obj.id}")

            elif op == "Editar usuario":

                self._mostrar_lista(
                    servicio.listar(),
                    "No hay usuarios cargados."
                )

                obj = servicio.buscar_por_id(
                    leer_entero("ID a editar: ")
                )

                nombre = (
                    input(f"Nombre [{obj.nombre}]: ").strip()
                    or obj.nombre
                )

                apellido = (
                    input(f"Apellido [{obj.apellido}]: ").strip()
                    or obj.apellido
                )

                mail = (
                    input(f"Mail [{obj.mail}]: ").strip()
                    or obj.mail
                )

                celular = (
                    input(f"Celular [{obj.celular}]: ").strip()
                    or obj.celular
                )

                contrasenia = (
                    input("Nueva contraseña (vacío conserva): ").strip()
                    or None
                )

                rol = (
                    leer_opcion_enum(Rol, "Seleccione el nuevo rol:")
                    if leer_sn("¿Cambiar rol?")
                    else None
                )

                servicio.editar(
                    obj.id,
                    nombre,
                    apellido,
                    mail,
                    celular,
                    contrasenia,
                    rol
                )

                print("Usuario actualizado.")

            elif op == "Eliminar usuario":

                self._mostrar_lista(
                    servicio.listar(),
                    "No hay usuarios cargados."
                )

                identificador = leer_entero("ID a eliminar: ")
                obj = servicio.buscar_por_id(identificador)
                
                if obj == self._usuario:
                    print("No puede eliminarse a sí mismo.")
                    
                elif leer_sn("¿Confirma la eliminación?"):
                    servicio.eliminar(identificador)
                    print("Usuario eliminado.")
            elif op == "Volver":
                return


    # PEDIDOS
    def _menu_pedidos(self):

        pedidos = self._servicios["pedidos"]
        productos = self._servicios["productos"]
        usuarios = self._servicios["usuarios"]

        while True:

            op = self._seleccionar(
                "--- PEDIDOS ---",
                [
                    "Listar pedidos",
                    "Crear pedido",
                    "Actualizar estado o pago",
                    "Eliminar pedido",
                    "Volver"
                ]
            )

            if op == "Listar pedidos":

                self._mostrar_lista(
                    pedidos.listar(),
                    "No hay pedidos cargados."
                )

                if pedidos.listar() and leer_sn(
                    "¿Ver detalles de un pedido?"
                ):
                    pedido = pedidos.buscar_por_id(
                        leer_entero("ID pedido: ")
                    )

                    self._mostrar_lista(
                        pedido.detalles,
                        "El pedido no tiene detalles."
                    )

            elif op == "Crear pedido":

                self._mostrar_lista(
                    usuarios.listar(),
                    "No hay usuarios."
                )

                usuario = usuarios.buscar_por_id(
                    leer_entero("ID usuario: ")
                )

                forma_pago = leer_opcion_enum(
                    FormaPago,
                    "Seleccione la forma de pago:"
                )

                detalles = []

                while True:

                    self._mostrar_lista(
                        productos.listar(),
                        "No hay productos."
                    )

                    producto = productos.buscar_por_id(
                        leer_entero("ID producto: ")
                    )

                    cantidad = leer_entero("Cantidad: ")

                    detalles.append((cantidad, producto))

                    if not leer_sn("¿Agregar otro producto?"):
                        break

                pedido = pedidos.crear(
                    usuario,
                    forma_pago,
                    detalles
                )

                print(
                    f"Pedido creado. ID: {pedido.id} "
                    f"| Total: ${pedido.total:.2f}"
                )

            elif op == "Actualizar estado o pago":

                self._mostrar_lista(
                    pedidos.listar(),
                    "No hay pedidos."
                )

                pedido = pedidos.buscar_por_id(
                    leer_entero("ID pedido: ")
                )

                if leer_sn("¿Cambiar estado?"):

                    estado = leer_opcion_enum(
                        Estado,
                        "Seleccione el estado:"
                    )

                else:
                    estado = None

                if leer_sn("¿Cambiar forma de pago?"):

                    forma = leer_opcion_enum(
                        FormaPago,
                        "Seleccione la forma de pago:"
                    )

                else:
                    forma = None

                pedidos.actualizar(
                    pedido.id,
                    estado,
                    forma
                )

                print("Pedido actualizado.")

            elif op == "Eliminar pedido":

                self._mostrar_lista(
                    pedidos.listar(),
                    "No hay pedidos."
                )

                identificador = leer_entero("ID pedido: ")

                if leer_sn("¿Confirma la eliminación?"):
                    pedidos.eliminar(identificador)
                    print("Pedido eliminado.")

            elif op == "Volver":
                return

    # MOSTRAR LISTAS
    def _mostrar_lista(self, elementos, mensaje: str):

        if not elementos:
            print(mensaje)

        else:
            for elemento in elementos:
                print(elemento)