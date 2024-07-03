from flask import render_template, request, redirect, url_for, session, flash
from app import app, dbSensores, users_collectionUsers
import mysql.connector
from pymongo import DESCENDING
from bson.objectid import ObjectId
import re

@app.route('/inicio/sensorTemHum', methods=['GET', 'POST'])
def sensorTemHum():
    if 'username' in session:
        if request.method == 'POST':
            usuario = session['username']
            print(usuario)
            valor = request.form['boton']
            lineas = valor.split('\r\n')
            resul = ""
            for linea in lineas:
                resul += linea

            # Consulta MongoDB
            ultima_lectura = dbSensores.TemperaturaHumedad.find_one(
                projection={'temperatura': True, 'humedad': True},
                sort=[('_id', DESCENDING)]
            )
            print(ultima_lectura)
            if ultima_lectura:
                temperatura = ultima_lectura.get('temperatura')
                humedad = ultima_lectura.get('humedad')
            else:
                temperatura = None
                humedad = None
            print(temperatura)
            print(humedad)

            # Conexion con MySQL
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pera11",
                database="AppFlask"
            )
            cursor = conexion.cursor()

            sql_select = "SELECT estado FROM motor WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            for estado in registros:
                print(estado)
            print(registros)

            sql_select = "SELECT salto, meta FROM calefaccion WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            saltoCalefaccion, metaCalefaccion = registros
            print(saltoCalefaccion)
            print(metaCalefaccion)
            if saltoCalefaccion == '-20.00' or metaCalefaccion == '50.00':
                saltoCalefaccion = 'nulo'
                metaCalefaccion = 'nulo'
            
            sql_select = "SELECT salto, meta FROM aire WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            saltoAire, metaAire = registros
            print(saltoAire)
            print(metaAire)
            if saltoAire == '50.00' or metaAire == '-20.00':
                saltoAire = 'nulo'
                metaAire = 'nulo'

            cursor.close()
            conexion.close()
            return render_template('sensorTemHum.html', title=resul, temperatura=temperatura, humedad=humedad, estado=estado, saltoCalefaccion=saltoCalefaccion, metaCalefaccion=metaCalefaccion, saltoAire=saltoAire, metaAire=metaAire)
    else:
        return redirect(url_for('login'))
    
    return render_template('sensorTemHum.html')

@app.route('/inicio/sensorAlarma', methods=['GET', 'POST'])
def sensorAlarma():
    if 'username' in session:
        if request.method == 'POST':
            usuario = session['username']
            print(usuario)
            valor = request.form['boton']
            lineas = valor.split('\r\n')
            resul = ""
            for linea in lineas:
                resul += linea
            
            # Conexion con MySQL
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pera11",
                database="AppFlask"
            )
            cursor = conexion.cursor()
            sql_select = "SELECT estado FROM alarma WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            for estado in registros:
                print(estado)
            print(registros)
            cursor.close()
            conexion.close()
            return render_template('sensorAlarma.html', title=resul, estado=estado)
    else:
        return redirect(url_for('login'))

    return render_template('sensorAlarma.html')

@app.route('/inicio/sensorLuzAutomatica', methods=['GET', 'POST'])
def sensorLuzAutomatica():
    if 'username' in session:
        if request.method == 'POST':
            usuario = session['username']
            print(usuario)
            valor = request.form['boton']
            lineas = valor.split('\r\n')
            resul = ""
            for linea in lineas:
                resul += linea
            
            # Consulta para obtener el último registro con id igual a 1
            ultima_lectura = dbSensores.Luminosidad.find_one(
                {'id': 1},
                projection={'lux': True},
                sort=[('_id', DESCENDING)]
            )

            print(ultima_lectura)
            if ultima_lectura:
                luz = ultima_lectura.get('lux')
            else:
                luz = None
            print(luz)

            # Conexion con MySQL
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pera11",
                database="AppFlask"
            )
            cursor = conexion.cursor()

            sql_select = "SELECT configuracion, estado, luminosidad FROM configLuz WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            configuracion, estado, luminosidad = registros
            
            cursor.close()
            conexion.close()

            return render_template('sensorLuzAutomatica.html', title=resul, luz=luz, configuracion=configuracion, estado=estado, luminosidad=luminosidad)
    else:
        return redirect(url_for('login'))
    
    return render_template('sensorLuzAutomatica.html')

@app.route('/inicio/sensorCO2', methods=['GET', 'POST'])
def sensorCO2():
    if 'username' in session:
        if request.method == 'POST':
            usuario = session['username']
            print(usuario)
            valor = request.form['boton']
            lineas = valor.split('\r\n')
            resul = ""
            for linea in lineas:
                resul += linea

            # Consulta MongoDB
            ultima_lectura = dbSensores.CO2.find_one(
                projection={'data': True},
                sort=[('_id', DESCENDING)]
            )
            print(ultima_lectura)
            if ultima_lectura:
                CO2 = ultima_lectura.get('data')
            else:
                CO2 = None
            print(CO2)

            # Conexion con MySQL
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pera11",
                database="AppFlask"
            )
            cursor = conexion.cursor()

            sql_select = "SELECT estado FROM motor WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            for estadoMotor in registros:
                print(estadoMotor)

            sql_select = "SELECT estado FROM servo WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            for estadoServo in registros:
                print(estadoServo)

            sql_select = "SELECT salto, meta FROM extractor WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            saltoExtractor, metaExtractor = registros
            print(saltoExtractor)
            print(metaExtractor)
            if saltoExtractor == '3000.00' or metaExtractor == '0.00':
                saltoExtractor = 'nulo'
                metaExtractor = 'nulo'
            
            sql_select = "SELECT salto, meta FROM ventana WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            saltoVentana, metaVentana = registros
            print(saltoVentana)
            print(metaVentana)
            if saltoVentana == '3000.00' or metaVentana == '0.00':
                saltoVentana = 'nulo'
                metaVentana = 'nulo'

            cursor.close()
            conexion.close()

            return render_template('sensorCO2.html', title=resul, CO2=CO2, estadoMotor=estadoMotor, estadoServo=estadoServo, saltoExtractor=saltoExtractor, metaExtractor=metaExtractor, saltoVentana=saltoVentana, metaVentana=metaVentana)
    else:
        return redirect(url_for('login'))
    
    return render_template('sensorCO2.html')

@app.route('/inicio/nuevoDispositivo', methods=['GET', 'POST'])
def nuevoDispositivo():
    if 'username' in session:
        if request.method == 'POST':
            usuario = session['username']
            print(usuario)

            # Consulta MongoDB
            user_data = users_collectionUsers.find_one({'username': session['username']})
            if user_data and 'sensores' in user_data:
                sensores = [sensor['descripcion'] for sensor in user_data['sensores'] if 'descripcion' in sensor]
            else:
                sensores = []
            print(sensores)
            newDevices = ['Luz automática 💡', 'Temperatura y \nHumedad 🌡', 'Alarma 🚨', 'Sensor de CO2 \n☁']
            for device in sensores:
                if device:
                    if device == 'Temperatura y \nHumedad 🌡':
                        newDevices.remove('Temperatura y \nHumedad 🌡')
                        print(newDevices)
                    elif device == 'Alarma 🚨':
                        newDevices.remove('Alarma 🚨')
                        print(newDevices)
                    elif device == 'Luz automática 💡':
                        newDevices.remove('Luz automática 💡')
                        print(newDevices)
                    elif device == 'Sensor de CO2 \n☁':
                        newDevices.remove('Sensor de CO2 \n☁')
                        print(newDevices)
            
            return render_template('nuevoDispositivo.html', devices=newDevices)
    else:
        return redirect(url_for('login'))
    
    return render_template('inicio.html')

@app.route('/inicio/nuevoTemHum', methods=['GET', 'POST'])
def nuevoTemHum():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    nuevo_sensor = {
        "tipo": "TemHum",
        "descripcion": "Temperatura y \nHumedad 🌡",
        "id": [1]
    }
    actualizacion = {'$push': {'sensores': nuevo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El nuevo sensor fue añadido exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/nuevoAlarma', methods=['GET', 'POST'])
def nuevoAlarma():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    nuevo_sensor = {
        "tipo": "Movimiento",
        "descripcion": "Alarma 🚨",
        "id": [1]
    }
    actualizacion = {'$push': {'sensores': nuevo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El nuevo sensor fue añadido exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/nuevoLuzAutomatica', methods=['GET', 'POST'])
def nuevoLuzAutomatica():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    nuevo_sensor = {
        "tipo": "Luz",
        "descripcion": "Luz automática 💡",
        "id": [1]
    }
    actualizacion = {'$push': {'sensores': nuevo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El nuevo sensor fue añadido exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/nuevoCO2', methods=['GET', 'POST'])
def nuevoCO2():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    nuevo_sensor = {
        "tipo": "CO2",
        "descripcion": "Sensor de CO2 \n☁",
        "id": [1]
    }
    actualizacion = {'$push': {'sensores': nuevo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El nuevo sensor fue añadido exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/borrarDispositivo', methods=['GET', 'POST'])
def borrarDispositivo():
    if 'username' in session:
        if request.method == 'POST':
            usuario = session['username']
            print(usuario)

            # Consulta MongoDB
            user_data = users_collectionUsers.find_one({'username': session['username']})
            if user_data and 'sensores' in user_data:
                sensores = [sensor['descripcion'] for sensor in user_data['sensores'] if 'descripcion' in sensor]
            else:
                sensores = []
            
            return render_template('borrarDispositivo.html', devices=sensores)
    else:
        return redirect(url_for('login'))
    
    return render_template('inicio.html')

@app.route('/inicio/borrarTemHum', methods=['GET', 'POST'])
def borrarTemHum():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    viejo_sensor = {
        "tipo": "TemHum",
        "descripcion": "Temperatura y \nHumedad 🌡",
        "id": [1]
    }
    actualizacion = {'$pull': {'sensores': viejo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El viejo sensor fue eliminado exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/borrarAlarma', methods=['GET', 'POST'])
def borrarAlarma():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    viejo_sensor = {
        "tipo": "Movimiento",
        "descripcion": "Alarma 🚨",
        "id": [1]
    }
    actualizacion = {'$pull': {'sensores': viejo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El viejo sensor fue eliminado exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/borrarLuzAutomatica', methods=['GET', 'POST'])
def borrarLuzAutomatica():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    viejo_sensor = {
        "tipo": "Luz",
        "descripcion": "Luz automática 💡",
        "id": [1]
    }
    actualizacion = {'$pull': {'sensores': viejo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El viejo sensor fue eliminado exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/borrarCO2', methods=['GET', 'POST'])
def borrarCO2():
    usuario = session['username']
    print(usuario)

    user_data = users_collectionUsers.find_one({'username': session['username']})
    if user_data:
        user_id = user_data['_id']
    else:
        print("Usuario no encontrado")
    
    filtro = {'_id': ObjectId(user_id)}
    viejo_sensor = {
        "tipo": "CO2",
        "descripcion": "Sensor de CO2 \n☁",
        "id": [1]
    }
    actualizacion = {'$pull': {'sensores': viejo_sensor}}

    resultado = users_collectionUsers.update_one(filtro, actualizacion)

    if resultado.modified_count > 0:
        print("El viejo sensor fue eliminado exitosamente.")
    else:
        print("No se encontró el documento o no se pudo actualizar.")
    
    return redirect(url_for('inicio'))

@app.route('/inicio/perfil', methods=['GET', 'POST'])
def perfil():
    if 'username' in session:
        usuario = session['username']
        user_data = users_collectionUsers.find_one({"username": usuario})
        email = user_data['mail']
        telefono = user_data['phone']
        return render_template('perfil.html', email=email, telefono=telefono)
    else:
        return redirect(url_for('login'))
    
@app.route('/inicio/perfil/cambiar', methods=['GET', 'POST'])
def cambiar():
    zentorno = 'true'
    return render_template('changePassword.html', zentorno=zentorno)

@app.route('/inicio/perfil/guardarDatos', methods=['POST'])
def guardarDatos():

    if 'username' in session:
        usuario = session['username']
        user_data = users_collectionUsers.find_one({"username": usuario})
        email = user_data['mail']
        telefono = user_data['phone']
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


        nuevoMail = request.form.get('email')
        nuevoTelefono = request.form.get('telefono')
        if email != nuevoMail and re.match(patron, nuevoMail):
            update = users_collectionUsers.update_one(
                {'username' : usuario},
                {'$set' : {'mail' : nuevoMail}}
            )
            if update.matched_count > 0:
                flash("Correo actualizado.")
                if telefono != nuevoTelefono:
                    update = users_collectionUsers.update_one(
                        {'username' : usuario},
                        {'$set' : {'phone' : nuevoTelefono}}
                    )
                    if update.matched_count > 0:
                        flash("Correo y Teléfono actualizados.")
                        return redirect(url_for('perfil'))
                else:
                    return redirect(url_for('perfil'))
            else:
                flash(f"No se encontró ningún usuario con el nombre: {usuario}")
                return redirect(url_for('perfil'))
        
        if telefono != nuevoTelefono:
            update = users_collectionUsers.update_one(
                {'username' : usuario},
                {'$set' : {'phone' : nuevoTelefono}}
            )
            if update.matched_count > 0:
                flash("Teléfono actualizado.")
                return redirect(url_for('perfil'))
            else:
                flash(f"No se encontró ningún usuario con el nombre: {usuario}")
                return redirect(url_for('perfil'))

        return redirect(url_for('perfil'))
    else:
        return redirect(url_for('login'))

