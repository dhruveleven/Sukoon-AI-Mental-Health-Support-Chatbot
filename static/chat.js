const chatHistory = document.getElementById('chatHistory');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const issueDropdown = document.getElementById('issueDropdown'); // Added dropdown selection

const issuePrompts = {
    anxiety: "I'm feeling anxious. What are some coping strategies?",
    depression: "I'm feeling depressed. What can I do to feel better?",
    stress: "I'm feeling stressed. How can I manage my stress?",
    relationship: "I am having relationship problems, what should I do?",
    sleep: "I am having trouble sleeping, what are some techniques that could help?",
    motivation: "I am having trouble staying motivated, what are some tips?"
    // Add more prompts as needed
};

const apiPrompts = {
    anxiety: "I'm feeling anxious. What are some coping strategies? Keep your response concise.",
    depression: "I'm feeling depressed. What can I do to feel better? Be brief with your response.",
    stress: "I'm feeling stressed. How can I manage my stress? Respond in 100 words or less.",
    relationship: "I am having relationship problems, what should I do? Please use short paragraphs.",
    sleep: "I am having trouble sleeping, what are some techniques that could help? Use bullet points.",
    motivation: "I am having trouble staying motivated, what are some tips? Keep your response under 200 characters."
    // Add more prompts as needed
};


if (userId) {
    async function loadChatHistory() {
        try {
            const response = await fetch(`/chat_history/${userId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const history = await response.json();
            chatHistory.innerHTML = '';
            history.forEach(item => {
                // Add user message with user-message class
                const userMessage = document.createElement('div');
                userMessage.className = 'user-message';
                userMessage.textContent = item[1];
                chatHistory.appendChild(userMessage);
                
                // Add bot message with bot-message class - use innerHTML to render HTML content
                const botMessage = document.createElement('div');
                botMessage.className = 'bot-message';
                
                // Process the bot response to handle HTML tags
                const processedResponse = processResponse(item[2]);
                botMessage.innerHTML = processedResponse;
                
                chatHistory.appendChild(botMessage);
            });
        } catch (error) {
            console.error("Error loading chat history:", error);
        }
    }
    
    // Function to process the bot's response
    function processResponse(response) {
        // Check if response contains HTML tags but isn't properly rendered
        if (response.includes('<p>') || response.includes('<ul>') || response.includes('<ol>')) {
            // It's already HTML, just need to ensure it's rendered
            return response;
        } else {
            // Convert plain text to HTML with paragraphs for better formatting
            // Split by double newlines and wrap in paragraphs
            const markdownConverter = new showdown.Converter();
            const paragraphs = response.split(/\n\n+/);
            return paragraphs.map(p => `<p>${markdownConverter.makeHtml(p.replace(/\n/g, '<br>'))}</p>`).join('');
        }
    }

    sendButton.addEventListener('click', async () => {
        const message = chatInput.value;
        if (!message.trim()) return; // Prevent empty messages
        
        try {
            // Add user message with user-message class
            const userMessage = document.createElement('div');
            userMessage.className = 'user-message';
            userMessage.textContent = message;
            chatHistory.appendChild(userMessage);
            
            chatInput.value = '';
            
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message: message })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            // Add bot message with bot-message class
            const botMessage = document.createElement('div');
            botMessage.className = 'bot-message';
            
            // Process the bot response to handle HTML tags
            const processedResponse = processResponse(data.response);
            botMessage.innerHTML = processedResponse;
            
            chatHistory.appendChild(botMessage);
            
            // Scroll to bottom of chat
            chatHistory.scrollTop = chatHistory.scrollHeight;
        } catch (error) {
            console.error("Error sending message:", error);
        }
    });
    
    issueDropdown.addEventListener('change', async () => {
        const selectedIssue = issueDropdown.value;
        if (selectedIssue && issuePrompts[selectedIssue]) {
            const userPrompt = issuePrompts[selectedIssue]; // Use user-friendly prompt
            const apiPrompt = apiPrompts[selectedIssue];
            
            // Add user message from dropdown selection
            const userMessage = document.createElement('div');
            userMessage.className = 'user-message';
            userMessage.textContent = userPrompt;
            chatHistory.appendChild(userMessage);
            
            chatInput.value = ''; // clear the input field

            try {
                const response = await fetch('/send_message', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: userId, message: apiPrompt })
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                
                // Add bot message with bot-message class
                const botMessage = document.createElement('div');
                botMessage.className = 'bot-message';
                
                // Process the bot response to handle HTML tags
                const processedResponse = processResponse(data.response);
                botMessage.innerHTML = processedResponse;
                
                chatHistory.appendChild(botMessage);
                
                // Scroll to bottom of chat
                chatHistory.scrollTop = chatHistory.scrollHeight;
                
                // Reset the dropdown
                issueDropdown.value = '';
            } catch (error) {
                console.error("Error sending message:", error);
            }
        }
    });

    document.getElementById('checkInForm').addEventListener('submit', async function(event) {
        event.preventDefault();
    
        const mood = document.getElementById('mood').value;
        const sadness = document.querySelector('input[name="sadness"]:checked').value;
        const anxiety = document.querySelector('input[name="anxiety"]:checked').value;
        const sleep = document.querySelector('input[name="sleep"]:checked').value;
        const appetite = document.querySelector('input[name="appetite"]:checked').value;
        const fatigue = document.querySelector('input[name="fatigue"]:checked').value;
        const concentration = document.querySelector('input[name="concentration"]:checked').value;
    
        const formData = {
            mood: mood,
            sadness: sadness,
            anxiety: anxiety,
            sleep: sleep,
            appetite: appetite,
            fatigue: fatigue,
            concentration: concentration
        };
    
        try {
            const response = await fetch('/analyze_checkin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, formData: formData })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            // Add a user message for check-in submission
            const userMessage = document.createElement('div');
            userMessage.className = 'user-message';
            userMessage.textContent = "Mental Health Check-in submitted";
            chatHistory.appendChild(userMessage);
            
            // Add bot message with the check-in response
            const botMessage = document.createElement('div');
            botMessage.className = 'bot-message';
            
            // Process the bot response to handle HTML tags
            const processedResponse = processResponse(data.recommendations);
            botMessage.innerHTML = processedResponse;
            
            chatHistory.appendChild(botMessage);
            
            // Scroll to bottom of chat
            chatHistory.scrollTop = chatHistory.scrollHeight;
            
            document.getElementById('mentalHealthForm').style.display = 'none';
        } catch (error) {
            console.error("Error analyzing check-in:", error);
        }
    });

    // Add the event listener for the Enter key
    chatInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
    
    // Add auto-scroll functionality
    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    loadChatHistory();
    // Scroll to bottom after loading history
    setTimeout(scrollToBottom, 100);
}