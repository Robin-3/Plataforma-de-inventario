import os
from modelos.Proveedor import Proveedor
from flask import Flask, render_template, request, redirect
from controladores.CRUDUsuario import BuscarUsuarios, ConsultarUsuarios, AgregarUsuario, EditarUsuario, EliminarUsuario, ExisteUsuario, BuscarUsuarios
from controladores.CRUDProveedor import ConsultarProveedores, AgregarProveedor, EditarProveedor, EliminarProveedor
from miscelaneos.misc import ListaATabla, CifrarContrasena

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= './static/img'

usuarios_bd = []
proveedores_bd = []

esta_registrado = False
usuario_registrado = None

def TraerUsuarios():
    global usuarios_bd
    usuarios_bd.clear()
    for usuario in ConsultarUsuarios():
        usuarios_bd.append(usuario)

def TraerProveedores():
    global proveedores_bd
    proveedores_bd.clear()
    for p in ConsultarProveedores():
        proveedores_bd.append(p)

@app.route('/', methods=['GET'])
def index():
    global esta_registrado, usuario_registrado
    esta_registrado = False
    usuario_registrado = None
    return render_template('index.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    global esta_registrado, usuario_registrado, usuarios_bd
    if request.method == 'POST':
        esta_registrado = False
        usuario_registrado = None
        id_usuario = request.form['user']
        password = request.form['password']
        if id_usuario == '' and password == '':
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
    if esta_registrado:
        return render_template('dashboard.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/usuarios/consultar', methods=['GET'])
def usuarios():
    global esta_registrado, usuarios_bd, usuario_registrado
    if esta_registrado:
        if usuarios_bd == []:
            TraerUsuarios()
        if usuario_registrado.rol.id != 0:
            return render_template('usuarios.html', usuarios=ListaATabla(usuarios_bd, 3), usuario_registrado=usuario_registrado)
        return redirect('/dashboard')
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
        if id_nuevo == '' or nombre_nuevo == '' or password_nuevo == '' or rol_nuevo == 'Seleccione' or password_nuevo != password_confirm:
            return redirect('/usuarios/agregar')
        if usuarios_bd == []:
            TraerUsuarios()
        id_nuevo = int(id_nuevo)
        rol_nuevo = int(rol_nuevo)
        if ExisteUsuario(id_nuevo):
            return redirect('/usuarios/agregar')
        imagen_usuario = request.files['imagen']
        if imagen_usuario.filename != '':
            ruta_guardar = os.path.join(app.config['UPLOAD_FOLDER']+'/Usuarios', str(id_nuevo)+'.jpg')
            imagen_usuario.save(ruta_guardar)
        AgregarUsuario(id_nuevo, nombre_nuevo, password_nuevo, rol_nuevo)
        TraerUsuarios()
        return redirect('/usuarios/consultar')
    if esta_registrado:
        if usuario_registrado.rol.id != 0:
            return render_template('usuariosAgregar.html', usuario_registrado=usuario_registrado)
        return redirect('/dashboard')
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
        if nombre_nuevo == '' or password_nuevo != password_confirm:
            return redirect('/usuarios/editar')
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
            return render_template('usuariosEditar.html', usuarios=usuarios_bd, usuario_registrado=usuario_registrado)
        return redirect('/dashboard')
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
                usuario_editar = BuscarUsuarios(id_usuario)[0]
                return render_template('usuariosEditarusuario.html', usuario=usuario_editar, usuario_registrado=usuario_registrado)
            return redirect('/usuarios/editar')
    return redirect('/')

@app.route('/usuarios/eliminar', methods=['GET','POST'])
def usuariosEliminar():
    global esta_registrado, usuarios_bd, usuario_registrado
    if request.method == 'POST':
        usuarios_eliminar = [u for u in request.form.values()]
        if len(usuarios_eliminar) == 0:
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
            return render_template('usuariosEliminar.html', usuarios=usuarios_bd, usuario_registrado=usuario_registrado)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/productos', methods=['GET'])
def productos():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('productos.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/productos/agregar', methods=['GET','POST'])
def productosAgregar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('productosAgregar.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/productos/editar', methods=['GET','PUT'])
def productosEditar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('productosEditar.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/productos/eliminar', methods=['GET','DELETE'])
def productosEliminar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('productosEliminar.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/proveedores', methods=['GET'])
def proveedores():
    global proveedores_bd, esta_registrado, usuario_registrado
    if esta_registrado:
        if proveedores_bd == []:
            TraerProveedores()
        return render_template('proveedores.html', usuario_registrado=usuario_registrado, proveedores = ListaATabla(proveedores_bd, 2))
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
        AgregarProveedor(Proveedor(id_nuevoprov, nombre_nuevoprov))
        TraerProveedores()
        return redirect('/proveedores')
    if esta_registrado:
        return render_template('proveedoresAgregar.html', usuario_registrado=usuario_registrado)
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
        TraerProveedores()
        return redirect('/proveedores')
    if esta_registrado:
        if proveedores_bd == []:
            TraerProveedores()
        return render_template('proveedoresEditar.html', usuario_registrado=usuario_registrado,Proveedores= proveedores_bd)
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
    return redirect('/')


@app.route('/proveedores/eliminar', methods=['GET','POST'])
def proveedoresEliminar():
    global proveedore_bd,esta_registrado, usuario_registrado
    if request.method == 'POST':
        for proveedor in [p for p in request.form.values()]:
            EliminarProveedor(proveedor)
        TraerProveedores()
        return redirect('/proveedores')
    if esta_registrado:
        if proveedores_bd ==[]:
            TraerProveedores()
        return render_template('proveedoresEliminar.html', usuario_registrado=usuario_registrado, proveedores = proveedores_bd)
    return redirect('/')

@app.route('/proveedor')
def proveedor():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('informacionProveedor.html', usuario_registrado=usuario_registrado)
    return redirect('/')
