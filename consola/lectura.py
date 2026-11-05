import questionary
from enums import Rol, Estado, FormaPago


def seleccionar_opcion(titulo: str, opciones: list):
    
    return questionary.select(
        titulo,
        choices=opciones,
        instruction="(Usá ↑ ↓ y Enter para seleccionar)"
    ).ask()


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingrese un número entero válido.")


def leer_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje).replace(",", "."))
        except ValueError:
            print("Ingrese un número válido.")


def leer_texto(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El texto no puede estar vacío.")


def leer_opcion_enum(tipo_enum, titulo: str):
    opciones = list(tipo_enum)

    seleccion = seleccionar_opcion(
        titulo,
        [opcion.value for opcion in opciones]
    )

    if seleccion is None:
        raise KeyboardInterrupt

    return next(opcion for opcion in opciones if opcion.value == seleccion)


def leer_sn(mensaje: str) -> bool:
    seleccion = seleccionar_opcion(
        mensaje,
        ["Sí", "No"]
    )

    if seleccion is None:
        raise KeyboardInterrupt

    return seleccion == "Sí"