from excepciones import EntidadNoEncontradaError

class BaseServicio:
    def __init__(self) -> None:
        self._coleccion: list = []

    def listar(self) -> list:
        return [objeto for objeto in self._coleccion if not objeto.eliminado]

    def buscar_por_id(self, identificador: int):
        for objeto in self._coleccion:
            if objeto.id == identificador and not objeto.eliminado:
                return objeto
        raise EntidadNoEncontradaError(f"No existe una entidad activa con ID {identificador}.")

    def eliminar(self, identificador: int) -> None:
        objeto = self.buscar_por_id(identificador)
        objeto.eliminado = True