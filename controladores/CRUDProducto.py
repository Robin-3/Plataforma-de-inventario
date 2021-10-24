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

def AgregarProducto(producto: Producto) -> None:
    datos: dict = eval(producto.__repr__())

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into producto (nombre_producto, descripcion, calificacion, cantidad_minima_requerida, cantidad_disponible_en_bodega) values (%(nombre)s, %(descripción)s, %(calificación)s, %(mínimo)s, %(disponible)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarProducto(id: int, producto: Producto) -> None:
    datos: dict = eval(producto.__repr__())
    datos['id'] = id

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('update producto set nombre_producto=%(nombre)s, descripcion=%(descripción)s, calificacion=%(calificación)s, cantidad_minima_requerida=%(mínimo)s, cantidad_disponible_en_bodega=%(disponible)s where id_producto=%(id)s', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EliminarProducto(id: int) -> None:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from producto where id_producto=%s', (id, ))
    BD.commit()
    BDcursor.close()
    BD.close()
