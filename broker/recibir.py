import paho.mqtt.client as mqtt
from pymongo import MongoClient
import socket
import json
from datetime import datetime
import mysql.connector
import subprocess
import os

# Configuración del broker MQTT
mqtt_server = socket.gethostbyname(socket.gethostname())
mqtt_topic_sensores = "sensor/datos"
mqtt_topic_alarma = "alarma/conexion"
mqtt_topic_motor = "motor/activacion"
mqtt_topic_servo = "servo/activacion"

# Configurar MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client.Sensores
dbEstados = client.Estados

# Función de callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con código de resultado {rc}")
    client.subscribe(mqtt_topic_sensores)
    client.subscribe(mqtt_topic_alarma)
    client.subscribe(mqtt_topic_motor)
    client.subscribe(mqtt_topic_servo)

# Función de callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    # Conexion con MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pera11",
        database="AppFlask"
    )
    cursor = conexion.cursor()
    enviar_path = os.path.join(os.path.dirname(__file__), 'enviar.py')

    print(f"Topic {msg.topic}: {str(msg.payload.decode())}")
    if msg.topic == mqtt_topic_sensores:
        ahora = datetime.now()
        fechaHora = "\"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
        mensaje_json = str(msg.payload.decode()) + fechaHora
        mensaje_dict = json.loads(mensaje_json)
        if (mensaje_dict['Sensor'] == "TemHum"):
            collection = db.TemperaturaHumedad
            collection.insert_one(mensaje_dict)

            #CONFIGURACION AUTOMATICA DE CALEFACCION Y AIRE ACONDICIONADO
            #------------------------------------------------------------------------------------------------------
            sql_select = "SELECT estado FROM motor WHERE id = 1"
            cursor.execute(sql_select)
            resultado = cursor.fetchone()
            for estado in resultado:
                print(estado)

            partes = str(msg.payload.decode()).split(',')
            temporal = partes[1].strip()
            subpartes = temporal.split(':')
            temperatura = subpartes[1].strip()
            
            #-------CALEFACCION-----------
            sql_select = "SELECT salto, meta FROM calefaccion WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            salto, meta = registros

            if estado == 'Activado':
                if float(temperatura) >= float(meta) and meta != '50.00':
                    topico = 'motor/activacion'
                    valor = 'desactivar'
                    subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)

                    mensaje_json = "{\"nombre\":\"Calefaccion\", \"estado\": \"Desactivada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
                    mensaje_dict = json.loads(mensaje_json)
                    collection = dbEstados.dispositivoTemHum
                    collection.insert_one(mensaje_dict)
            elif estado == 'Desactivado':
                if float(temperatura) <= float(salto) and salto != '-20.00':
                    topico = 'motor/activacion'
                    valor = 'activar'
                    subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)

                    mensaje_json = "{\"nombre\":\"Calefaccion\", \"estado\": \"Activada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
                    mensaje_dict = json.loads(mensaje_json)
                    collection = dbEstados.dispositivoTemHum
                    collection.insert_one(mensaje_dict)

            #-------AIRE ACONDICIONADO-----------
            # sql_select = "SELECT salto, meta FROM aire WHERE id = 1"
            # cursor.execute(sql_select)
            # registros = cursor.fetchone()
            # salto, meta = registros
            # print(salto)
            # print(meta)

            # if estado == 'Activado':
            #     if temperatura <= meta:
            #         topico = 'motor/activacion'
            #         valor = 'desactivar'
            #         subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)

            #         mensaje_json = "{\"nombre\":\"Aire\", \"estado\": \"Desactivado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
            #         mensaje_dict = json.loads(mensaje_json)
            #         collection = dbEstados.dispositivoTemHum
            #         collection.insert_one(mensaje_dict)
            # elif estado == 'Desactivado':
            #     if temperatura >= salto:
            #         topico = 'motor/activacion'
            #         valor = 'activar'
            #         subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)

            #         mensaje_json = "{\"nombre\":\"Aire\", \"estado\": \"Activado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
            #         mensaje_dict = json.loads(mensaje_json)
            #         collection = dbEstados.dispositivoTemHum
            #         collection.insert_one(mensaje_dict)
            #------------------------------------------------------------------------------------------------------
        elif (mensaje_dict['Sensor'] == "CO2"):
            collection = db.CO2
            collection.insert_one(mensaje_dict)

            #CONFIGURACION AUTOMATICA DE EXTRACTOR Y VENTANA
            #------------------------------------------------------------------------------------------------------
            partes = str(msg.payload.decode()).split(',')
            temporal = partes[1].strip()
            subpartes = temporal.split(':')
            dioxido = subpartes[1].strip()
            
            # -------EXTRACTOR-----------
            # sql_select = "SELECT estado FROM motor WHERE id = 1"
            # cursor.execute(sql_select)
            # resultado = cursor.fetchone()
            # for estado in resultado:
            #     print(estado)

            # sql_select = "SELECT salto, meta FROM extractor WHERE id = 1"
            # cursor.execute(sql_select)
            # registros = cursor.fetchone()
            # salto, meta = registros
            # print(salto)
            # print(meta)

            # if estado == 'Activado':
            #     if dioxido <= meta:
            #         topico = 'motor/activacion'
            #         valor = 'desactivar'
            #         subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)

            #         mensaje_json = "{\"nombre\":\"Extractor\", \"estado\": \"Desactivado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
            #         mensaje_dict = json.loads(mensaje_json)
            #         collection = dbEstados.dispositivoCO2
            #         collection.insert_one(mensaje_dict)
            # elif estado == 'Desactivado':
            #     if dioxido >= salto:
            #         topico = 'motor/activacion'
            #         valor = 'activar'
            #         subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)
                    
            #         mensaje_json = "{\"nombre\":\"Extractor\", \"estado\": \"Activado\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
            #         mensaje_dict = json.loads(mensaje_json)
            #         collection = dbEstados.dispositivoCO2
            #         collection.insert_one(mensaje_dict)

            #-------VENTANA-----------
            sql_select = "SELECT estado FROM servo WHERE id = 1"
            cursor.execute(sql_select)
            resultado = cursor.fetchone()
            for estado in resultado:
                print(estado)

            sql_select = "SELECT salto, meta FROM ventana WHERE id = 1"
            cursor.execute(sql_select)
            registros = cursor.fetchone()
            salto, meta = registros

            if estado == 'Abierta':
                if float(dioxido) <= float(meta) and meta != '0.00':
                    topico = 'servo/activacion'
                    valor = 'desactivar'
                    subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)

                    mensaje_json = "{\"nombre\":\"Ventana\", \"estado\": \"Cerrada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
                    mensaje_dict = json.loads(mensaje_json)
                    collection = dbEstados.dispositivoCO2
                    collection.insert_one(mensaje_dict)
            elif estado == 'Cerrada':
                if float(dioxido) >= float(salto) and salto != '3000.00':
                    topico = 'servo/activacion'
                    valor = 'activar'
                    subprocess.run(['python', enviar_path, topico, valor], capture_output=True, text=True)

                    mensaje_json = "{\"nombre\":\"Ventana\", \"estado\": \"Abierta\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
                    mensaje_dict = json.loads(mensaje_json)
                    collection = dbEstados.dispositivoCO2
                    collection.insert_one(mensaje_dict)
            #------------------------------------------------------------------------------------------------------
        elif (mensaje_dict['Sensor'] == "Luz"):
            collection = db.Luminosidad
            collection.insert_one(mensaje_dict)

            partes = str(msg.payload.decode()).split(',')
            temporal = partes[1].strip()
            subpartes = temporal.split(':')
            idLuz = subpartes[1].strip()

            if int(idLuz) == 1:
                partes = str(msg.payload.decode()).split(',')
                temporal = partes[2].strip()
                subpartes = temporal.split(':')
                luz = subpartes[1].strip()

                sql_select = "SELECT configuracion, estado, luminosidad FROM configLuz WHERE id = 1"
                cursor.execute(sql_select)
                resultado = cursor.fetchone()
                configuracion, estadoLuz, luminosidad = resultado
                if configuracion == 'Automática' and float(luminosidad) >= 0.01:
                    if float(luminosidad) >= float(luz) and estadoLuz == 'Apagada':
                        topic = 'luz/led'
                        valor = 'encender'
                        subprocess.run(['python', enviar_path, topic, valor], capture_output=True, text=True)

                        mensaje_json = "{\"nombre\":\"Luz\", \"estado\": \"Encendida\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
                        mensaje_dict = json.loads(mensaje_json)
                        collection = dbEstados.dispositivoLuz
                        collection.insert_one(mensaje_dict)

                        sql_select = "UPDATE configLuz SET estado = 'Encendida' WHERE id = 1"
                        cursor.execute(sql_select)
                        conexion.commit()
                    elif float(luminosidad) < float(luz) and estadoLuz == 'Encendida':
                        topic = 'luz/led'
                        valor = 'apagar'
                        ahora = datetime.now()
                        subprocess.run(['python', enviar_path, topic, valor], capture_output=True, text=True)

                        mensaje_json = "{\"nombre\":\"Luz\", \"estado\": \"Apagada\", \"fecha\": \"" + ahora.strftime("%Y-%m-%d") + "\", \"hora\": \"" + ahora.strftime("%H:%M:%S") + "\"}"
                        mensaje_dict = json.loads(mensaje_json)
                        collection = dbEstados.dispositivoLuz
                        collection.insert_one(mensaje_dict)

                        sql_select = "UPDATE configLuz SET estado = 'Apagada' WHERE id = 1"
                        cursor.execute(sql_select)
                        conexion.commit()
    elif msg.topic == mqtt_topic_alarma:
        estado = str(msg.payload.decode())
        if estado == 'Conectada' or estado == 'Desconectada':
            print(estado)
            id_usuario = 1
            sql_update = "UPDATE alarma SET estado = %s WHERE id = %s"
            mensaje_env = (estado, id_usuario)
            cursor.execute(sql_update, mensaje_env)
            conexion.commit()
    elif msg.topic == mqtt_topic_motor:
        estado = str(msg.payload.decode())
        if estado == 'Activado' or estado == 'Desactivado':
            print(estado)
            id_usuario = 1
            sql_update = "UPDATE motor SET estado = %s WHERE id = %s"
            mensaje_dict = (estado, id_usuario)
            cursor.execute(sql_update, mensaje_dict)
            conexion.commit()
    elif msg.topic == mqtt_topic_servo:
        estado = str(msg.payload.decode())
        if estado == 'Abierta' or estado == 'Cerrada':
            print(estado)
            id_usuario = 1
            sql_update = "UPDATE servo SET estado = %s WHERE id = %s"
            mensaje_dict = (estado, id_usuario)
            cursor.execute(sql_update, mensaje_dict)
            conexion.commit()
    
    cursor.close()
    conexion.close()

# Crear un cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server, 1883, 60)
client.loop_forever()
