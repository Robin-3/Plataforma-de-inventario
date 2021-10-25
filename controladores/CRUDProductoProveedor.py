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

def AgregarProductoProveedor(productoProveedor: ProductoProveedor) -> None:
    datos: dict = eval(productoProveedor.__repr__())
    datos['producto'] = productoProveedor.producto.id
    datos['proveedor'] = productoProveedor.proveedor.id

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('insert into producto_proveedor (id_producto, id_proveedor) values (%(producto)s, %(proveedor)s)', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

def EditarProductoProveedor(idBuscar: int, productoProveedor: ProductoProveedor) -> None:
    datos: dict = eval(productoProveedor.__repr__())
    datos['id'] = idBuscar
    datos['producto'] = productoProveedor.producto.id
    datos['proveedor'] = productoProveedor.proveedor.id

    BD = conectar()
    BDcursor = BD.cursor()
    BDcursor.execute('update producto_proveedor set id_producto=%(producto)s, id_proveedor=%(proveedor)s where id=%(id)s', datos)
    BD.commit()
    BDcursor.close()
    BD.close()

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

