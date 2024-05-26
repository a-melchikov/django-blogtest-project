document.addEventListener('DOMContentLoaded', function() {
    const passwordToggleIcons = document.querySelectorAll('.password-toggle-icon');
    
    passwordToggleIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const passwordInput = document.querySelector(icon.getAttribute('toggle'));
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });
});