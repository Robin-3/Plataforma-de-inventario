from modelos.Rol import Rol

class Usuario:

    def __init__(self, id: int, nombre: str, contrasena: str, rol: Rol=None) -> None:
        self.__id: int = id
        self.__nombre: str = nombre
        self.__contrasena: str = contrasena
        self.__rol = rol

    @property
    def id(self) -> int:
        return self.__id
    @id.setter
    def id(self, x) -> None:
        pass

    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self, x) -> None:
        pass

    @property
    def contrasena(self) -> str:
        return self.__contrasena
    @contrasena.setter
    def contrasena(self, x) -> None:
        pass

    @property
    def rol(self):
        return self.__rol
    @rol.setter
    def rol(self, x) -> None:
        pass

    def __repr__(self) -> str:
        if self.__rol != None:
            return str({'id': self.__id, 'nombre': self.__nombre, 'contraseña': self.__contrasena, 'rol': self.__rol.nombre})
        else:
            return str({'id': self.__id, 'nombre': self.__nombre, 'contraseña': self.__contrasena})
