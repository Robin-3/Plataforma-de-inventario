from modelos.Producto import Producto
from modelos.Proveedor import Proveedor

class ProductoProveedor:

    def __init__(self, id: int, producto: Producto, proveedor: Proveedor) -> None:
        self.__id: int = id
        self.__producto: Producto = producto
        self.__proveedor: Proveedor = proveedor

    @property
    def id(self) -> int:
        return self.__id
    @id.setter
    def id(self, x) -> None:
        pass

    @property
    def producto(self) -> Producto:
        return self.__producto
    @producto.setter
    def producto(self, x) -> None:
        pass

    @property
    def proveedor(self) -> Proveedor:
        return self.__proveedor
    @proveedor.setter
    def proveedor(self, x) -> None:
        pass

    def __repr__(self) -> str:
        return str({'id': self.__id, 'producto': self.__producto.nombre, 'proveedor': self.__proveedor.nombre})
