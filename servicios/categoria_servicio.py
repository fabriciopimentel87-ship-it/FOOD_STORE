from .base_servicio import BaseServicio
from entidades import categoria as categoria_modulo
from entidades.categoria import Categoria
from excepciones import DuplicadoError, OperacionNoPermitidaError

class CategoriaServicio(BaseServicio):
    def crear(self, nombre: str, descripcion: str) -> Categoria:
        for categoria in self.listar():
            if categoria.nombre.lower() == nombre.strip().lower():
                raise DuplicadoError("Ya existe una categoría con ese nombre.")
        categoria = Categoria(nombre, descripcion)
        self._coleccion.append(categoria)
        return categoria

    def editar(self, identificador: int, nombre: str, descripcion: str) -> Categoria:
        categoria = self.buscar_por_id(identificador)
        for otra in self.listar():
            if otra != categoria and otra.nombre.lower() == nombre.strip().lower():
                raise DuplicadoError("Ya existe una categoría con ese nombre.")
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        return categoria

    def eliminar(self, identificador: int, producto_servicio=None) -> None:
        categoria = self.buscar_por_id(identificador)
        if producto_servicio is not None:
            cantidad = sum(1 for p in producto_servicio.listar() if p.categoria == categoria)
            if cantidad:
                raise OperacionNoPermitidaError(
                    f"No se puede eliminar: la categoría tiene {cantidad} producto(s) activo(s)."
                )
        categoria.eliminado = True