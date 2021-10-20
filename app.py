from flask import Flask, render_template, request
from controladores.CRUDUsuario import ConsultarUsuarios
from miscelaneos.misc import ListaATabla

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/usuarios', methods=['GET'])
def usuarios():
    usuarios = []
    for u in ConsultarUsuarios():
        usuarios.append(eval(u.__repr__()))
    return render_template('usuarios.html', usuarios=ListaATabla(usuarios, 3))

@app.route('/usuarios/agregar', methods=['GET','POST'])
def usuariosAgregar():
    if request.method =="POST":
        return "Aquí se van a agregar los datos de un nuevo usuario"
    return render_template('usuariosAgregar.html')

@app.route('/usuarios/editar', methods=['GET','PUT'])
def usuariosEditar():
    if request.method == "PUT":
        return "Aquí se van a modificar los datos del usuario seleccionado"
    return render_template('usuariosEditar.html')

@app.route('/usuarios/eliminar', methods=['GET','DELETE'])
def usuariosEliminar():
    return render_template('usuariosEliminar.html')

@app.route('/productos', methods=['GET'])
def productos():
    return render_template('productos.html')

@app.route('/productos/agregar', methods=['GET','POST'])
def productosAgregar():
    return render_template('productosAgregar.html')

@app.route('/productos/editar', methods=['GET','PUT'])
def productosEditar():
    return render_template('productosEditar.html')

@app.route('/productos/eliminar', methods=['GET','DELETE'])
def productosEliminar():
    return render_template('productosEliminar.html')

@app.route('/proveedores', methods=['GET'])
def proveedores():
    return render_template('proveedores.html')

@app.route('/proveedores/agregar', methods=['GET','POST'])
def proveedoresAgregar():
    return render_template('proveedoresAgregar.html')

@app.route('/proveedores/editar', methods=['GET','PUT'])
def proveedoresEditar():
    return render_template('proveedoresEditar.html')

@app.route('/proveedores/eliminar', methods=['GET','DELETE'])
def proveedoresEliminar():
    return render_template('proveedoresEliminar.html')