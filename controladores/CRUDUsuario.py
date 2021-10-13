from controladores.conexion import conectar
from modelos.Rol import Rol
from controladores.CRUDRol import ObtenerRoles
from modelos.Usuario import Usuario
from miscelaneos.misc import CifrarContrasena

ROLES: list[Rol] = ObtenerRoles()

def ConsultarUsuarios() -> list[Usuario]:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from usuario')

    usuarios: list[Usuario] = []
    for cursor in BDcursor:
        rol: Rol = [i for i in ROLES if i.id == cursor[3]][0]
        usuarios.append(Usuario(cursor[0], cursor[1], cursor[2], rol))
    BDcursor.close()
    BD.close()
    return usuarios

def AgregarUsuario(usuario: Usuario, rol: Rol) -> None:
    datos: dict = eval(usuario.__repr__())
    datos['contraseña'] = CifrarContrasena(datos['contraseña'])
    datos['rol'] = rol.id

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into usuario values (%(id)s, %(nombre)s, %(contraseña)s, %(rol)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarUsuario(id: int, usuario: Usuario, rol: Rol, cambioContrasena: bool=False) -> None:
    datos: dict = eval(usuario.__repr__())
    datos['id'] = id
    datos['rol'] = rol.id

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

def EliminarUsuario(id: int) -> None:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from usuario where id_usuario=%s', (id, ))
    BD.commit()
    BDcursor.close()
    BD.close()
