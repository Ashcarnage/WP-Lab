from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain_groq import ChatGroq 
import os
load_dotenv()
app = Flask(__name__)
groq_api_key = os.getenv("GROQ_API_KEY")
app.secret_key = "a_random_unique_string_12345"

# Initialize LangChain components

llm = ChatGroq(
    model_name="llama3-8b-8192",  
    temperature=0.7,             
    max_retries=3 ,
    groq_api_key =  groq_api_key  )     
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

@app.route('/')
def form():
    return render_template('form.html')  # Render the HTML form

@app.route('/process', methods=['POST'])
def process_form():
    # Collect form data
    name = request.form['name']
    gender = request.form['gender']
    interests = request.form.getlist('interest')
    message = request.form['message']

    # Store user data in session (or optionally in a database)
    session['user_data'] = {
        'name': name,
        'gender': gender,
        'interests': interests,
        'message': message
    }

    # Redirect to chat interface
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    return render_template('chatbot.html')  # Render the chat interface

@app.route('/chat_response', methods=['POST'])
def chat_response():
    user_message = request.json['message']

    # Retrieve user data from session for personalized context
    user_data = session.get('user_data', {})
    name = user_data.get('name', 'User')
    gender = user_data.get('gender', 'unknown')
    interests = ', '.join(user_data.get('interests', []))
    initial_message = user_data.get('message', '')

    # Build personalized context for LangChain
    context = f"My name is {name}. I am {gender}. My interests are {interests}. {initial_message}"
    
    # Combine context with user's current message
    full_input = f"{context}\nUser says: {user_message}"

    # Generate response using LangChain
    response = conversation.predict(input=full_input)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
