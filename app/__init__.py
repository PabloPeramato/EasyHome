from flask import Flask
from pymongo import MongoClient
from flask_restx import Api

app = Flask(__name__)
app.secret_key = "super secret key"
api = Api(app, version='1.0', title='Mi API', description='Una simple API', doc='/docs')

# Configuración de MongoDB para DB Users
client = MongoClient('mongodb://localhost:27017')
dbUsers = client.Users
users_collectionUsers = dbUsers.usuarios

# Configuración de MongoDB para DB Sensores
client = MongoClient('mongodb://localhost:27017')
dbSensores = client.Sensores

# Configuración de MongoDB para DB Estados
client = MongoClient('mongodb://localhost:27017')
dbEstados = client.Estados

# Importar rutas después de configurar la base de datos
from app.routes import usuarios
from app.routes import principal
from app.routes import sensores