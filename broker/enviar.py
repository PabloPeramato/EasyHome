import paho.mqtt.client as mqtt
import socket
import sys

# Configura el broker MQTT y el puerto
broker_address = socket.gethostbyname(socket.gethostname())
port = 1883
topic = sys.argv[1]
valor = sys.argv[2]

# Función de callback cuando se conecta al broker MQTT
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conectado al broker MQTT, " + topic + ", " + valor)
        client.publish(topic, valor)
        client.disconnect()
    else:
        print(f"Error al conectar. Código de error: {rc}")

# Crear un cliente MQTT
client = mqtt.Client()

# Asignar la función de callback
client.on_connect = on_connect

# Conectar al broker
client.connect(broker_address, port)
client.loop_start()
client.loop_stop()