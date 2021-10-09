from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/usuariosAgregar')
def usuariosAgregar():
    return render_template('usuariosAgregar.html')

@app.route('/usuariosEditar')
def usuariosEditar():
    return render_template('usuariosEditar.html')

@app.route('/usuariosEliminar')
def usuariosEliminar():
    return render_template('usuariosEliminar.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/productosAgregar')
def productosAgregar():
    return render_template('productosAgregar.html')

@app.route('/productosEditar')
def productosEditar():
    return render_template('productosEditar.html')

@app.route('/productosEliminar')
def productosEliminar():
    return render_template('productosEliminar.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

@app.route('/proveedoresAgregar')
def proveedoresAgregar():
    return render_template('proveedoresAgregar.html')

@app.route('/proveedoresEditar')
def proveedoresEditar():
    return render_template('proveedoresEditar.html')

@app.route('/proveedoresEliminar')
def proveedoresEliminar():
    return render_template('proveedoresEliminar.html')