const chatHistory = document.getElementById('chatHistory');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const passwordMatchError = document.getElementById('passwordMatchError'); // New element


if (userId) { // Check if userId is defined before running the rest of the javascript.
    async function loadChatHistory() {
        try {
            const response = await fetch(`/chat_history/${userId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const history = await response.json();
            chatHistory.innerHTML = '';
            history.forEach(item => {
                chatHistory.innerHTML += `<p>User: ${item[1]}</p><p>Bot: ${item[2]}</p>`;
            });
        } catch (error) {
            console.error("Error loading chat history:", error);
        }
    }

    sendButton.addEventListener('click', async () => {
        const message = chatInput.value;
        try {
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message: message })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            chatHistory.innerHTML += `<p>User: ${message}</p><p>Bot: ${data.response}</p>`;
            chatInput.value = '';
        } catch (error) {
            console.error("Error sending message:", error);
        }
    });

    loadChatHistory();
}

const signupButton = document.querySelector('button[name="signup"]');
if (signupButton) {
    signupButton.addEventListener('click', async (event) => {
        event.preventDefault();

        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;
        const confirmPassword = document.querySelector('input[name="confirm_password"]').value;

        if (password !== confirmPassword) {
            passwordMatchError.textContent = "Passwords do not match.";
            return;
        } else {
            passwordMatchError.textContent = "";
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            if (response.ok) {
                console.log(data.message);
            } else {
                console.error(data.message);
            }
        } catch (error) {
            console.error("Signup error:", error);
        }
    });
}
/*
// Modify the signup button event listener:
document.querySelector('button[name="signup"]').addEventListener('click', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value; // Get confirm password

    if (password !== confirmPassword) {
        passwordMatchError.textContent = "Passwords do not match.";
        return;
    } else {
        passwordMatchError.textContent = ""; // Clear the error message
    }

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (response.ok) {
            // Handle success
            console.log(data.message);
        } else {
            // Handle error
            console.error(data.message);
        }
    } catch (error) {
        console.error("Signup error:", error);
    }
});
*/
