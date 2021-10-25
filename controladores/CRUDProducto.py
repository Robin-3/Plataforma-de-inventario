from typing import List
from controladores.conexion import conectar
from modelos.Producto import Producto

def ConsultarProductos() -> List[Producto]:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from producto')

    productos: list[Producto] = []
    for cursor in BDcursor:
        productos.append(Producto(cursor[0], cursor[1], cursor[2], cursor[3], cursor[4], cursor[5]))
    BDcursor.close()
    BD.close()
    return productos

def AgregarProducto(nombreNuevo: str, descripcionNueva: str, calificacionNueva: float, minimoNuevo: int, disponibleNuevo: int) -> None:
    producto: Producto = Producto(0, nombreNuevo, descripcionNueva, calificacionNueva, minimoNuevo, disponibleNuevo)
    datos: dict = eval(producto.__repr__())

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into producto (nombre_producto, descripcion, calificacion, cantidad_minima_requerida, cantidad_disponible_en_bodega) values (%(nombre)s, %(descripción)s, %(calificación)s, %(mínimo)s, %(disponible)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarProducto(idNuevo: int, nombreNuevo: str, descripcionNueva: str, calificacionNueva: float, minimoNuevo: int, disponibleNuevo: int) -> None:
    producto: Producto = Producto(idNuevo, nombreNuevo, descripcionNueva, calificacionNueva, minimoNuevo, disponibleNuevo)
    datos: dict = eval(producto.__repr__())

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('update producto set nombre_producto=%(nombre)s, descripcion=%(descripción)s, calificacion=%(calificación)s, cantidad_minima_requerida=%(mínimo)s, cantidad_disponible_en_bodega=%(disponible)s where id_producto=%(id)s', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EliminarProducto(idEliminar: int) -> None:
    from controladores.CRUDProductoProveedor import EliminarProductoProveedorPorProducto
    EliminarProductoProveedorPorProducto(idEliminar)
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from producto where id_producto=%s', (idEliminar, ))
    BD.commit()
    BDcursor.close()
    BD.close()

def BuscarProducto(nombreBuscar: str):
    productos: List[Producto] = [producto for producto in ConsultarProductos() if producto.nombre == nombreBuscar]
    if len(productos) == 0:
        return None
    return productos[0]

def ExisteProducto(nombreBuscar: str) -> bool:
    return BuscarProducto(nombreBuscar) != None

def BuscarIdProducto(nombreBuscar: str) -> int:
    producto = BuscarProducto(nombreBuscar)
    if producto == None:
        return -1
    return producto.id

def BuscarProductoPorId(idBuscar: int):
    productos: List[Producto] = [producto for producto in ConsultarProductos() if producto.id == idBuscar]
    if len(productos) == 0:
        return None
    return productos[0]

