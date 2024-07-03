function showFlashMessage(message, button) {
    var flashMessage = document.getElementById('flash-message');
    var rect = button.getBoundingClientRect();
    flashMessage.textContent = message;
    flashMessage.style.top = rect.top + rect.height + 10 + 'px'; // Ajusta la posición vertical
    flashMessage.style.left = rect.left + (rect.width / 2) + 'px'; // Ajusta la posición horizontal
    flashMessage.style.display = 'block';
    setTimeout(function() {
        flashMessage.style.display = 'none';
    }, 3000);
}

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

    if (floatValue < 0 || floatValue > 3000) {
        input.value = value.slice(0, -1); // Eliminar el último carácter si está fuera de rango
    }
}

function transferirValores(num1, num2, form) {
    const input1 = document.getElementById(num1).value;
    const input2 = document.getElementById(num2).value;
    if (form == "form1") {
        const hiddenInput1 = document.getElementById('hiddenInput1');
        const hiddenInput2 = document.getElementById('hiddenInput2');
        hiddenInput1.value = input1;
        hiddenInput2.value = input2;
    } else if (form == "form2") {
        const hiddenInput3 = document.getElementById('hiddenInput3');
        const hiddenInput4 = document.getElementById('hiddenInput4');
        hiddenInput3.value = input1;
        hiddenInput4.value = input2;
    }
    
    document.getElementById(form).submit();

}