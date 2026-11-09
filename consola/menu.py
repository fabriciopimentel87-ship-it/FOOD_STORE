from abc import ABC, abstractmethod
from excepciones import FoodStoreError
from .lectura import seleccionar_opcion


class Menu(ABC):

    def __init__(self, usuario, servicios: dict) -> None:
        self._usuario = usuario
        self._servicios = servicios

    @abstractmethod
    def mostrar(self) -> bool:
        pass

    def _seleccionar(self, titulo: str, opciones: list):
        seleccion = seleccionar_opcion(titulo, opciones)

        if seleccion is None:
            raise KeyboardInterrupt

        return seleccion

    def _ejecutar_seguro(self, accion) -> None:
        try:
            accion()
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
        except (FoodStoreError, ValueError) as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Se produjo un error inesperado: {error}")

        input("\nPresione Enter para continuar...")