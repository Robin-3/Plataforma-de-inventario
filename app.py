import os
from modelos.Usuario import Usuario
from flask import Flask, render_template, request, redirect
from controladores.CRUDRol import ObtenerRoles
from controladores.CRUDUsuario import ConsultarUsuarios, AgregarUsuario, EditarUsuario, EliminarUsuario
from miscelaneos.misc import ListaATabla, CifrarContrasena

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= './static/img'

usuarios_bd = []
ROLES = ObtenerRoles()

esta_registrado = False
usuario_registrado = None

def TraerUsuarios():
    global usuarios_bd
    usuarios_bd.clear()
    for u in ConsultarUsuarios():
        usuarios_bd.append(u)

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

@app.route('/usuarios', methods=['GET'])
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
    if request.method =="POST":
        id_nuevo = request.form['id']
        nombre_nuevo = request.form['nombre']
        password_nuevo = request.form['password']
        password_confirm = request.form['password2']
        rol_nuevo = request.form['rol']
        if (id_nuevo == '' or nombre_nuevo == '' or password_nuevo == '' or rol_nuevo == 'Seleccione') or password_nuevo != password_confirm:
            return redirect('/usuarios/agregar')
        if usuarios_bd == []:
            TraerUsuarios()
        id_nuevo = int(id_nuevo)
        rol_nuevo = int(rol_nuevo)
        if len([u for u in usuarios_bd if u.id == id_nuevo]) == 1:
            return redirect('/usuarios/agregar')
        imagen_usuario= request.files['imagen']
        if imagen_usuario.filename!="":
            ruta_guardar= os.path.join(app.config['UPLOAD_FOLDER']+'/Usuarios', str(id_nuevo)+'.jpg')
            imagen_usuario.save(ruta_guardar)
        AgregarUsuario(Usuario(id_nuevo, nombre_nuevo, password_nuevo), ROLES[rol_nuevo])
        TraerUsuarios()
        return redirect('/usuarios')
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
        EditarUsuario(id_nuevo, Usuario(id_nuevo, nombre_nuevo, password_nuevo), ROLES[rol_nuevo], cambiar_contrasena)
        imagen_usuario= request.files['imagen']
        if imagen_usuario.filename!="":
            ruta_guardar= os.path.join(app.config['UPLOAD_FOLDER']+'/Usuarios', str(id_nuevo)+'.jpg')
            imagen_usuario.save(ruta_guardar)
        TraerUsuarios()
        return redirect('/usuarios')
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
    if request.method == "POST":
        if esta_registrado:
            id_usuario = int(request.form['id'])
            if usuarios_bd == []:
                TraerUsuarios()
            usuario_editar = [u for u in usuarios_bd if u.id == id_usuario][0]
            return render_template('usuariosEditarusuario.html', usuario=usuario_editar, usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/usuarios/eliminar', methods=['GET','POST'])
def usuariosEliminar():
    global esta_registrado, usuarios_bd, usuario_registrado
    if request.method == 'POST':
        for usuario in [d for d in request.form.values()]:
            EliminarUsuario(usuario)
        TraerUsuarios()
        return redirect('/usuarios')
    if esta_registrado:
        if usuario_registrado.rol.id != 0:
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
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('proveedores.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/proveedores/agregar', methods=['GET','POST'])
def proveedoresAgregar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('proveedoresAgregar.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/proveedores/editar', methods=['GET','PUT'])
def proveedoresEditar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('proveedoresEditar.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/proveedores/eliminar', methods=['GET','DELETE'])
def proveedoresEliminar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('proveedoresEliminar.html', usuario_registrado=usuario_registrado)
    return redirect('/')
