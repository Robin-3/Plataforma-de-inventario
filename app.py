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

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')