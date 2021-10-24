class Producto:

    def __init__(self, id: int, nombre: str, descripcion: str, calificacion: float, minimo: int, disponible: int) -> None:
        self.__id: int = id
        self.__nombre: str = nombre
        self.__descripcion: str = descripcion 
        self.__calificacion: float = calificacion
        self.__minimo: int = minimo
        self.__disponible: int = disponible

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
    def descripcion(self) -> str:
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, x) -> None:
        pass

    @property
    def calificacion(self) -> float:
        return self.__calificacion
    @calificacion.setter
    def calificacion(self, x) -> None:
        pass

    @property
    def minimo(self) -> int:
        return self.__minimo
    @minimo.setter
    def minimo(self, x) -> None:
        pass

    @property
    def disponible(self) -> int:
        return self.__disponible
    @disponible.setter
    def disponible(self, x) -> None:
        pass

    def __repr__(self) -> str:
        return str({'id': self.__id, 'nombre': self.__nombre, 'descripción': self.__descripcion, 'calificación': self.__calificacion, 'mínimo': self.__minimo, 'disponible': self.__disponible})
