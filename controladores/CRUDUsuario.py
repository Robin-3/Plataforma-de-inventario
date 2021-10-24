from typing import List
from controladores.conexion import conectar
from modelos.Rol import Rol
from controladores.CRUDRol import ObtenerRoles
from modelos.Usuario import Usuario
from miscelaneos.misc import CifrarContrasena

ROLES: List[Rol] = ObtenerRoles()

def ConsultarUsuarios() -> List[Usuario]:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from usuario')

    usuarios: List[Usuario] = []
    for cursor in BDcursor:
        rol: Rol = [i for i in ROLES if i.id == cursor[3]][0]
        usuarios.append(Usuario(cursor[0], cursor[1], cursor[2], rol))
    BDcursor.close()
    BD.close()
    return usuarios

def AgregarUsuario(idNuevo: int, nombreNuevo: str, contrasenaNueva: str, rolNuevo: int) -> None:
    usuario: Usuario = Usuario(idNuevo, nombreNuevo, contrasenaNueva, ROLES[rolNuevo])
    datos: dict = eval(usuario.__repr__())
    datos['contraseña'] = CifrarContrasena(datos['contraseña'])
    datos['rol'] = rolNuevo

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into usuario values (%(id)s, %(nombre)s, %(contraseña)s, %(rol)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarUsuario(idNuevo: int, nombreNuevo: str, contrasenaNueva: str, rolNuevo: int, cambioContrasena: bool) -> None:
    usuario: Usuario = Usuario(idNuevo, nombreNuevo, contrasenaNueva, ROLES[rolNuevo])
    datos: dict = eval(usuario.__repr__())
    datos['rol'] = rolNuevo

    BD = conectar()
    BDcursor = BD.cursor()
    query = 'update usuario set nombre_usuario=%(nombre)s, id_rol=%(rol)s where id_usuario=%(id)s'
    if cambioContrasena:
        datos['contraseña'] = CifrarContrasena(datos['contraseña'])
        query = 'update usuario set nombre_usuario=%(nombre)s, id_rol=%(rol)s, contrasena=%(contraseña)s where id_usuario=%(id)s'
    BDcursor.execute(query, datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EliminarUsuario(idEliminar: int) -> None:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from usuario where id_usuario=%s', (idEliminar, ))
    BD.commit()
    BDcursor.close()
    BD.close()

def BuscarUsuarios(idBuscar: int) -> List[Usuario]:
    return [usuario for usuario in ConsultarUsuarios() if usuario.id == idBuscar]

def ExisteUsuario(idBuscar: int) -> bool:
    return len(BuscarUsuarios(idBuscar)) > 0

