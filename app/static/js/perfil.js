
// Agregar un evento de enfoque para los campos de entrada text2
document.addEventListener('DOMContentLoaded', function() {
    var text2Inputs = document.querySelectorAll('input[type="text2"]');
    text2Inputs.forEach(function(input) {
        var originalValue = input.value;
        input.addEventListener('focus', function() {
            if (input.value === originalValue) {
                input.value = '';
                input.style.color = '#000'; // Cambiar el color del texto al escribir
            }
        });
        input.addEventListener('blur', function() {
            if (input.value === '') {
                input.value = originalValue;
                input.style.color = '#7e7e7e'; // Restaurar el color del texto original
            }
        });
    });
});

function validarInput(event) {
    const input = event.target;
    let value = input.value.trim(); // Eliminar espacios en blanco al inicio y al final
    const regex = /^-?\d*\.?\d{0,2}$/;

    if (!regex.test(value)) {
        input.value = value.slice(0, -1); // Eliminar el último carácter si no coincide con la regex
        return;
    }

    const floatValue = parseFloat(value);

    if (floatValue < -20 || floatValue > 50) {
        input.value = value.slice(0, -1); // Eliminar el último carácter si está fuera de rango
    }
}

function transferirValores() {
    var email = document.getElementById('mail').value;
    var telefono = document.getElementById('telefono').value;

    document.getElementById('hiddenInput1').value = email;
    document.getElementById('hiddenInput2').value = telefono;
}