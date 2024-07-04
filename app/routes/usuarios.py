from flask import render_template, redirect, url_for, session, flash, request
from itsdangerous import URLSafeTimedSerializer
from app import app, users_collectionUsers
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flasgger import swag_from
from swagger_conf import sc_index, sc_register, sc_login, sc_inicio, sc_logout, sc_forgotPassword, sc_changePassword, sc_changePasswordMail

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/')
@swag_from(sc_index)
def home(): 
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@swag_from(sc_register)
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        mail = request.form['mail']
        phone = request.form['phone']

        # Verificar si el usuario ya existe en la base de datos
        existing_user = users_collectionUsers.find_one({"username": username})
        if existing_user:
            flash('Usuario ya registrado. Por favor, pruebe con otro nombre.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Contraseña y Confirmar contraseña no coinciden.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        
        user = {
            "username": username,
            "password": hashed_password,
            "mail": mail,
            "phone": phone,
            "date": datetime.now()
        }
        
        users_collectionUsers.insert_one(user)
        flash('Usuario registrado correctamente!')
        session['username'] = username
        return redirect(url_for('inicio'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@swag_from(sc_login)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collectionUsers.find_one({"username": username})

        if user:
            if check_password_hash(user['password'], password):
                session['username'] = username
                flash('Sesión iniciada correctamente!')
                return redirect(url_for('inicio'))
            else:
                flash('Usuario o contraseña incorrecto', 'error')
                return redirect(url_for('login'))
        else:
            flash('Usuario no registrado', 'error')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/inicio')
@swag_from(sc_inicio)
def inicio():
    if 'username' in session:
        inicio = 'inicio'
        user_data = users_collectionUsers.find_one({'username': session['username']})
        if user_data and 'sensores' in user_data:
            sensores = [sensor['descripcion'] for sensor in user_data['sensores'] if 'descripcion' in sensor]
        else:
            sensores = []

        return render_template('inicio.html', devices=sensores, inicio=inicio)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
@swag_from(sc_logout)
def logout():
    session.pop('username', None)
    flash('Sesión cerrada correctamente!')
    return redirect(url_for('login'))

@app.route('/forgotPassword', methods=['GET', 'POST'])
@swag_from(sc_forgotPassword)
def forgotPassword():
    if request.method == 'POST':
        sender_email = "pabloperamatobenito@gmail.com"
        receiver_email = request.form['mail']
        password = "hxpb dweo uhei klxl"
        username = request.form['username']
        
        subject = "Recuperar contraseña"
        
        # Genera un token con el nombre de usuario
        token = serializer.dumps(username, salt='password-reset-salt')
        
        body = f"""
        <html>
        <body>
        <p>Hola {username},</p>
        <p>Para recuperar su cuenta, haga clic en el siguiente <a href="http://localhost:5000/changePasswordMail?token={token}">enlace</a>.</p>
        <p>Un saludo.<br>Soporte de EasyHome.</p>
        </body>
        </html>
        """

        user_data = users_collectionUsers.find_one({"username": username})

        if not user_data:
            flash('Usuario no registrado.', 'error')
            return redirect(url_for('forgotPassword'))
        elif user_data['mail'] != receiver_email:
            flash('Correo electrónico introducido no coincidente con el registrado por el usuario.', 'error')
            return redirect(url_for('forgotPassword'))
        else:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "html"))

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                flash("Correo electrónico enviado. Por favor, revise su bandeja de entrada.")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Error al enviar el correo: {e}', 'error')
                return redirect(url_for('forgotPassword'))
    
    return render_template('forgotPassword.html')

@app.route('/changePassword', methods=['GET', 'POST'])
@swag_from(sc_changePassword)
def changePassword():
    if 'username' in session:
        if request.method == 'POST':
            username = session['username']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if new_password != confirm_password:
                flash('Contraseña y Confirmar nueva contraseña no coinciden.', 'error')
                return redirect(url_for('changePassword'))

            hashed_password = generate_password_hash(new_password)

            update = users_collectionUsers.update_one(
                {'username' : username},
                {'$set' : {'password' : hashed_password}}
            )

            if update.matched_count > 0:
                flash("Contraseña actualizada correctamente.")
                session.pop('username', None)
                return redirect(url_for('login'))
            else:
                flash(f"No se encontró ningún usuario con el nombre: {username}")
                return redirect(url_for('perfil'))
        
        return render_template('changePassword.html')
    else:
        return redirect(url_for('login'))

@app.route('/changePasswordMail', methods=['GET', 'POST'])
@swag_from(sc_changePasswordMail)
def changePasswordMail():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        username = request.form['username']

        if new_password != confirm_password:
            flash('Contraseña y Confirmar nueva contraseña no coinciden.', 'error')
            return redirect(url_for('changePasswordMail'))

        hashed_password = generate_password_hash(new_password)

        update = users_collectionUsers.update_one(
            {'username' : username},
            {'$set' : {'password' : hashed_password}}
        )

        if update.matched_count > 0:
            flash("Contraseña actualizada correctamente.")
            return redirect(url_for('login'))
        else:
            flash(f"No se encontró ningún usuario con el nombre: {username}")
            return redirect(url_for('changePasswordMail'))
    
    token = request.args.get('token')
    try:
        # Valida el token y obtiene el nombre de usuario
        username = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token válido por 1 hora
    except Exception as e:
        flash('Token no válido o ha expirado.', 'error')
        return redirect(url_for('forgotPassword'))

    return render_template('changePasswordMail.html', username=username)
