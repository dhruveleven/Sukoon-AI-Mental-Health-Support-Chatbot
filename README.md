# 🌿 Sukoon AI – Mental Health Support Chatbot

Sukoon AI is a **Flask-based web application** designed to provide mental health support through an intelligent chatbot.  
The project creates a user-friendly interface to create a safe space where users can share their thoughts and receive AI-driven support.

---

## ✨ Features
- 💬 **AI-Powered Chatbot** – Provides empathetic and context-aware responses using Gemini API  
- 👤 **User Authentication** – Secure login and registration system  
- 🧠 **Mental Health Focus** – Safe and supportive interaction environment  
- 🗄️ **SQLite Database** – For user data management and chat history persistence  
- 🎨 **Clean UI** – Responsive frontend built with HTML, CSS, and JavaScript  
- 🔐 **Environment Variables** – API keys and sensitive data kept secure  

---

## 🛠️ Technologies Used
- **Backend**: Python (Flask)  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: SQLite  
- **AI Integration**: Google Gemini API  

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/Sukoon-AI-Mental-Health-Support-Chatbot.git
cd Sukoon-AI-Mental-Health-Support-Chatbot/backend
````

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On macOS/Linux

pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file inside `backend/`:

```env
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
```

### 4. Run the application

```bash
python app.py
```

### 5. Access in browser

Open: [http://localhost:5000](http://localhost:5000)

---

## 📂 Project Structure

```
├── backend/
│   ├── app.py               # Main Flask application
│   ├── auth.py              # Authentication logic
│   ├── auth_functions.py    # Helper functions for login/signup
│   ├── database.py          # SQLite database models
│   ├── gemini_api.py        # Gemini API integration
│   ├── mental_health_chatbot.db # SQLite database
│   ├── static/              # JavaScript, CSS
│   ├── templates/           # HTML templates (index, auth, chat)
│   └── requirements.txt     # Python dependencies
```

---

## 📜 License

This project is developed for **educational purposes** to explore the intersection of AI and mental health technology.

---

## 👩‍💻 Contributors

* Dhruv Patel

---

##Screenshots
### Login Page
<img width="959" height="447" alt="login" src="https://github.com/user-attachments/assets/e2bc9dae-ad72-489d-a36c-a65f7febab11" />

### Main Page
<img width="959" height="440" alt="home" src="https://github.com/user-attachments/assets/8b01bf59-8318-423c-82c2-87e859006b47" />
