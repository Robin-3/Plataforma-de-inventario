from flask import Flask, render_template, request, redirect
from controladores.CRUDUsuario import ConsultarUsuarios
from miscelaneos.misc import ListaATabla, CifrarContrasena

app = Flask(__name__)
usuarios_bd = []

esta_registrado = False
usuario_registrado = None

def TraerUsuarios():
    global usuarios_bd
    usuarios_bd.clear()
    for u in ConsultarUsuarios():
        usuarios_bd.append(u)

@app.route('/', methods=['GET'])
def index():
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
        return render_template('usuarios.html', usuarios=ListaATabla(usuarios_bd, 3), usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/usuarios/agregar', methods=['GET','POST'])
def usuariosAgregar():
    global esta_registrado, usuario_registrado
    if request.method =="POST":
        return "Aquí se van a agregar los datos de un nuevo usuario"
    if esta_registrado:
        return render_template('usuariosAgregar.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/usuarios/editar', methods=['GET','PUT'])
def usuariosEditar():
    global esta_registrado, usuario_registrado
    usuarios = []
    for u in ConsultarUsuarios():
        usuarios.append(eval(u.__repr__()))
    if esta_registrado:
        return render_template('usuariosEditar.html', usuarios=ListaATabla(usuarios, 3), usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/usuarios/editarusuario', methods=['GET','PUT'])
def usuariosEditarusuario():
    global esta_registrado, usuario_registrado
    if request.method == "PUT":
        return "Aquí se van a modificar los datos del usuario seleccionado"
    if esta_registrado:
        return render_template('usuariosEditarusuario.html', usuario_registrado=usuario_registrado)
    return redirect('/')

@app.route('/usuarios/eliminar', methods=['GET','DELETE'])
def usuariosEliminar():
    global esta_registrado, usuario_registrado
    if esta_registrado:
        return render_template('usuariosEliminar.html', usuario_registrado=usuario_registrado)
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
