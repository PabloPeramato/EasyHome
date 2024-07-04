#include <DHT.h>           
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <BH1750.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

#define DHTTYPE  DHT22  // Modelo del sensor DHT22
#define DHTPIN    4     // PIN al que está conectado el sensor DHT22 en la ESP32
#define GASPIN    34    // PIN al que está conectado el sensor de GAS en la ESP32
#define BOTtoken "7018717968:AAGZpGujBs7Ndxz25I4GrATm91Dq79emWWI"  // Token del bot de telegram
#define CHAT_ID "868424504" // ID del chat de telegram
#define MOTOR_PIN 5 
#define SERVO_PIN 2
#define ALARMA_PIN 13
#define BUZ_PIN 12
#define LED_PIN 32

unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

const char* ssid = "TP-LIN_PABLO";
const char* password = "PradoPocito48";

// Configuración del broker MQTT
const char* mqtt_server = "192.168.0.106";  // Cambia esto por la IP de tu broker MQTT
const char* mqtt_port_envio = "1883";
const char* mqtt_topic_envio = "sensor/datos";
const char* mqtt_topic_alarma = "alarma/conexion";
const char* mqtt_topic_motor = "motor/activacion";
const char* mqtt_topic_servo = "servo/activacion";
const char* mqtt_topic_luz = "luz/led";
char mensaje[200];
WiFiClient espClient;
PubSubClient client(espClient);

// Servidor thingspeak url con la api_key para realizar gráficas.
String serverName = "https://api.thingspeak.com/update?api_key=UJB9TWC5YPAAWB3L";

// Sensor de temperatura y humedad
DHT dht(DHTPIN, DHTTYPE, 22);
double temperatura;
double humedad;

// Sensor de CO2
float data;
//float rzero; // Valor de resistencia del sensor
//float CO2;   // Concentración de CO2 en ppm
//MQ135 gasSensor = MQ135(GASPIN);

// Sensor de movimiento Alarma
WiFiClientSecure cliente;
UniversalTelegramBot bot(BOTtoken, cliente);
int botRequestDelay = 1000;   // Busca nuevos mensajes cada 1 segundo.
unsigned long lastTimeBotRan;
int buzState = 0;
bool motionDetected1 = false;
bool booleanoAlarma = false;

// Sensor de luz
BH1750 lightMeter1(0x23);
BH1750 lightMeter2(0x5C);
float lux1;
float lux2;

// Servo motor
Servo myservo;


void IRAM_ATTR detectsMovement() {
    motionDetected1 = true;
}

void setup() {
    Serial.begin(115200);   //Se inicia la comunicación serial 
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);

    // Sensor de temperatura y humedad
    configurarTemperaturaHumedad();

    // Sensor de CO2
    configurarCO2();

    // Sensor de luz
    configurarLuz();

    // Sensor de movimiento Alarma
    configurarAlarma();

    // Motor
    pinMode(MOTOR_PIN, OUTPUT);

    // Servo
    myservo.attach(SERVO_PIN);

    delay(5000); // Tiempo de espera para que se calienten los sensores
    Serial.println("--------------------------");
}

void loop() {

    if (!client.connected()) {
        reconnect();
    }
    client.loop();
  
    if ((millis() - lastTime) > timerDelay) { // Check if its been a minute
        // TEMPERATURA Y HUMEDAD
        funcionTemperaturaHumedad();

        // CO2
        funcionCO2();

        // LUZ
        funcionLuz();

        if(WiFi.status() == WL_CONNECTED) { // Check to make sure wifi is still connected
            sendData(temperatura, humedad, lux1, data); // Call the sendData function defined below
            data = 0;
        } else {
            Serial.println("WiFi Disconnected");
        }
        Serial.println("--------------------------");

        lastTime = millis();
    }

    // Sensor de movimiento Alarma
    if (booleanoAlarma) {
        funcionAlarma();
    }
    
}

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Conectando a ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    #ifdef ESP32
        cliente.setCACert(TELEGRAM_CERTIFICATE_ROOT); // Add root certificate for api.telegram.org
    #endif

    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi conectado");
    Serial.println("Dirección IP: ");
    Serial.println(WiFi.localIP());
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Intentando conexión MQTT a ");
        Serial.println(mqtt_server);

        if (client.connect("ArduinoClient")) {
            Serial.println("Conectado");
            // Suscribirse al tema "alarma"
            client.subscribe(mqtt_topic_alarma);
            client.subscribe(mqtt_topic_motor);
            client.subscribe(mqtt_topic_servo);
            client.subscribe(mqtt_topic_luz);
        } else {
            Serial.print("Fallo, rc=");
            Serial.print(client.state());
            Serial.println(" intentando de nuevo en 5 segundos");
            delay(5000);
        }
    }
}

void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Mensaje recibido en el tema: ");
    Serial.println(topic);
    Serial.print("Mensaje: ");

    char* mensaje = (char*)malloc(length + 1);
    if (mensaje == NULL) {
        Serial.println("Error al asignar memoria");
        return;
    }

    for (unsigned int i = 0; i < length; i++) {
        mensaje[i] = (char)payload[i];
        Serial.print((char)payload[i]);
    }
    mensaje[length] = '\0';
    Serial.println(mensaje);

    // Manejo del mensaje del tema "alarma"
    if (strcmp(topic, mqtt_topic_alarma) == 0) {
        // Aquí puedes manejar el mensaje recibido en el tema "alarma"
        // Por ejemplo, podrías activar o desactivar una alarma
        if (strcmp(mensaje, "conectar") == 0) {
            booleanoAlarma = true;
            Serial.println("Alarma conectada");
            client.publish(mqtt_topic_alarma, "Conectada");
        } else if (strcmp(mensaje, "desconectar") == 0) {
            booleanoAlarma = false;
            Serial.println("Alarma desconectada");
            client.publish(mqtt_topic_alarma, "Desconectada");
        }
        // Manejo adicional según el mensaje recibido
    } else if (strcmp(topic, mqtt_topic_motor) == 0) {
        if (strcmp(mensaje, "activar") == 0) {
            digitalWrite(MOTOR_PIN, HIGH);
            Serial.println("Motor activado");
            client.publish(mqtt_topic_motor, "Activado");
        } else if (strcmp(mensaje, "desactivar") == 0) {
            digitalWrite(MOTOR_PIN, LOW);
            Serial.println("Motor desactivado");
            client.publish(mqtt_topic_motor, "Desactivado");
        }
    } else if (strcmp(topic, mqtt_topic_servo) == 0) {
        if (strcmp(mensaje, "activar") == 0) {
            myservo.write(180);
            Serial.println("Servo activado");
            client.publish(mqtt_topic_servo, "Abierta");
        } else if (strcmp(mensaje, "desactivar") == 0) {
            myservo.write(0);
            Serial.println("Servo desactivado");
            client.publish(mqtt_topic_servo, "Cerrada");
        }
    } else if (strcmp(topic, mqtt_topic_luz) == 0) {
        if (strcmp(mensaje, "encender") == 0) {
            digitalWrite(LED_PIN, HIGH);
        } else if (strcmp(mensaje, "apagar") == 0) {
            digitalWrite(LED_PIN, LOW);
        }
    }
}

void configurarTemperaturaHumedad() {
    dht.begin();
}

void funcionTemperaturaHumedad() {
    temperatura = dht.readTemperature();
    humedad = dht.readHumidity();
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.println(" ºC.");
    Serial.print("Humedad: "); 
    Serial.print(humedad);
    Serial.println(" %.");
    snprintf(mensaje, 200, "{\"Sensor\": \"TemHum\", \"temperatura\": %.2f, \"humedad\": %.2f, ", temperatura, humedad);
    Serial.print("Publicando mensaje: ");
    Serial.println(mensaje);
    client.publish(mqtt_topic_envio, mensaje);
}

void configurarCO2() {
    pinMode(GASPIN, INPUT);
}

void funcionCO2() {
    
    data = analogRead(GASPIN);
    //rzero = gasSensor.getRZero();
    //CO2 = gasSensor.getPPM();

    Serial.print("CO2: ");
    Serial.print(data);
    //Serial.print("RZero: ");
    //Serial.println(rzero);
    //Serial.print("CO2: ");
    //Serial.print(CO2);
    Serial.println(" ppm");
    snprintf(mensaje, 200, "{\"Sensor\": \"CO2\", \"data\": %.2f, ", data);
    Serial.print("Publicando mensaje: ");
    Serial.println(mensaje);
    client.publish(mqtt_topic_envio, mensaje);

}

void configurarLuz() {

    pinMode(LED_PIN, OUTPUT);

    Wire.begin(21, 22);
    if (lightMeter1.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x23, &Wire)) {
        Serial.println("BH1750 (sensor 1) iniciado correctamente");
    } else {
        Serial.println("Error al iniciar BH1750 (sensor 1)");
    }
    if (lightMeter2.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x5C, &Wire)) {
        Serial.println("BH1750 (sensor 2) iniciado correctamente");
    } else {
        Serial.println("Error al iniciar BH1750 (sensor 2)");
    }

}

void funcionLuz() {
    lux1 = lightMeter1.readLightLevel();
    Serial.print("Sensor 1 Light: ");
    Serial.print(lux1);
    Serial.println(" lx");
    if (lux1 >= 0.00) {
        snprintf(mensaje, 200, "{\"Sensor\": \"Luz\", \"id\": 1, \"lux\": %.2f, ", lux1);
        Serial.print("Publicando mensaje: ");
        Serial.println(mensaje);
        client.publish(mqtt_topic_envio, mensaje);
    }
    
    lux2 = lightMeter2.readLightLevel();
    Serial.print("Sensor 2 Light: ");
    Serial.print(lux2);
    Serial.println(" lx");
    if (lux2 >= 0.00) {
        snprintf(mensaje, 200, "{\"Sensor\": \"Luz\", \"id\": 2, \"lux\": %.2f, ", lux2);
        Serial.print("Publicando mensaje: ");
        Serial.println(mensaje);
        client.publish(mqtt_topic_envio, mensaje);
    }
}

void configurarAlarma() {
    pinMode(ALARMA_PIN, INPUT_PULLUP);
    pinMode(BUZ_PIN, OUTPUT);
    digitalWrite(BUZ_PIN, buzState);
    attachInterrupt(digitalPinToInterrupt(ALARMA_PIN), detectsMovement, RISING);
}

void funcionAlarma() {
    if (millis() > lastTimeBotRan + botRequestDelay)  {
        int numNewMessages = bot.getUpdates(bot.last_message_received + 1);

        while(numNewMessages) {
            Serial.println("got response");
            handleNewMessages(numNewMessages);
            numNewMessages = bot.getUpdates(bot.last_message_received + 1);
        }

        if(motionDetected1) {
            String mensaje = "¡¡¡ MOVIMIENTO DETECTADO !!!\n\n";
            mensaje += "¿ Quiere encender la alarma ?:  /alarma_on \n";
            Serial.println("¡¡¡ Movimiento detectado !!!\n");
            bot.sendMessage(CHAT_ID, mensaje, "");
            motionDetected1 = false;
        }

        lastTimeBotRan = millis();
    }
}

void sendData(double temperatura, double humedad, float luz, float CO2) {
    HTTPClient http; // Initialize our HTTP client
    String url = serverName + "&field1=" + temperatura + "&field2=" + humedad + "&field3=" + luz + "&field4=" + CO2; // Define our entire url 
    
    http.begin(url.c_str()); // Initialize our HTTP request 
    int httpResponseCode = http.GET(); // Send HTTP request
        
    if (httpResponseCode > 0){ // Check for good HTTP status code
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
    }else{
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
    }

    http.end();
}

void handleNewMessages(int numNewMessages) {
    Serial.println("handleNewMessages");
    Serial.println(String(numNewMessages));

    for (int i = 0; i<numNewMessages; i++) {
        // Chat id of the requester
        String chat_id = String(bot.messages[i].chat_id);
        if (chat_id != CHAT_ID){
            bot.sendMessage(chat_id, "Unauthorized user", "");
            continue;
        }
    
        // Print the received message
        String text = bot.messages[i].text;
        Serial.println(text);

        String from_name = bot.messages[i].from_name;

        if (text == "/start") {
            String benvingut = "Bienvenido, " + from_name + ".\n";
            benvingut += "Utiliza los siguientes comandos para controlar tus OUTPUTS.\n\n";
            benvingut += "/alarma_on para ENCENDER la alarma \n";
            benvingut += "/alarma_off para APAGAR la alarma \n";
            benvingut += "/estado para saber el ESTADO ACTUAL de la alarma \n";
            bot.sendMessage(chat_id, benvingut, "");
        }

        if (text == "/alarma_on") {
            String mensaje = "La ALARMA ahora está ENCENDIDA.\n\n";
            mensaje += "Pulse /alarma_off si desea APAGAR la ALARMA.\n";
            bot.sendMessage(chat_id, mensaje, "");
            buzState = 10;
            digitalWrite(BUZ_PIN, buzState);
        }
    
        if (text == "/alarma_off") {
            String mensaje = "La ALARMA ahora está APAGADA.\n\n";
            mensaje += "Pulse /alarma_on si desea ENCENDER la ALARMA.\n";
            bot.sendMessage(chat_id, mensaje, "");
            buzState = 0;
            digitalWrite(BUZ_PIN, buzState);
        }
    
        if (text == "/estado") {
            if (digitalRead(BUZ_PIN)){
                String mensaje = "La ALARMA está ENCENDIDA.\n\n";
                mensaje += "Pulse /alarma_off para APAGAR la ALARMA.\n";
                bot.sendMessage(chat_id, mensaje, "");
            }
            else{
                String mensaje = "La ALARMA está APAGADA.\n\n";
                mensaje += "Pulse /alarma_on para ENCENDER la ALARMA";
                bot.sendMessage(chat_id, mensaje, "");
            }
        }
    }
}