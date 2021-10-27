from typing import List
from controladores.conexion import conectar
from modelos.Producto import Producto
from modelos.Proveedor import Proveedor
from modelos.ProductoProveedor import ProductoProveedor
from controladores.CRUDProducto import ConsultarProductos
from controladores.CRUDProveedor import ConsultarProveedores

def ConsultarProductosProveedores() -> List[ProductoProveedor]:
    productos: List[Producto] = ConsultarProductos()
    proveedores: List[Proveedor] = ConsultarProveedores()
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('select * from producto_proveedor')

    productosProveedores: List[ProductoProveedor] = []
    for cursor in BDcursor:
        producto: Producto = [i for i in productos if i.id == cursor[1]][0]
        proveedor: Proveedor = [i for i in proveedores if i.id == cursor[2]][0]
        productosProveedores.append(ProductoProveedor(cursor[0], producto, proveedor))
    BDcursor.close()
    BD.close()
    return productosProveedores

def AgregarProductoProveedor(idProveedor: int, idProducto: int) -> None:
    datos: dict = {}
    datos['producto'] = idProducto
    datos['proveedor'] = idProveedor

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into producto_proveedor (id_producto, id_proveedor) values (%(producto)s, %(proveedor)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarProductoProveedor(idBuscarProveedor: int, idBuscarProducto: int, agregar: bool) -> None:
    if agregar:
        AgregarProductoProveedor(idBuscarProveedor, idBuscarProducto)
    else:
        productoProveedor: ProductoProveedor = BuscarProductoProveedor(idBuscarProveedor, idBuscarProducto)
        EliminarProductoProveedor(productoProveedor.id)

def BuscarProductoProveedor(idBuscarProveedor: int, idBuscarProducto: int) -> ProductoProveedor:
    return [pp for pp in ConsultarProductosProveedores() if pp.proveedor.id == idBuscarProveedor and pp.producto.id == idBuscarProducto][0]

def EliminarProductoProveedor(idEliminar: int) -> None:
    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('delete from producto_proveedor where id=%s', (idEliminar, ))
    BD.commit()
    BDcursor.close()
    BD.close()

def EliminarProductoProveedorPorProveedor(idEliminar: int) -> None:
    for producto_proveedor in [pp for pp in ConsultarProductosProveedores() if pp.proveedor.id == idEliminar]:
        EliminarProductoProveedor(producto_proveedor.id)

def EliminarProductoProveedorPorProducto(idEliminar: int) -> None:
    for producto_proveedor in [pp for pp in ConsultarProductosProveedores() if pp.producto.id == idEliminar]:
        EliminarProductoProveedor(producto_proveedor.id)

def BuscarProductosDelProveedor(idProveedor: int) -> List[Producto]:
    return [d.producto for d in ConsultarProductosProveedores() if d.proveedor.id == idProveedor]

def BuscarNoProductosDelProveedor(idProveedor: int) -> List[Producto]:
    productosProveedor = BuscarProductosDelProveedor(idProveedor)
    productos = ConsultarProductos()
    productosFiltro = []
    for p in productos:
        insertar = True
        for pp in productosProveedor:
            if pp.id == p.id:
                insertar = False
        if insertar:
            productosFiltro.append(p)
    return productosFiltro

