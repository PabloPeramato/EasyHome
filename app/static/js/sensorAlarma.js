function conectar() {
    fetch('/inicio/sensorAlarma/conectar', {
        method: 'POST'
    })
    .catch(error => console.error('Error:', error));
}

function desconectar() {
    fetch('/inicio/sensorAlarma/desconectar', {
        method: 'POST'
    })
    .catch(error => console.error('Error:', error));
}
