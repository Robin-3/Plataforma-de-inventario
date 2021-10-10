import mysql.connector
from math import ceil
from hashlib import pbkdf2_hmac

SALT = b'Al cesar lo que es del cesar'

def CifrarContrasena(contrasena: str) -> str:
    return pbkdf2_hmac('sha256', contrasena.encode('utf-8'), SALT, 100000).hex()

def ListaATabla(lista: list, numero_columnas: int) -> list[list]:
    return [lista[sublista*numero_columnas:(sublista+1)*numero_columnas] for sublista in range(ceil(len(lista)/numero_columnas))] # if len(lista) > 0 else [[]]

class Rol:
    #Constructor
    def __init__(self, id: int, nombre: str) -> None:
        # Declaro variables privadas
        self.__id: int = id
        self.__nombre: str = nombre
    # Permito el mostrar el contenido de las variables
    @property
    def id(self) -> int:
        return self.__id
    # Prohíbo la alteración de las variables
    @id.setter
    def id(self, x) -> None:
        pass
    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self, x) -> None:
        pass
    # Representación de la clase
    def __repr__(self) -> str:
        return str({'id': self.__id, 'nombre': self.__nombre})

class Usuario:
    def __init__(self, id: int, nombre: str, contrasena: str, rol: Rol=None) -> None:
        self.__id: int = id
        self.__nombre: str = nombre
        self.__contrasena: str = contrasena
        self.__rol = rol
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
    def contrasena(self) -> str:
        return self.__contrasena
    @contrasena.setter
    def contrasena(self, x) -> None:
        pass
    @property
    def rol(self):
        return self.__rol
    @rol.setter
    def rol(self, x) -> None:
        pass
    def __repr__(self) -> str:
        if self.__rol != None:
            return str({'id': self.__id, 'nombre': self.__nombre, 'contraseña': self.__contrasena, 'rol': self.__rol.nombre})
        else:
            return str({'id': self.__id, 'nombre': self.__nombre, 'contrasena': self.__contrasena})

def BDconectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="inventario"
    )

def BDdesconectar(BD) -> None:
    BD.close()

def ObtenerRoles() -> list[Rol]:
    BD = BDconectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from rol')

    roles: list[Rol] = []
    for cursor in BDcursor:
        roles.append(Rol(cursor[0], cursor[1]))
    BDcursor.close()
    BDdesconectar(BD)
    return roles

def ConsultarUsuarios() -> list[Usuario]:
    BD = BDconectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from usuario')

    usuarios: list[Usuario] = []
    for cursor in BDcursor:
        rol = [i for i in ROLES if i.id == cursor[3]][0]
        usuarios.append(Usuario(cursor[0], cursor[1], cursor[2], rol))
    BDcursor.close()
    BDdesconectar(BD)
    return usuarios

def AgregarUsuario(usuario: Usuario, rol: Rol) -> None:
    datos: dict = eval(usuario.__repr__())
    datos['contrasena'] = CifrarContrasena(datos['contrasena'])
    datos['rol'] = rol.id

    BD = BDconectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into usuario values (%(id)s, %(nombre)s, %(contrasena)s, %(rol)s)', datos)

    BD.commit() # Guardar el cambio dentro de la base de datos
    # BD.rollback() # No guardar el cambio en la base de datos
    BDcursor.close()
    BDdesconectar(BD)

def EditarUsuario(id: int, usuario: Usuario, rol: Rol, cambioContrasena: bool=False) -> None:
    datos: dict = eval(usuario.__repr__())
    datos['id'] = id # Para evitar que se modifique un usuario diferente
    datos['rol'] = rol.id

    BD = BDconectar()
    BDcursor = BD.cursor()
    query = 'update usuario set nombre_usuario=%(nombre)s, id_rol=%(rol)s where id_usuario=%(id)s'
    if cambioContrasena:
        datos['contrasena'] = CifrarContrasena(datos['contrasena'])
        query = 'update usuario set nombre_usuario=%(nombre)s, id_rol=%(rol)s, contrasena=%(contrasena)s where id_usuario=%(id)s'
    BDcursor.execute(query, datos)
    BD.commit()
    BDcursor.close()
    BDdesconectar(BD)

def EliminarUsuario(id: int) -> None:
    BD = BDconectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from usuario where id_usuario=%s', (id, ))
    BD.commit()
    BDcursor.close()
    BDdesconectar(BD)


#


def MostrarProductos(numero_columnas=3):
    BD = BDconectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from producto')

    productos = []
    for x in BDcursor:
        productos.append({'id': x[0], 'nombre': x[1], 'descripcion': x[2], 'calificacion': x[3], 'minimo': x[4], 'disponible': x[5]})
    BDdesconectar(BD)
    return ListaATabla(productos, numero_columnas)

def MostrarProveedores():
    BD = BDconectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from proveedor')

    proveedores = []
    for x in BDcursor:
        proveedores.append({'id': x[0], 'nombre': x[1]})
    BDdesconectar(BD)
    return proveedores




ROLES: list[Rol]

if __name__ == '__main__':
    ROLES = ObtenerRoles()
    print("--------ROLES---------")
    print(ROLES)
    print("-------USUARIOS: MOSTRAR-------")
    print(ConsultarUsuarios())
    # Ejemplo de agregar un nuevo usuario
    # Necesita un usuario y un rol
    nuevoUsuario = Usuario(23456789, 'Carlos Paez', 'qwerty') # Necesita: id, nombre, contraseña
    AgregarUsuario(nuevoUsuario, ROLES[1]) # ROLES[0] = Usuario final, ROLES[1] = Administrador, ROLES[2] = Super Administrador
    print("-------USUARIOS: AGREGAR-------")
    print(ConsultarUsuarios())
    # Ejemplo de edición de usuario
    # Necesita un id, usuario, rol y contraseña[opcional]
    nuevoUsuario = Usuario(0, 'Milena García', '')
    EditarUsuario(23456789, nuevoUsuario, ROLES[2])
    print("-------USUARIOS: EDITAR-------")
    print(ConsultarUsuarios())
    # Ejemplo de eliminación de usuario
    # Necesita un id
    EliminarUsuario(23456789)
    print("-------USUARIOS: ELIMINAR-------")
    print(ConsultarUsuarios())






