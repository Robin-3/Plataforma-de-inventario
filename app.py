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

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')