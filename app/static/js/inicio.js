function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(function() {
        showFlashMessage('Copiado en el portapapeles: ' + text, button);
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

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