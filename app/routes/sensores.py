from flask import render_template, request
from app import app, dbSensores, dbEstados
import subprocess
from pymongo import DESCENDING
import mysql.connector
from datetime import datetime
import json

#-------------------------------------------------------------
#                   ALARMA
#-------------------------------------------------------------
@app.route('/inicio/sensorAlarma/conectar', methods=['POST'])
def conectar():
    topic = 'alarma/conexion'
    valor = 'conectar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)
    
    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Alarma\", \"estado\": \"Conectada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoAlarma
    collection.insert_one(mensaje_dict)
    title = 'Alarma 🚨'
    estado = 'Conectada'
    return render_template('sensorAlarma.html', title=title, estado=estado)

@app.route('/inicio/sensorAlarma/desconectar', methods=['POST'])
def desconectar():
    topic = 'alarma/conexion'
    valor = 'desconectar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)
    
    ahora = datetime.now()
    mensaje_json = "{\"estado\": \"Desconectada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoAlarma
    collection.insert_one(mensaje_dict)
    title = 'Alarma 🚨'
    estado = 'Desconectada'
    return render_template('sensorAlarma.html', title=title, estado=estado)

#-------------------------------------------------------------
#                   CO2
#-------------------------------------------------------------
@app.route('/inicio/sensorCO2/activarMotorCO2', methods=['POST'])
def activarMotorCO2():
    topic = 'motor/activacion'
    valor = 'activar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Extractor\", \"estado\": \"Activado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoCO2
    collection.insert_one(mensaje_dict)

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
    title = 'Sensor de CO2 ☁'
    estadoMotor = 'Activado'
    # Conexion con MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pera11",
        database="AppFlask"
    )
    cursor = conexion.cursor()
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
    return render_template('sensorCO2.html', title=title, CO2=CO2, estadoMotor=estadoMotor, estadoServo=estadoServo, saltoExtractor=saltoExtractor, metaExtractor=metaExtractor, saltoVentana=saltoVentana, metaVentana=metaVentana)
    
@app.route('/inicio/sensorCO2/desactivarMotorCO2', methods=['POST'])
def desactivarMotorCO2():
    topic = 'motor/activacion'
    valor = 'desactivar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Extractor\", \"estado\": \"Desactivado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoCO2
    collection.insert_one(mensaje_dict)

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
    title = 'Sensor de CO2 ☁'
    estadoMotor = 'Desactivado'
    # Conexion con MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pera11",
        database="AppFlask"
    )
    cursor = conexion.cursor()
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
    return render_template('sensorCO2.html', title=title, CO2=CO2, estadoMotor=estadoMotor, estadoServo=estadoServo, saltoExtractor=saltoExtractor, metaExtractor=metaExtractor, saltoVentana=saltoVentana, metaVentana=metaVentana)

@app.route('/inicio/sensorCO2/activarServoCO2', methods=['POST'])
def activarServoCO2():
    topic = 'servo/activacion'
    valor = 'activar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Ventana\", \"estado\": \"Abierta\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoCO2
    collection.insert_one(mensaje_dict)

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
    title = 'Sensor de CO2 ☁'
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

    estadoServo = 'Abierta'
    return render_template('sensorCO2.html', title=title, CO2=CO2, estadoMotor=estadoMotor, estadoServo=estadoServo, saltoExtractor=saltoExtractor, metaExtractor=metaExtractor, saltoVentana=saltoVentana, metaVentana=metaVentana)

@app.route('/inicio/sensorCO2/desactivarServoCO2', methods=['POST'])
def desactivarServoCO2():
    topic = 'servo/activacion'
    valor = 'desactivar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Ventana\", \"estado\": \"Cerrada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoCO2
    collection.insert_one(mensaje_dict)

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

    title = 'Sensor de CO2 ☁'
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

    estadoServo = 'Cerrada'
    return render_template('sensorCO2.html', title=title, CO2=CO2, estadoMotor=estadoMotor, estadoServo=estadoServo, saltoExtractor=saltoExtractor, metaExtractor=metaExtractor, saltoVentana=saltoVentana, metaVentana=metaVentana)

@app.route('/inicio/sensorCO2/configurarExtractor', methods=['POST'])
def configurarExtractor():
    saltoExtractor = str(request.form['input1'])
    metaExtractor = str(request.form['input2'])

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
    title = 'Sensor de CO2 ☁'

    # Conexion con MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pera11",
        database="AppFlask"
    )
    cursor = conexion.cursor()

    id_usuario = 1
    sql_update = "UPDATE extractor SET salto = %s, meta = %s WHERE id = %s"
    mensaje_dict = (saltoExtractor, metaExtractor, id_usuario)
    cursor.execute(sql_update, mensaje_dict)
    conexion.commit()

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

    sql_select = "SELECT salto, meta FROM ventana WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    saltoVentana, metaVentana = registros
    print(saltoVentana)
    print(metaVentana)
    if saltoVentana == '3000.00' or metaVentana == '0.00':
        saltoVentana = 'nulo'
        metaVentana = 'nulo'
    
    if saltoExtractor == '3000.00' or metaExtractor == '0.00':
        saltoExtractor = 'nulo'
        metaExtractor = 'nulo'

    cursor.close()
    conexion.close()

    return render_template('sensorCO2.html', title=title, CO2=CO2, estadoMotor=estadoMotor, estadoServo=estadoServo, saltoExtractor=saltoExtractor, metaExtractor=metaExtractor, saltoVentana=saltoVentana, metaVentana=metaVentana)

@app.route('/inicio/sensorCO2/configurarVentana', methods=['POST'])
def configurarVentana():
    saltoVentana = str(request.form['input3'])
    metaVentana = str(request.form['input4'])

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
    title = 'Sensor de CO2 ☁'
    
    # Conexion con MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pera11",
        database="AppFlask"
    )
    cursor = conexion.cursor()

    id_usuario = 1
    sql_update = "UPDATE ventana SET salto = %s, meta = %s WHERE id = %s"
    mensaje_dict = (saltoVentana, metaVentana, id_usuario)
    cursor.execute(sql_update, mensaje_dict)
    conexion.commit()

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
    
    if saltoVentana == '3000.00' or metaVentana == '0.00':
        saltoVentana = 'nulo'
        metaVentana = 'nulo'

    cursor.close()
    conexion.close()

    return render_template('sensorCO2.html', title=title, CO2=CO2, estadoMotor=estadoMotor, estadoServo=estadoServo, saltoExtractor=saltoExtractor, metaExtractor=metaExtractor, saltoVentana=saltoVentana, metaVentana=metaVentana)

#-------------------------------------------------------------
#                   TEMPERATURA HUMEDAD
#-------------------------------------------------------------
@app.route('/inicio/sensorTemHum/activarCalefaccion', methods=['POST'])
def activarCalefaccion():
    topic = 'motor/activacion'
    valor = 'activar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Calefaccion\", \"estado\": \"Activada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoTemHum
    collection.insert_one(mensaje_dict)

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

    title = 'Temperatura y Humedad 🌡'
    estado = 'Activada'
    return render_template('sensorTemHum.html', title=title, temperatura=temperatura, humedad=humedad, estado=estado, saltoCalefaccion=saltoCalefaccion, metaCalefaccion=metaCalefaccion, saltoAire=saltoAire, metaAire=metaAire)
    
@app.route('/inicio/sensorTemHum/desactivarCalefaccion', methods=['POST'])
def desactivarCalefaccion():
    topic = 'motor/activacion'
    valor = 'desactivar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Calefaccion\", \"estado\": \"Desactivada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoTemHum
    collection.insert_one(mensaje_dict)

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

    title = 'Temperatura y Humedad 🌡'
    estado = 'Desactivada'
    return render_template('sensorTemHum.html', title=title, temperatura=temperatura, humedad=humedad, estado=estado, saltoCalefaccion=saltoCalefaccion, metaCalefaccion=metaCalefaccion, saltoAire=saltoAire, metaAire=metaAire)

@app.route('/inicio/sensorTemHum/activarAire', methods=['POST'])
def activarAire():
    topic = 'motor/activacion'
    valor = 'activar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Aire\", \"estado\": \"Activado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoTemHum
    collection.insert_one(mensaje_dict)

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

    title = 'Temperatura y Humedad 🌡'
    estado = 'Activado'
    return render_template('sensorTemHum.html', title=title, temperatura=temperatura, humedad=humedad, estado=estado, saltoCalefaccion=saltoCalefaccion, metaCalefaccion=metaCalefaccion, saltoAire=saltoAire, metaAire=metaAire)

@app.route('/inicio/sensorTemHum/desactivarAire', methods=['POST'])
def desactivarAire():
    topic = 'motor/activacion'
    valor = 'desactivar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Aire\", \"estado\": \"Desactivado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoTemHum
    collection.insert_one(mensaje_dict)

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

    title = 'Temperatura y Humedad 🌡'
    estado = 'Desactivado'
    return render_template('sensorTemHum.html', title=title, temperatura=temperatura, humedad=humedad, estado=estado, saltoCalefaccion=saltoCalefaccion, metaCalefaccion=metaCalefaccion, saltoAire=saltoAire, metaAire=metaAire)

@app.route('/inicio/sensorTemHum/configurarCalefaccion', methods=['POST'])
def configurarCalefaccion():
    saltoCalefaccion = str(request.form['input1'])
    metaCalefaccion = str(request.form['input2'])

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

    title = 'Temperatura y Humedad 🌡'

    # Conexion con MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pera11",
        database="AppFlask"
    )
    cursor = conexion.cursor()

    id_usuario = 1
    sql_update = "UPDATE calefaccion SET salto = %s, meta = %s WHERE id = %s"
    mensaje_dict = (saltoCalefaccion, metaCalefaccion, id_usuario)
    cursor.execute(sql_update, mensaje_dict)
    conexion.commit()

    sql_select = "SELECT estado FROM motor WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    for estado in registros:
        print(estado)
    print(registros)

    sql_select = "SELECT salto, meta FROM aire WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    saltoAire, metaAire = registros
    print(saltoAire)
    print(metaAire)
    if saltoAire == '50.00' or metaAire == '-20.00':
        saltoAire = 'nulo'
        metaAire = 'nulo'
    
    if saltoCalefaccion == '-20.00' or metaCalefaccion == '50.00':
        saltoCalefaccion = 'nulo'
        metaCalefaccion = 'nulo'

    cursor.close()
    conexion.close()

    return render_template('sensorTemHum.html', title=title, temperatura=temperatura, humedad=humedad, estado=estado, saltoCalefaccion=saltoCalefaccion, metaCalefaccion=metaCalefaccion, saltoAire=saltoAire, metaAire=metaAire)

@app.route('/inicio/sensorTemHum/configurarAire', methods=['POST'])
def configurarAire():
    saltoAire = str(request.form['input3'])
    metaAire = str(request.form['input4'])

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

    title = 'Temperatura y Humedad 🌡'

    # Conexion con MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pera11",
        database="AppFlask"
    )
    cursor = conexion.cursor()

    id_usuario = 1
    sql_update = "UPDATE aire SET salto = %s, meta = %s WHERE id = %s"
    mensaje_dict = (saltoAire, metaAire, id_usuario)
    cursor.execute(sql_update, mensaje_dict)
    conexion.commit()

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
    
    if saltoAire == '50.00' or metaAire == '-20.00':
        saltoAire = 'nulo'
        metaAire = 'nulo'

    cursor.close()
    conexion.close()
    
    return render_template('sensorTemHum.html', title=title, temperatura=temperatura, humedad=humedad, estado=estado, saltoCalefaccion=saltoCalefaccion, metaCalefaccion=metaCalefaccion, saltoAire=saltoAire, metaAire=metaAire)

#-------------------------------------------------------------
#                   LUZ AUTOMATICA
#-------------------------------------------------------------
@app.route('/inicio/sensorLuzAutomatica/manual', methods=['POST'])
def manual():

    # Consulta MongoDB
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

    sql_update = "UPDATE configLuz SET configuracion='Manual' WHERE id = 1"
    cursor.execute(sql_update)
    conexion.commit()

    sql_select = "SELECT configuracion, estado FROM configLuz WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    configuracion, estado = registros

    cursor.close()
    conexion.close()

    title = 'Luz automática 💡'
    return render_template('sensorLuzAutomatica.html', title=title, luz=luz, configuracion=configuracion, estado=estado)

@app.route('/inicio/sensorLuzAutomatica/automatica', methods=['POST'])
def automatica():

    # Consulta MongoDB
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

    sql_update = "UPDATE configLuz SET configuracion='Automática' WHERE id = 1"
    cursor.execute(sql_update)
    conexion.commit()

    sql_select = "SELECT configuracion, estado, luminosidad FROM configLuz WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    configuracion, estado, luminosidad = registros

    cursor.close()
    conexion.close()

    title = 'Luz automática 💡'
    return render_template('sensorLuzAutomatica.html', title=title, luz=luz, configuracion=configuracion, estado=estado, luminosidad=luminosidad)

@app.route('/inicio/sensorLuzAutomatica/encender', methods=['POST'])
def encender():
    topic = 'luz/led'
    valor = 'encender'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Luz\", \"estado\": \"Encendida\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoLuz
    collection.insert_one(mensaje_dict)

    # Consulta MongoDB
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

    sql_update = "UPDATE configLuz SET estado='Encendida' WHERE id = 1"
    cursor.execute(sql_update)
    conexion.commit()

    sql_select = "SELECT configuracion, estado FROM configLuz WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    configuracion, estado = registros

    cursor.close()
    conexion.close()

    title = 'Luz automática 💡'
    return render_template('sensorLuzAutomatica.html', title=title, luz=luz, configuracion=configuracion, estado=estado)

@app.route('/inicio/sensorLuzAutomatica/apagar', methods=['POST'])
def apagar():
    topic = 'luz/led'
    valor = 'apagar'
    subprocess.run(['python', 'broker/enviar.py', topic, valor], capture_output=True, text=True)

    ahora = datetime.now()
    mensaje_json = "{\"nombre\":\"Luz\", \"estado\": \"Apagada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
    mensaje_dict = json.loads(mensaje_json)
    collection = dbEstados.dispositivoLuz
    collection.insert_one(mensaje_dict)

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

    sql_update = "UPDATE configLuz SET estado='Apagada' WHERE id = 1"
    cursor.execute(sql_update)
    conexion.commit()

    sql_select = "SELECT configuracion, estado FROM configLuz WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    configuracion, estado = registros

    cursor.close()
    conexion.close()

    title = 'Luz automática 💡'
    return render_template('sensorLuzAutomatica.html', title=title, luz=luz, configuracion=configuracion, estado=estado)

@app.route('/inicio/sensorLuzAutomatica/configurarLuz', methods=['POST'])
def configurarLuz():
    
    luminoso = str(request.form['input1'])
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

    id_usuario = 1
    sql_update = "UPDATE configLuz SET luminosidad = %s WHERE id = %s" 
    mensaje_dict = (luminoso, id_usuario)
    cursor.execute(sql_update, mensaje_dict)
    conexion.commit()

    sql_select = "SELECT configuracion, estado, luminosidad FROM configLuz WHERE id = 1"
    cursor.execute(sql_select)
    registros = cursor.fetchone()
    configuracion, estado, luminosidad = registros

    cursor.close()
    conexion.close()

    title = 'Luz automática 💡'
    return render_template('sensorLuzAutomatica.html', title=title, luz=luz, configuracion=configuracion, estado=estado, luminosidad=luminosidad)

