from app import app
import subprocess
import os

def lanzarBroker():
    recibir_path = os.path.join(os.path.dirname(__file__), 'recibir.py')
    subprocess.run(['python', recibir_path], capture_output=True, text=True)

if __name__ == '__main__':
    lanzarBroker()    
    app.run(debug=True)
