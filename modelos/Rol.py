class Rol:

    def __init__(self, id: int, nombre: str) -> None:
        self.__id: int = id
        self.__nombre: str = nombre

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

    def __repr__(self) -> str:
        return str({'id': self.__id, 'nombre': self.__nombre})
