from .base_servicio import BaseServicio
from entidades.usuario import Usuario
from enums import Rol
from excepciones import DuplicadoError, CredencialesInvalidasError, DatoInvalidoError

class UsuarioServicio(BaseServicio):
    def crear(self, nombre: str, apellido: str, mail: str, celular: str,
            contrasenia: str, rol: Rol) -> Usuario:
        if any(u.mail == mail.strip().lower() for u in self._coleccion):
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self._coleccion.append(usuario)
        return usuario

    def editar(self, identificador: int, nombre: str, apellido: str, mail: str,
            celular: str, contrasenia: str | None = None, rol: Rol | None = None) -> Usuario:
        usuario = self.buscar_por_id(identificador)
        for otro in self._coleccion:
            if otro != usuario and otro.mail == mail.strip().lower():
                raise DuplicadoError("Ya existe un usuario con ese mail.")
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.mail = mail
        usuario.celular = celular
        if contrasenia:
            usuario.contrasenia = contrasenia
        if rol is not None:
            usuario.rol = rol
        return usuario

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        for usuario in self._coleccion:
            if usuario.mail == mail.strip().lower() and not usuario.eliminado:
                if usuario.verificar_contrasenia(contrasenia):
                    return usuario
                break
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")