import os
from flask import Flask, render_template, request, redirect, session
from controladores.CRUDUsuario import ConsultarUsuarios, AgregarUsuario, EditarUsuario, EliminarUsuario, ExisteUsuario, BuscarUsuario
from controladores.CRUDProducto import ConsultarProductos, AgregarProducto,EditarProducto, EliminarProducto, ExisteProducto, BuscarIdProducto, BuscarProductoPorId
from controladores.CRUDProveedor import ConsultarProveedores, AgregarProveedor, EditarProveedor, EliminarProveedor, ExisteProveedor, BuscarProveedor
from controladores.CRUDProductoProveedor import BuscarProductosDelProveedor
from miscelaneos.misc import ListaATabla, CifrarContrasena, SALT

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= './static/img'
app.secret_key = SALT

usuarios_bd = []
productos_bd = []
proveedores_bd = []

esta_registrado = False
usuario_registrado = None

'''Para debugging'''
esta_registrado = ExisteUsuario(123) # Colocar su id para registrarse
if esta_registrado:
    usuario_registrado = BuscarUsuario(123) # Colocar su id para registrarse
print('No olvidar borrar')

'''Falta validar rol de usuario en las diferentes páginas'''
'''Falta validar los inputs por si se eliminan en html. Ej: <input type="number" max="2147483647"> -> <input type="number">'''
'''Falta añadir la posibilidad de agregar o eliminar producto proveedor'''
'''Opcional: Cookies para sesión'''

def TraerUsuarios():
    global usuarios_bd
    usuarios_bd.clear()
    for usuario in ConsultarUsuarios():
        usuarios_bd.append(usuario)

def TraerProductos():
    global productos_bd
    productos_bd.clear()
    for producto in ConsultarProductos():
        productos_bd.append(producto)

def TraerProveedores():
    global proveedores_bd
    proveedores_bd.clear()
    for proveedor in ConsultarProveedores():
        proveedores_bd.append(proveedor)

@app.route('/', methods=['GET'])
def index():
    global esta_registrado, usuario_registrado
    esta_registrado = False
    usuario_registrado = None
    error = session.pop('error', '')
    return render_template('index.html', error=error)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    global esta_registrado, usuario_registrado, usuarios_bd
    if request.method == 'POST':
        esta_registrado = False
        usuario_registrado = None
        id_usuario = request.form['user']
        password = request.form['password']
        if id_usuario == '' and password == '':
            session['error'] = 'Usuario y contraseña no deben estar en blanco'
            return redirect('/')
        id_usuario = int(id_usuario)
        password = CifrarContrasena(password)
        if usuarios_bd == []:
            TraerUsuarios()
        for usuario in usuarios_bd:
            if usuario.id == id_usuario:
                if password == usuario.contrasena:
                    esta_registrado = True
                    usuario_registrado = usuario
                    session['error'] = ''
                    return redirect('/dashboard')
                session['error'] = 'Contraseña incorrecta'
                return redirect('/')
        session['error'] = 'Usuario no registrado'
        return redirect('/')
    if esta_registrado:
        session['error'] = ''
        return render_template('dashboard.html', usuario_registrado=usuario_registrado)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/usuarios/consultar', methods=['GET'])
def usuarios():
    global esta_registrado, usuarios_bd, usuario_registrado
    if esta_registrado:
        session['error'] = ''
        if usuarios_bd == []:
            TraerUsuarios()
        if usuario_registrado.rol.id != 0:
            return render_template('usuarios.html', usuarios=ListaATabla(usuarios_bd, 3), usuario_registrado=usuario_registrado)
        return redirect('/dashboard')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/usuarios/agregar', methods=['GET','POST'])
def usuariosAgregar():
    global esta_registrado, usuarios_bd, usuario_registrado
    if request.method == 'POST':
        id_nuevo = request.form['id']
        nombre_nuevo = request.form['nombre']
        password_nuevo = request.form['password']
        password_confirm = request.form['password2']
        rol_nuevo = request.form['rol']
        imagen_usuario = request.files['imagen']
        if id_nuevo == '' or nombre_nuevo == '' or password_nuevo == '' or rol_nuevo == 'Seleccione' or imagen_usuario.filename == '':
            session['error'] = 'Todos los campos son obligatorios'
            return redirect('/usuarios/agregar')
        if password_nuevo != password_confirm:
            session['error'] = 'Las contraseñas deben de coincidir'
            return redirect('/usuarios/agregar')
        if usuarios_bd == []:
            TraerUsuarios()
        id_nuevo = int(id_nuevo)
        rol_nuevo = int(rol_nuevo)
        if ExisteUsuario(id_nuevo):
            session['error'] = 'Id \'%d\' de usuario ya existe en el sistema' % id_nuevo
            return redirect('/usuarios/agregar')
        ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Usuarios', str(id_nuevo)+'.jpg')
        imagen_usuario.save(ruta_guardar)
        AgregarUsuario(id_nuevo, nombre_nuevo, password_nuevo, rol_nuevo)
        TraerUsuarios()
        session['error'] = ''
        return redirect('/usuarios/consultar')
    if esta_registrado:
        if usuario_registrado.rol.id != 0:
            error = session.pop('error', '')
            return render_template('usuariosAgregar.html', usuario_registrado=usuario_registrado, error=error)
        return redirect('/dashboard')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/usuarios/editar', methods=['GET', 'POST'])
def usuariosEditar():
    global esta_registrado, usuarios_bd, usuario_registrado
    if request.method == 'POST':
        id_nuevo = int(request.form['id'])
        nombre_nuevo = request.form['nombre']
        password_nuevo = request.form['password']
        password_confirm = request.form['password2']
        rol_nuevo = int(request.form['rol'])
        if nombre_nuevo == '':
            session['error'] = 'El campo de nombre es obligatorio'
            return redirect('/usuarios/editar')
        if password_nuevo != password_confirm:
            session['error'] = 'Las contraseñas deben de coincidir'
            return redirect('/usuarios/editar')
        session['error'] = ''
        cambiar_contrasena = password_nuevo != ''
        EditarUsuario(id_nuevo, nombre_nuevo, password_nuevo, rol_nuevo, cambiar_contrasena)
        imagen_usuario = request.files['imagen']
        if imagen_usuario.filename != '':
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Usuarios', str(id_nuevo)+'.jpg')
            imagen_usuario.save(ruta_guardar)
        TraerUsuarios()
        return redirect('/usuarios/consultar')
    if esta_registrado:
        if usuarios_bd == []:
            TraerUsuarios()
        if usuario_registrado.rol.id != 0:
            error = session.pop('error', '')
            return render_template('usuariosEditar.html', usuarios=usuarios_bd, usuario_registrado=usuario_registrado, error=error)
        return redirect('/dashboard')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/usuarios/editar/usuario', methods=['POST'])
def usuariosEditarusuario():
    global esta_registrado, usuarios_bd, usuario_registrado
    if request.method == 'POST':
        if esta_registrado:
            if len(request.form) == 1:
                id_usuario = int(request.form['id'])
                if usuarios_bd == []:
                    TraerUsuarios()
                usuario_editar = BuscarUsuario(id_usuario)
                return render_template('usuariosEditarusuario.html', usuario=usuario_editar, usuario_registrado=usuario_registrado)
            session['error'] = 'Si deseas editar un usuario, selecciona cual de todos'
            return redirect('/usuarios/editar')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/usuarios/eliminar', methods=['GET','POST'])
def usuariosEliminar():
    global esta_registrado, usuarios_bd, usuario_registrado
    if request.method == 'POST':
        usuarios_eliminar = [int(u) for u in request.form.values()]
        if len(usuarios_eliminar) == 0:
            session['error'] = 'Si deseas eliminar usuarios, seleccione todos los usuarios que desee eliminar. Sea cuidadoso'
            return redirect('/usuarios/eliminar')
        for id_usuario in usuarios_eliminar:
            EliminarUsuario(id_usuario)
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Usuarios', str(id_usuario)+'.jpg')
            if os.path.exists(ruta_guardar):
                os.remove(ruta_guardar)
        TraerUsuarios()
        return redirect('/usuarios/consultar')
    if esta_registrado:
        if usuario_registrado.rol.id != 0:
            if usuarios_bd == []:
                TraerUsuarios()
            error = session.pop('error', '')
            return render_template('usuariosEliminar.html', usuarios=usuarios_bd, usuario_registrado=usuario_registrado, error=error)
        return redirect('/dashboard')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/consultar', methods=['GET', 'POST'])
def productos():
    global esta_registrado, usuario_registrado, productos_bd
    if esta_registrado:
        session['error'] = ''
        if productos_bd == []:
            TraerProductos()
        return render_template('productos.html', usuario_registrado=usuario_registrado, productos = ListaATabla(productos_bd, 3))
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/agregar', methods=['GET','POST'])
def productosAgregar():
    global esta_registrado, usuario_registrado
    if request.method =="POST":
        nombre_producto = request.form['nombreProduct']
        descripcion_producto = request.form['DescProduct']
        calificacion_producto = request.form['calific']
        cantidad_minima = request.form['canMin']
        cantidad_disponible = request.form['canDisp']
        imagen_producto = request.files['imagen']
        if nombre_producto == '' or descripcion_producto == '' or calificacion_producto == 'Seleccione' or cantidad_minima == '' or cantidad_disponible == '' or imagen_producto.filename == '':
            session['error'] = 'Todos los campos son obligatorios'
            return redirect('/productos/agregar')
        if productos_bd == []:
            TraerProductos()
        calificacion_producto = float(calificacion_producto)
        cantMinima = int(cantidad_minima)
        cantDisponible = int(cantidad_disponible)
        if ExisteProducto(nombre_producto):
            session['error'] = 'El producto %s ya existe en el sistema' % nombre_producto.__repr__()
            return redirect('/productos/agregar')
        AgregarProducto(nombre_producto, descripcion_producto, calificacion_producto, cantMinima, cantDisponible)
        ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Productos', str(BuscarIdProducto(nombre_producto))+'.jpg')
        imagen_producto.save(ruta_guardar)
        TraerProductos()
        session['error'] = ''
        return redirect('/productos/consultar')
    if esta_registrado:
        error = session.pop('error', '')
        return render_template('productosAgregar.html', usuario_registrado=usuario_registrado, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/editar', methods=['GET','POST'])
def productosEditar():
    global esta_registrado, usuario_registrado, productos_bd
    if request.method =="POST":
        id_producto = int(request.form['id'])
        nombre_producto = request.form['nombreProduct']
        if ExisteProducto(nombre_producto):
            session['error'] = 'El producto %s ya existe en el sistema' % nombre_producto.__repr__()
            return redirect('/productos/editar')
        descripcion_producto = request.form['DescProduct']
        calificacion_producto = float(request.form['calific'])
        cantidad_minima = request.form['canMin']
        cantidad_disponible = request.form['canDisp']
        imagen_producto = request.files['imagen']
        if nombre_producto == '' or descripcion_producto == '' or cantidad_minima == '' or cantidad_disponible == '':
            session['error'] = 'Los campos nombre, descripción, cantidad mínima y cantidad disponible son obligatorios'
            return redirect('/productos/editar')
        session['error'] = ''
        cantidad_minima = int(cantidad_minima)
        cantidad_disponible = int(cantidad_disponible)
        EditarProducto(id_producto, nombre_producto, descripcion_producto, calificacion_producto, cantidad_minima, cantidad_disponible)
        if imagen_producto.filename != '':
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Productos', str(id_producto)+'.jpg')
            imagen_producto.save(ruta_guardar)
        TraerProductos()
        return redirect('/productos/consultar')
    if esta_registrado:
        if productos_bd == []:
            TraerProductos()
        error = session.pop('error', '')
        return render_template('productosEditar.html', usuario_registrado=usuario_registrado, productos = productos_bd, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/editar/producto', methods=['POST'])
def productosEditarproducto():
    global esta_registrado, usuario_registrado, productos_bd
    if request.method =="POST":
        if esta_registrado:
            if len(request.form) == 1:
                id_producto = int(request.form['id'])
                if productos_bd == []:
                    TraerProductos()
                producto_editar = BuscarProductoPorId(id_producto)
                return render_template('productosEditarproducto.html', producto=producto_editar, usuario_registrado=usuario_registrado)
            session['error'] = 'Si deseas editar un producto, selecciona cual de todos'
            return redirect('/productos/editar')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/eliminar', methods=['GET','POST'])
def productosEliminar():
    global esta_registrado, usuario_registrado, productos_bd
    if request.method == 'POST':
        productos_eliminar = [int(p) for p in request.form.values()]
        if len(productos_eliminar) == 0:
            session['error'] = 'Si deseas eliminar productos, seleccione todos los productos que desee eliminar'
            return redirect('/productos/eliminar')
        for id_producto in productos_eliminar:
            EliminarProducto(id_producto)
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Productos', str(id_producto)+'.jpg')
            if os.path.exists(ruta_guardar):
                os.remove(ruta_guardar)
        TraerProductos()
        return redirect('/productos/consultar')
    if esta_registrado:
        if productos_bd == []:
            TraerProductos()
        error = session.pop('error', '')
        return render_template('productosEliminar.html', productos=productos_bd, usuario_registrado=usuario_registrado, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/consultar', methods=['GET'])
def proveedores():
    global proveedores_bd, esta_registrado, usuario_registrado
    if esta_registrado:
        session['error'] = ''
        if proveedores_bd == []:
            TraerProveedores()
        return render_template('proveedores.html', usuario_registrado=usuario_registrado, proveedores=ListaATabla(proveedores_bd, 2))
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/agregar', methods=['GET','POST'])
def proveedoresAgregar():
    global esta_registrado, usuario_registrado
    if request.method == 'POST':
        id_proveedor = request.form['id']
        nombre_proveedor = request.form['nombre']
        imagen_proveedor = request.files['imagen']
        if id_proveedor == '' or nombre_proveedor == '' or imagen_proveedor.filename == '':
            session['error'] = 'Todos los campos son obligatorios'
            return redirect('/proveedores/agregar')
        if proveedores_bd == []:
            TraerProveedores()
        id_proveedor = int(id_proveedor)
        if ExisteProveedor(id_proveedor):
            session['error'] = 'Id \'%d\' de proveedor ya existe en el sistema' % id_proveedor
            return redirect('/proveedores/agregar')
        ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Proveedores', str(id_proveedor)+'.jpg')
        imagen_proveedor.save(ruta_guardar)
        AgregarProveedor(id_proveedor, nombre_proveedor)
        TraerProveedores()
        session['error'] = ''
        return redirect('/proveedores/consultar')
    if esta_registrado:
        error = session.pop('error', '')
        return render_template('proveedoresAgregar.html', usuario_registrado=usuario_registrado, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/editar', methods=['GET','POST'])
def proveedoresEditar():
    global proveedor_bd, esta_registrado, usuario_registrado
    if request.method == 'POST':
        id_proveedor = int(request.form["id"])
        nombre_proveedor = request.form["nombre"]
        if nombre_proveedor == '':
            session['error'] = 'El campo nombre es obligatorio'
            return redirect('/proveedores/editar')
        session['error'] = ''
        EditarProveedor(id_proveedor, nombre_proveedor)
        imagen_proveedor = request.files['imagen']
        if imagen_proveedor.filename != '':
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Proveedores', str(id_proveedor)+'.jpg')
            imagen_proveedor.save(ruta_guardar)
        TraerProveedores()
        return redirect('/proveedores/consultar')
    if esta_registrado:
        if proveedores_bd == []:
            TraerProveedores()
        error = session.pop('error', '')
        return render_template('proveedoresEditar.html', usuario_registrado=usuario_registrado,proveedores=proveedores_bd, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/editar/proveedor', methods = ['POST'])
def proveedoresEditarproveedor():
    global proveedor_bd, esta_registrado, usuario_registrado
    if request.method =='POST':
        if esta_registrado:
            if len(request.form) == 1:
                id_proveedor = int(request.form['id'])
                if proveedores_bd == []:
                    TraerProveedores()
                proveedor_editar = BuscarProveedor(id_proveedor)
                return render_template('proveedoresEditarproveedor.html', proveedor=proveedor_editar, usuario_registrado=usuario_registrado)
            session['error'] = 'Si deseas editar un proveedor, selecciona cual de todos'
            return redirect('/proveedores/editar')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')


@app.route('/proveedores/eliminar', methods=['GET','POST'])
def proveedoresEliminar():
    global proveedores_bd,esta_registrado, usuario_registrado
    if request.method == 'POST':
        proveedores_eliminar = [int(p) for p in request.form.values()]
        if len(proveedores_eliminar) == 0:
            session['error'] = 'Si deseas eliminar proveedores, seleccione todos los proveedores que desee eliminar'
            return redirect('/proveedores/eliminar')
        for id_proveedor in proveedores_eliminar:
            EliminarProveedor(id_proveedor)
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Usuarios', str(id_proveedor)+'.jpg')
            if os.path.exists(ruta_guardar):
                os.remove(ruta_guardar)
        TraerProveedores()
        return redirect('/proveedores/consultar')
    if esta_registrado:
        if proveedores_bd ==[]:
            TraerProveedores()
        error = session.pop('error', '')
        return render_template('proveedoresEliminar.html', usuario_registrado=usuario_registrado, proveedores=proveedores_bd, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedoresProductoagregar')
def proveedoresProductoagregar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        if productos_bd == []:
            TraerProductos()
        error = session.pop('error', '')
        return render_template('proveedoresProductoagregar.html', productos=productos_bd, usuario_registrado=usuario_registrado, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedoresProductoeliminar')
def proveedoresProductoeliminar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        if productos_bd == []:
            TraerProductos()
        error = session.pop('error', '')
        return render_template('proveedoresProductoeliminar.html', productos=productos_bd, usuario_registrado=usuario_registrado, error=error)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/consultar/proveedor/<int:id_proveedor>')
def proveedor(id_proveedor):
    global proveedores_bd, esta_registrado, usuario_registrado
    if esta_registrado:
        if proveedores_bd == []:
            TraerProveedores()
        if ExisteProveedor(id_proveedor):
            proveedor = BuscarProveedor(id_proveedor)
            productos = BuscarProductosDelProveedor(proveedor.id)
            return render_template('informacionProveedor.html', usuario_registrado=usuario_registrado, proveedor=proveedor, productos=ListaATabla(productos, 3))
        return redirect('/proveedores/consultar')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

