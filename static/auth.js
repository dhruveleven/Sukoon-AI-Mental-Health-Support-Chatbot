document.addEventListener('DOMContentLoaded', function() {
    const passwordMatchError = document.getElementById('passwordMatchError');
    const authForm = document.querySelector('form');
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const confirmPasswordToggle = document.getElementById('confirmPasswordToggle');

    authForm.addEventListener('submit', async (event) => {
        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;
        const confirmPassword = document.querySelector('input[name="confirm_password"]').value;
        const isSignup = event.submitter.name === 'signup';

        if (isSignup && password !== confirmPassword) {
            passwordMatchError.textContent = "Passwords do not match.";
            event.preventDefault();
            return;
        } else {
            passwordMatchError.textContent = "";
        }
    });

    passwordToggle.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            passwordToggle.classList.remove('fa-eye');
            passwordToggle.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            passwordToggle.classList.remove('fa-eye-slash');
            passwordToggle.classList.add('fa-eye');
        }
    });

    confirmPasswordToggle.addEventListener('click', function() {
        if (confirmPasswordInput.type === 'password') {
            confirmPasswordInput.type = 'text';
            confirmPasswordToggle.classList.remove('fa-eye');
            confirmPasswordToggle.classList.add('fa-eye-slash');
        } else {
            confirmPasswordInput.type = 'password';
            confirmPasswordToggle.classList.remove('fa-eye-slash');
            confirmPasswordToggle.classList.add('fa-eye');
        }
    });
    const words = ["peace", "balance", "closure", "tranquility"];
    const element = document.getElementById("dynamicWord");
    let wordIndex = 0;
    let charIndex = 0;

    function typeWriter() {
        if (charIndex < words[wordIndex].length) {
            element.textContent += words[wordIndex].charAt(charIndex);
            charIndex++;
            setTimeout(typeWriter, 150); // Typing speed
        } else {
            setTimeout(() => {
                eraseText();
            }, 1000); // Delay before erasing
        }
    }

    function eraseText() {
        if (charIndex > 0) {
            element.textContent = element.textContent.slice(0, -1);
            charIndex--;
            setTimeout(eraseText, 100); // Erasing speed
        } else {
            wordIndex = (wordIndex + 1) % words.length; // Cycle through words
            setTimeout(typeWriter, 500); // Delay before typing next word
        }
    }

    typeWriter(); // Start the effect
});