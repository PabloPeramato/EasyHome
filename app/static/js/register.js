document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        var flashMessage = document.getElementById('.flash-message');
        if (flashMessage) {
            flashMessage.style.display = 'none';
        }
    }, 5000); // 5000 ms = 5 segundos
});

// Function to check password match
const form = document.querySelector('form');
form.addEventListener('submit', function(event) {
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    
    console.log(password !== confirm_password);
    if (password !== confirm_password) {
        console.log(password);
        console.log(confirm_password);
        event.preventDefault(); // Prevent form submission
        const flashMessageElement = document.getElementById('flash-message');
        flashMessageElement.innerText = "Passwords do not match.";
        flashMessageElement.style.display = 'block';
        setTimeout(() => {
            flashMessageElement.style.display = 'none';
        }, 3000); // Message disappears after 3 seconds
    } 
});