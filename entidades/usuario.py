from .base import Base
from enums import Rol
from excepciones import DatoInvalidoError

class Usuario(Base):
    def __init__(self, nombre: str, apellido: str, mail: str, celular: str,
                contrasenia: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia: str = ""
        self.contrasenia = contrasenia
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío.")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El mail debe tener un formato válido.")
        self.__mail = valor.strip().lower()

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío.")
        self.__celular = valor.strip()

    @property
    def contrasenia(self) -> str:
        raise AttributeError("La contraseña no se puede consultar.")

    @contrasenia.setter
    def contrasenia(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor) < 4:
            raise DatoInvalidoError("La contraseña debe tener al menos 4 caracteres.")
        self.__contrasenia = valor

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol seleccionado no es válido.")
        self.__rol = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        return f"ID: {self.id} | {self.nombre} {self.apellido} | {self.mail} | {self.rol.value}"
