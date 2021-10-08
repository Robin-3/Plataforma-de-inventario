import mysql.connector

def BDconectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="inventario"
    )

def MostrarUsuarios(BD):
    BDcursor = BD.cursor()
    BDcursor.execute('select id_usuario, nombre_usuario, contrasena, nombre from usuario, rol where usuario.id_rol = rol.id_rol')
    usuarios = []
    for x in BDcursor:
        usuarios.append({'id': x[0], 'nombre': x[1], 'contrasena': x[2], 'rol': x[3]})
    return usuarios

def MostrarProductos(BD):
    BDcursor = BD.cursor()
    BDcursor.execute('select * from producto')

    productos = []
    for x in BDcursor:
        productos.append({'id': x[0], 'nombre': x[1], 'descripcion': x[2], 'calificacion': x[3], 'minimo': x[4], 'disponible': x[5]})
    return productos

def MostrarProveedores(BD):
    BDcursor = BD.cursor()
    BDcursor.execute('select * from proveedor')

    proveedores = []
    for x in BDcursor:
        proveedores.append({'id': x[0], 'nombre': x[1]})
    return proveedores

def BDdesconectar(BD):
    BD.close()

inventarioBD = BDconectar()
print(MostrarUsuarios(inventarioBD))
print(MostrarProductos(inventarioBD))
print(MostrarProveedores(inventarioBD))
BDdesconectar(inventarioBD)


