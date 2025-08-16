from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_cors import CORS
import auth
import database
import gemini_api
import os
import markdown
from flask import Flask, request, jsonify
import gemini_api 

"""template_dir = os.path.join('..', 'templates')
app = Flask(__name__, template_folder=template_dir)"""
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"Received registration data: {data}")
    username = data.get('username')
    password = data.get('password')
    auth.register_user(username, password)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Received login data: {data}")
    username = data.get('username')
    password = data.get('password')
    if auth.verify_user(username, password):
        user_id = auth.get_user_id(username)
        print(f"Login successful for user: {username}, ID: {user_id}")
        return jsonify({'message': 'Login successful', 'user_id': user_id}), 200
    else:
        print(f"Login failed for user: {username}")
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/chat_history/<user_id>', methods=['GET'])
def get_history(user_id):
    print(f"Retrieving chat history for user ID: {user_id}")
    history = database.get_chat_history(user_id)
    return jsonify(history), 200

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    print(f"Received message data: {data}")
    user_id = data.get('user_id')
    message = data.get("message")
    response = gemini_api.get_gemini_response(message)
    response = markdown.markdown(response)
    database.insert_chat_message(user_id, message, response)
    return jsonify({"response": response})

@app.route('/', methods=['GET', 'POST'])
def auth_page():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if 'login' in request.form:
                user_verification = auth.verify_user(username, password)
                if user_verification:
                    user_id = auth.get_user_id(username)
                    return redirect(url_for('chat_page', user_id=user_id)) #redirect to chat page.
                else:
                    return render_template('auth.html', error='Invalid credentials')
            elif 'signup' in request.form:
                auth.register_user(username, password)
                return render_template('auth.html')
    return render_template('auth.html')

@app.route('/chat/<user_id>')
def chat_page(user_id):
    return render_template('chat.html', logged_in=True, user_id=user_id)

@app.route('/logout')
def logout():
    return redirect(url_for('auth_page'))

def analyze_checkin_data(form_data):
    """Analyzes mental health check-in data and generates recommendations."""

    # Data Preprocessing (Convert responses to numerical values)
    sadness = 1 if form_data['sadness'] == "yes" else 0
    anxiety = 1 if form_data['anxiety'] == "yes" else 0
    sleep = 1 if form_data['sleep'] == "yes" else 0
    appetite = 1 if form_data['appetite'] == "yes" else 0
    fatigue = 1 if form_data['fatigue'] == "yes" else 0
    concentration = 1 if form_data['concentration'] == "yes" else 0
    mood = int(form_data['mood'])

    # Weighted Symptom Scoring
    weights = {
        'sadness': 4, 'anxiety': 3, 'sleep': 2, 'appetite': 2, 'fatigue': 2, 'concentration': 2,
    }
    weighted_scores = {
        'sadness': sadness * weights['sadness'],
        'anxiety': anxiety * weights['anxiety'],
        'sleep': sleep * weights['sleep'],
        'appetite': appetite * weights['appetite'],
        'fatigue': fatigue * weights['fatigue'],
        'concentration': concentration * weights['concentration'],
    }

    total_weighted_score = sum(weighted_scores.values())

    # Symptom Cluster Analysis
    depression_cluster = ['sadness', 'fatigue', 'concentration']
    anxiety_cluster = ['anxiety', 'sleep']
    depression_cluster_score = sum(weighted_scores[symptom] for symptom in depression_cluster)
    anxiety_cluster_score = sum(weighted_scores[symptom] for symptom in anxiety_cluster)

    # Condition Identification
    recommendations = "Based on your responses, here are some recommendations:\n\n"

    if depression_cluster_score > 15 and total_weighted_score > 20:
        recommendations += "- You may be experiencing symptoms of depression. Consider seeking professional help.\n"
    if anxiety_cluster_score > 12:
        recommendations += "- You may be experiencing symptoms of anxiety. Try relaxation techniques.\n"

    if weighted_scores['sleep'] > 3:
      recommendations += "- you are experiencing sleep disturbances, try a consistent bedtime routine.\n"

    if weighted_scores['appetite'] > 3:
      recommendations += "- You are experiencing appetite changes, consider tracking your food intake.\n"

    if mood <= 2:
      recommendations += "- You are experiencing a low mood, consider engaging in self care activities.\n"

    # Gemini API Integration
    gemini_prompt = f"user data = {form_data}, depression score = {depression_cluster_score}, anxiety score = {anxiety_cluster_score}. give a detailed response"
    gemini_response = gemini_api.get_gemini_response(gemini_prompt)
    recommendations += "\n\n" + gemini_response

    recommendations += "\n\n- If you are in crisis, please contact a crisis hotline immediately.\n- These recommendations are not a substitute for professional mental health care."

    return recommendations

@app.route('/analyze_checkin', methods=['POST'])
def analyze_checkin():
    data = request.get_json()
    form_data = data.get('formData')
    recommendations = analyze_checkin_data(form_data)
    recommendations = markdown.markdown(recommendations)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)


#----------------------------------------------------------------------------------------------------
"""
from flask import Flask, request, jsonify, send_from_directory, render_template, url_for, redirect
from flask_cors import CORS
import auth
import database
import gemini_api
import os

template_dir = os.path.join('..', 'templates') #create the path to the templates folder.
app = Flask(__name__, template_folder=template_dir)
#app = Flask(__name__)  # Removed static_folder, we'll use templates and static
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"Received registration data: {data}")
    username = data.get('username')
    password = data.get('password')
    auth.register_user(username, password)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Received login data: {data}")
    username = data.get('username')
    password = data.get('password')
    if auth.verify_user(username, password):
        user_id = auth.get_user_id(username)
        print(f"Login successful for user: {username}, ID: {user_id}")
        return jsonify({'message': 'Login successful', 'user_id': user_id}), 200
    else:
        print(f"Login failed for user: {username}")
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/chat_history/<user_id>', methods=['GET'])
def get_history(user_id):
    print(f"Retrieving chat history for user ID: {user_id}")
    history = database.get_chat_history(user_id)
    return jsonify(history), 200

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    print(f"Received message data: {data}")
    user_id = data.get('user_id')
    message = data.get("message")
    response = gemini_api.get_gemini_response(message)
    database.insert_chat_message(user_id, message, response)
    return jsonify({"response": response})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if 'login' in request.form:
                user_verification = auth.verify_user(username, password)
                if user_verification:
                    user_id = auth.get_user_id(username)
                    return render_template('index.html', logged_in=True, user_id=user_id)
                else:
                    return render_template('index.html', error='Invalid credentials', logged_in=False)
            elif 'signup' in request.form:
                auth.register_user(username, password)
                return render_template('index.html', logged_in=False)
    return render_template('index.html', logged_in=False)

if __name__ == '__main__':
    app.run(debug=True)
"""

