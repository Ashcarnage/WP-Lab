from flask import Flask, request, jsonify, render_template
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import json
import os
from langchain_groq import ChatGroq 
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

# Initialize LangChain's OpenAI LLM and other components
openai_api_key = os.getenv("GROQ_API_KEY")
chat_model = ChatGroq(
    model_name="llama3-8b-8192",  
    temperature=0.7,             
    max_retries=3    )            

# Directory to save the documents (ensure it exists)
os.makedirs('saved_documents', exist_ok=True)

@app.route('/processForm', methods=['POST'])
def process_form():
    form_data = request.get_json()

    # Create the document from form data
    doc_content = f"Student Name: {form_data['name']}\nDate of Birth: {form_data['dob']}\nGender: {form_data['gender']}\nCourse: {form_data['course']}"
    
    # Save document to file (for later use in LangChain)
    doc_filename = f"saved_documents/{form_data['name']}_{form_data['dob']}.txt"
    with open(doc_filename, 'w') as file:
        file.write(doc_content)
    
    # Create Document object for LangChain
    document = Document(page_content=doc_content)

    # Index document using FAISS (for RAG - Retrieval-Augmented Generation)
    embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-large")
    vector_store = FAISS.from_documents([document], embeddings)

    # Save the vector store for later use
    vector_store.save_local(f"saved_documents/{form_data['name']}_faiss")

    session_id = f"{form_data['name']}_{form_data['dob']}"
    
    return jsonify({"sessionId": session_id})


@app.route('/chatbot', methods=['GET'])
def chatbot_page():
    session_id = request.args.get('session')

    return render_template('chatbot.html', session_id=session_id)


@app.route('/getChatbotResponse', methods=['GET'])
def get_chatbot_response():
    session_id = request.args.get('session')
    user_message = request.args.get('message')

    # Load the document's vector store from session
    vector_store = FAISS.load_local(f"saved_documents/{session_id}_faiss")
    
    # Query the vector store for relevant information
    docs = vector_store.similarity_search(user_message)
    doc_contents = "\n".join([doc.page_content for doc in docs])
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the context below to answer the user's question."),
        ("system", f"Context: {doc_contents}"),
        ("human", "{user_query}")
    ])
    llm = ({"doc_contents":itemgetter("contents"),"user_query":itemgetter("query")}|chat_prompt|chat_model|StringOutputParser())
    rellm.invoke({"query":user_message,"contents":[doc.page_content for doc in docs]})
    # Generate a response based on the retrieved documents using LangChain
    response = chat_model.chat([doc.page_content for doc in docs])
    
    return jsonify({'botResponse': response})


if __name__ == '__main__':
    app.run(debug=True)
