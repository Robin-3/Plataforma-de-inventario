import os
from modelos.Proveedor import Proveedor
from modelos.Producto import Producto
from flask import Flask, render_template, request, redirect, session
from controladores.CRUDUsuario import ConsultarUsuarios, AgregarUsuario, EditarUsuario, EliminarUsuario, ExisteUsuario, BuscarUsuario
from controladores.CRUDProveedor import ConsultarProveedores, AgregarProveedor, EditarProveedor, EliminarProveedor
from controladores.CRUDProducto import ConsultarProductos, AgregarProducto,EditarProducto, EliminarProducto
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
        if id_nuevo == '' or nombre_nuevo == '' or password_nuevo == '' or rol_nuevo == 'Seleccione':
            session['error'] = 'Los campos de id, nombre, contraseña y rol son obligatorios'
            return redirect('/usuarios/agregar')
        if password_nuevo != password_confirm:
            session['error'] = 'Las contraseñas deben de coincidir'
            return redirect('/usuarios/agregar')
        if usuarios_bd == []:
            TraerUsuarios()
        id_nuevo = int(id_nuevo)
        rol_nuevo = int(rol_nuevo)
        if ExisteUsuario(id_nuevo):
            session['error'] = 'Id de usuario ya existente en el sistema'
            return redirect('/usuarios/agregar')
        imagen_usuario = request.files['imagen']
        if imagen_usuario.filename != '':
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
            session['error'] = 'Si deseas editar un usuario, por favor selecciona cual de todos'
            return redirect('/usuarios/editar')
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/usuarios/eliminar', methods=['GET','POST'])
def usuariosEliminar():
    global esta_registrado, usuarios_bd, usuario_registrado
    if request.method == 'POST':
        usuarios_eliminar = [u for u in request.form.values()]
        if len(usuarios_eliminar) == 0:
            session['error'] = 'Si deseas eliminar usuarios, por favor seleccione todos los usuarios que desee eliminar. Sea cuidadoso'
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

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    global esta_registrado, usuario_registrado, productos_bd
    if esta_registrado:
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
        cantMinima = request.form['canMin']
        cantDisponible = request.form['canDisp']
        imagenProduct = request.files['imagen']

        if (nombre_producto == '' or descripcion_producto == '' or calificacion_producto == 'Seleccione' or cantMinima == '' or cantDisponible == ''):
            mensaje = 'Error al intentar agregar el producto, uno o varios campos estaban vacíos. Por favor revise nuevamente los campos'
            return render_template('productosAgregar.html', usuario_registrado=usuario_registrado, mensaje=mensaje)
        if imagenProduct.filename =="":
            mensaje = 'Error: Por favor seleccione una imagen para continuar'
            return render_template('productosAgregar.html', usuario_registrado=usuario_registrado, mensaje=mensaje)
        if productos_bd == []:
            TraerProductos()
        calificacion_producto = float(calificacion_producto)
        cantMinima = int(cantMinima)
        cantDisponible = int(cantDisponible)
        id=0
        for h in productos_bd:
            if h.nombre == nombre_producto:
                mensaje = 'Error: el producto ' + nombre_producto + ' ya existe en el sistema'
                return render_template('productosAgregar.html', usuario_registrado=usuario_registrado, mensaje=mensaje)
        AgregarProducto(Producto(id, nombre_producto, descripcion_producto, calificacion_producto, cantMinima, cantDisponible))
        TraerProductos()
        for h in productos_bd:
            if h.nombre == nombre_producto:
                id = h.id
        if imagenProduct.filename!="":
            ruta_guardar= os.path.join(app.config['UPLOAD_FOLDER']+'/Productos', str(id)+'.jpg')
            imagenProduct.save(ruta_guardar)
        return redirect('/productos')
    if esta_registrado:
        mensaje='False'
        return render_template('productosAgregar.html', usuario_registrado=usuario_registrado, mensaje=mensaje)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/editar', methods=['GET','POST'])
def productosEditar():
    global esta_registrado, usuario_registrado, productos_bd
    if request.method =="POST":
        id = request.form['id']
        nombre_producto = request.form['nombreProduct']
        descripcion_producto = request.form['DescProduct']
        calificacion_producto = request.form['calific']
        cantMinima = request.form['canMin']
        cantDisponible = request.form['canDisp']
        imagenProduct = request.files['imagen']

        if (nombre_producto == '' or descripcion_producto == '' or calificacion_producto == 'Seleccione' or cantMinima == '' or cantDisponible == ''):
            idProducto = int (request.form['id'])
            producto_editar = [h for h in productos_bd if h.id == idProducto][0]
            mensaje = 'Error al intentar editar el producto, uno o varios campos estaban vacíos. Por favor revise nuevamente'
            return render_template('productosEditarproducto.html', producto=producto_editar, usuario_registrado=usuario_registrado, mensaje=mensaje)
        if productos_bd == []:
            TraerProductos()
        id = int(id)
        calificacion_producto = float(calificacion_producto)
        cantMinima = int(cantMinima)
        cantDisponible = int(cantDisponible)
        EditarProducto(id, Producto(id, nombre_producto, descripcion_producto, calificacion_producto, cantMinima, cantDisponible))
        TraerProductos()
        if imagenProduct.filename!="":
            ruta_guardar= os.path.join(app.config['UPLOAD_FOLDER']+'/Productos', str(id)+'.jpg')
            imagenProduct.save(ruta_guardar)
        return redirect('/productos/editar')    
    if esta_registrado:
        if productos_bd == []:
            TraerProductos()
        return render_template('productosEditar.html', usuario_registrado=usuario_registrado, productos = productos_bd)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/editar/producto', methods=['POST'])
def productosEditarproducto():
    global esta_registrado, usuario_registrado, productos_bd
    if request.method =="POST":
        idProducto = int (request.form['id'])
        producto_editar = [h for h in productos_bd if h.id == idProducto][0]
    if esta_registrado:
        if productos_bd == []:
            TraerProductos()
        mensaje='False'
        return render_template('productosEditarproducto.html', producto=producto_editar, usuario_registrado=usuario_registrado, productos = productos_bd, mensaje=mensaje)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/productos/eliminar', methods=['GET','POST'])
def productosEliminar():
    global esta_registrado, usuario_registrado, productos_bd
    if request.method == 'POST':
        for producto in [h for h in request.form.values()]:
            EliminarProducto(producto)
        TraerProductos()
        return redirect('/productos')
    
    
    if esta_registrado:
        if productos_bd ==[]:
            TraerProductos()
        return render_template('productosEliminar.html', productos = productos_bd, usuario_registrado=usuario_registrado)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores', methods=['GET'])
def proveedores():
    global proveedores_bd, esta_registrado, usuario_registrado
    if esta_registrado:
        if proveedores_bd == []:
            TraerProveedores()
        return render_template('proveedores.html', usuario_registrado=usuario_registrado, proveedores = ListaATabla(proveedores_bd, 2))
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/agregar', methods=['GET','POST'])
def proveedoresAgregar():
    global esta_registrado, usuario_registrado
    if request.method =="POST":
        id_nuevoprov = request.form['id']
        nombre_nuevoprov = request.form['nombre']
        if (id_nuevoprov == '' or nombre_nuevoprov == ''):
            return redirect('/proveedores/agregar')
        if proveedores_bd == []:
            TraerProveedores()
        id_nuevoprov = int(id_nuevoprov)
        if len([u for u in proveedores_bd if u.id == id_nuevoprov]) == 1:
            return redirect('/proveedores/agregar')
        imagen_prov = request.files['imagen']
        if imagen_prov.filename != '':
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/proveedores', str(id_nuevoprov)+'.jpg')
            imagen_prov.save(ruta_guardar)
        AgregarProveedor(Proveedor(id_nuevoprov, nombre_nuevoprov))
        TraerProveedores()
        return redirect('/proveedores')
    if esta_registrado:
        return render_template('proveedoresAgregar.html', usuario_registrado=usuario_registrado)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/editar', methods=['GET','POST'])
def proveedoresEditar():
    global proveedor_bd,esta_registrado, usuario_registrado
    if request.method == "POST":
        id_nuevoprov = int(request.form["id"])
        nombre_nuevoprov = request.form["nombre"]
        if nombre_nuevoprov == "":
            return redirect("/proveedores/editar")
        EditarProveedor (id_nuevoprov, Proveedor(55,nombre_nuevoprov))
        imagen_prov = request.files['imagen']
        if imagen_prov.filename != '':
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/proveedores', str(id_nuevoprov)+'.jpg')
            imagen_prov.save(ruta_guardar)
        TraerProveedores()
        return redirect('/proveedores')
    if esta_registrado:
        if proveedores_bd == []:
            TraerProveedores()
        return render_template('proveedoresEditar.html', usuario_registrado=usuario_registrado,Proveedores= proveedores_bd)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/editar/proveedor', methods = ['POST'])
def proveedoresEditarproveedor():
    global proveedor_bd,esta_registrado, usuario_registrado
    if request.method =="POST":
        id_nuevoprov = int (request.form['id'])
        if esta_registrado:
            if proveedores_bd == []:
                TraerProveedores()
            proveedores_editar = [u for u in proveedores_bd if u.id == id_nuevoprov][0]
            return render_template('proveedoresEditarproveedor.html', proveedor=proveedores_editar, usuario_registrado=usuario_registrado)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')


@app.route('/proveedores/eliminar', methods=['GET','POST'])
def proveedoresEliminar():
    global proveedores_bd,esta_registrado, usuario_registrado
    if request.method == 'POST':
        for proveedor in [p for p in request.form.values()]:
            EliminarProveedor(proveedor)
        TraerProveedores()
        return redirect('/proveedores')
    if esta_registrado:
        if proveedores_bd ==[]:
            TraerProveedores()
        return render_template('proveedoresEliminar.html', usuario_registrado=usuario_registrado, proveedores = proveedores_bd)
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')

@app.route('/proveedores/consultar/proveedor/<int:id_proveedor>')
def proveedor(id_proveedor):
    global proveedores_bd, esta_registrado, usuario_registrado
    if esta_registrado:
        if proveedores_bd == []:
            TraerProveedores()
        proveedor = [p for p in proveedores_bd if p.id == id_proveedor][0]
        productos = BuscarProductosDelProveedor(proveedor.id)
        return render_template('informacionProveedor.html', usuario_registrado=usuario_registrado, proveedor=proveedor, productos=ListaATabla(productos, 3))
    session['error'] = 'Debes de registrarte para usar la aplicación'
    return redirect('/')
