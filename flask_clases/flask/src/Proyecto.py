from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
import re
from flask_sqlalchemy import SQLAlchemy
from Models.entities.Usuarios import usuarios
from Models.ModelUsuarios import modeluser

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template("Home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        usuario = usuarios(None, None, email, contraseña)
        logged_user = modeluser.login(db, usuario)
        
        if logged_user:
            return redirect(url_for('home'))
        else:
            return render_template("auth/login.html", error="Email o contraseña incorrectos.")
    return render_template("auth/login.html")

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']

        # Verificar si la cédula ya existe en la base de datos
        usuario_existente = modeluser.buscar_usuario_por_cedula(db, cedula)
        
        if usuario_existente:
            # Si la cédula ya existe, mostrar un mensaje de error
            return render_template("Registro.html", error="La cédula ya está registrada.")

        # Si no existe, proceder a registrar el nuevo usuario
        nuevo_usuario = usuarios(cedula, nombre, email, contraseña)
        modeluser.registrar(db, nuevo_usuario)
        return redirect(url_for('login'))

    return render_template("Registro.html")




@app.route('/actualizar', methods=['GET', 'POST'])
def Cambiar_Contraseña():
    if request.method == 'POST':
        cedula = request.form['cedula']  # Obtener la cédula del formulario
        nueva_contraseña = request.form['contraseña']  # Obtener la nueva contraseña del formulario

        # Busca al usuario por cédula
        usuario = modeluser.buscar_usuario_por_cedula(db, cedula)
        if usuario is None:
            return render_template("actualizar.html", error="No se encontró un usuario con esa cédula.")

        # Actualiza la contraseña
        usuario.contraseña = nueva_contraseña
        db.session.commit()  # Guarda los cambios en la base de datos

        return redirect(url_for('login'))  
    return render_template("actualizar.html")  

 

@app.route('/actualizarInfo', methods=['GET', 'POST'])
def actualizar_informacion():
    if request.method == 'POST':
        cedula = request.form['cedula']
        email = request.form['email']
        nueva_contraseña = request.form['nueva_contraseña']
        
        # Validar que la nueva contraseña cumple los requisitos
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', nueva_contraseña):
            flash("La contraseña debe tener al menos 8 caracteres y contener letras y números", "error")
            return redirect(url_for('actualizar_informacion'))

        # Buscar usuario por cédula
        usuario = modeluser.buscar_usuario_por_cedula(db, cedula)
        if usuario is None:
            flash("No se encontró un usuario con esa cédula.", "error")
            return redirect(url_for('actualizar_informacion'))

        # Actualizar el email y la contraseña del usuario
        usuario.email = email
        usuario.contraseña = nueva_contraseña
        
        try:
            # Guardar los cambios en la base de datos
            db.session.commit()
            flash("Cambio de email y contraseña exitoso, ingresa con tus datos", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Si hay un error, revertir cambios
            flash("Error al actualizar los datos: " + str(e), "error")
            return redirect(url_for('actualizar_informacion'))
    
    return render_template("actualizarInfo.html")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
