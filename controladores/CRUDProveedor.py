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

def AgregarProveedor(proveedor: Proveedor) -> None:
    datos: dict = eval(proveedor.__repr__())

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into proveedor values (%(id)s, %(nombre)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarProveedor(id: int, proveedor: Proveedor) -> None:
    datos: dict = eval(proveedor.__repr__())
    datos['id'] = id

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('update proveedor set nombre=%(nombre)s where id_proveedor=%(id)s', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EliminarProveedor(id: int) -> None:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from proveedor where id_proveedor=%s', (id, ))
    BD.commit()
    BDcursor.close()
    BD.close()
