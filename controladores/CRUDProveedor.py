from typing import List
from controladores.conexion import conectar
from modelos.Proveedor import Proveedor

def ConsultarProveedores() -> List[Proveedor]:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from proveedor')

    proveedores: List[Proveedor] = []
    for cursor in BDcursor:
        proveedores.append(Proveedor(cursor[0], cursor[1]))
    BDcursor.close()
    BD.close()
    return proveedores

def AgregarProveedor(idNuevo: int, nombreNuevo: str) -> None:
    proveedor: Proveedor = Proveedor(idNuevo, nombreNuevo)
    datos: dict = eval(proveedor.__repr__())
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into proveedor values (%(id)s, %(nombre)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarProveedor(idNuevo: int, nombreNuevo: str) -> None:
    proveedor: Proveedor = Proveedor(idNuevo, nombreNuevo)
    datos: dict = eval(proveedor.__repr__())

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('update proveedor set nombre=%(nombre)s where id_proveedor=%(id)s', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EliminarProveedor(idEliminar: int) -> None:
    from controladores.CRUDProductoProveedor import EliminarProductoProveedorPorProveedor
    EliminarProductoProveedorPorProveedor(idEliminar)
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from proveedor where id_proveedor=%s', (idEliminar, ))
    BD.commit()
    BDcursor.close()
    BD.close()

def BuscarProveedor(idBuscar: int):
    proveedores: List[Proveedor] = [proveedor for proveedor in ConsultarProveedores() if proveedor.id == idBuscar]
    if len(proveedores) == 0:
        return None
    return proveedores[0]

def ExisteProveedor(idBuscar: int) -> bool:
    return BuscarProveedor(idBuscar) != None

