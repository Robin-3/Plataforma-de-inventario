from modelos.Rol import Rol
from controladores.CRUDRol import ObtenerRoles
from modelos.Usuario import Usuario
from controladores.CRUDUsuario import *
from modelos.Producto import Producto
from controladores.CRUDProducto import *
from modelos.Proveedor import Proveedor
from controladores.CRUDProveedor import *
from modelos.ProductoProveedor import ProductoProveedor
from controladores.CRUDProductoProveedor import *

def ImprimirListaObjetos(lista: list):
    for objeto in lista:
        for valor in eval(objeto.__repr__()).items():
            print(f"  {valor[0]}: {valor[1]}")
        print()

if __name__ == '__main__':

    AgregarProveedor(Proveedor(87659874, 'Perla Paz'))
    AgregarProveedor(Proveedor(8965874, 'DB organization'))
    AgregarProveedor(Proveedor(87567356, 'START S.A'))
    AgregarProveedor(Proveedor(54685886, 'Jesús Reales'))
    AgregarProveedor(Proveedor(6545321, 'Go S.A'))
    AgregarProveedor(Proveedor(46857679, 'Jorge Aristizabal'))


    '''
    roles: list[Rol] = ObtenerRoles()
    AgregarUsuario(Usuario(1023456876, 'Ana Díaz', '1'), roles[0])
    AgregarUsuario(Usuario(2345678, 'Carlos Paez', '2'), roles[0])
    AgregarUsuario(Usuario(98764523, 'Milena García', '3'), roles[1])
    AgregarUsuario(Usuario(7799654, 'Pedro Rincón', '4'), roles[1])
    AgregarUsuario(Usuario(6545321, 'Rosa Hernández', '5'), roles[2])
    AgregarUsuario(Usuario(95341236, 'Yesid Rodríguez', '6'), roles[2])
    '''
    '''roles: list[Rol] = ObtenerRoles()
    print("--------------------ROLES: MOSTRAR---------")
    ImprimirListaObjetos(ObtenerRoles())

    print("-----------------USUARIOS: MOSTRAR---------")
    ImprimirListaObjetos(ConsultarUsuarios())

    print("----------------PRODUCTOS: MOSTRAR---------")
    ImprimirListaObjetos(ConsultarProductos())

    print("--------------PROVEEDORES: MOSTRAR---------")
    ImprimirListaObjetos(ConsultarProvedores())

    print("--------PRODUCTOPROVEEDOR: MOSTRAR---------")
    ImprimirListaObjetos(ConsultarProductosProveedores())

    print("-----------------USUARIOS: AGREGAR---------")
    # Necesita un usuario y un rol
    nuevoUsuario = Usuario(23456789, 'Carlos Paez', 'qwerty') # Necesita: id, nombre, contraseña
    AgregarUsuario(nuevoUsuario, roles[1]) # roles[0] = Usuario final, roles[1] = Administrador, roles[2] = Super Administrador
    ImprimirListaObjetos(ConsultarUsuarios())

    print("----------------PRODUCTOS: AGREGAR---------")
    # Necesita un producto
    nuevoProducto = Producto(3, 'Camioneta', 'Cinco llantas', 5.0, 50, 0) # Necesita: id[autoincremetal], nombre, descripción, calificación, mínimo, disponible
    AgregarProducto(nuevoProducto)
    productoCopia: Producto = ConsultarProductos()[-1]
    ImprimirListaObjetos(ConsultarProductos())

    print("--------------PROVEEDORES: AGREGAR---------")
    # Necesita un proveedor
    nuevoProveedor = Proveedor(4, 'Carro Mio') # Necesita: id, nombre
    AgregarProveedor(nuevoProveedor)
    ImprimirListaObjetos(ConsultarProvedores())

    print("--------PRODUCTOPROVEEDOR: AGREGAR---------")
    # Necesita un productoProveedor[producto, proveedor]
    nuevoProductoProveedor = ProductoProveedor(0, productoCopia, nuevoProveedor)
    AgregarProductoProveedor(nuevoProductoProveedor)
    productoProveedorCopia = ConsultarProductosProveedores()[-1]
    ImprimirListaObjetos(ConsultarProductosProveedores())

    print("-----------------USUARIOS: EDITAR----------")
    # Necesita un id, usuario, rol y contraseña[opcional]
    nuevoUsuario = Usuario(0, 'Milena García', 'iloveyou')
    EditarUsuario(23456789, nuevoUsuario, roles[2], True)
    ImprimirListaObjetos(ConsultarUsuarios())

    print("----------------PRODUCTOS: EDITAR----------")
    # Necesita un id, producto
    nuevoProducto = Producto(0, 'Triciclo', 'Tres llantas', 5.2, 3, 3)
    EditarProducto(productoCopia.id, nuevoProducto)
    ImprimirListaObjetos(ConsultarProductos())

    print("--------------PROVEEDORES: EDITAR----------")
    # Necesita un id, proveedor
    nuevoProveedor = Proveedor(0, 'Carro = Status')
    EditarProveedor(4, nuevoProveedor)
    ImprimirListaObjetos(ConsultarProvedores())

    # print("--------PRODUCTOPROVEEDOR: EDITAR----------")
    # Necesita un id, ProductoProveedor

    print("-----------------USUARIOS: ELIMINAR--------")
    # Necesita un id
    EliminarUsuario(23456789)
    ImprimirListaObjetos(ConsultarUsuarios())

    print("--------PRODUCTOPROVEEDOR: ELIMINAR--------")
    # Necesita un id
    EliminarProductoProveedor(productoProveedorCopia.id)
    ImprimirListaObjetos(ConsultarProductosProveedores())

    print("----------------PRODUCTOS: ELIMINAR--------")
    # Necesita un id
    EliminarProducto(productoCopia.id)
    ImprimirListaObjetos(ConsultarProductos())

    print("--------------PROVEEDORES: ELIMINAR--------")
    # Necesita in id
    EliminarProveedor(4)
    ImprimirListaObjetos(ConsultarProvedores())'''
