from typing import List, List
from controladores.conexion import conectar
from modelos.Rol import Rol

def ObtenerRoles() -> List[Rol]:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from rol')

    roles: List[Rol] = []
    for cursor in BDcursor:
        roles.append(Rol(cursor[0], cursor[1]))
    BDcursor.close()
    BD.close()
    return roles
