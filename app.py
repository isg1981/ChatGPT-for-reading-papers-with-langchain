import os
from flask import Flask, render_template
from flask_cors import CORS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
from src.load_pdf import PDFLoader
from src.question import ask_question
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the app
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Embeddings and database configuration
embeddings = OpenAIEmbeddings()
db_path = "emb"
chat = ChatOpenAI()
retriever = None  # Will be initialized after loading documents
folder_name = "data"

# Memory configuration
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="question",  
    output_key="answer"    
)

# Initialize PDFLoader instance
pdf_loader = PDFLoader(folder_name="../"+folder_name, db_path=db_path, embeddings=embeddings)

@app.route("/"+folder_name, methods=["POST"])
def upload_pdfs_route():
    """
    Handles the upload of PDF files and processes them to create a vector database.

    Returns:
        The response from the PDFLoader's upload_pdfs method.
    """
    # Call the upload_pdfs function from the pdf_loader instance.
    return pdf_loader.upload_pdfs()

@app.route("/ask", methods=["POST"])
def ask_question_route():
    """
    Handles user questions by querying the vector database using a conversational retrieval chain.

    Returns:
        The response from the ask_question function.
    """
    global retriever, chat, memory
    return ask_question(retriever=retriever, chat=chat, memory=memory)

@app.route("/")
def home():
    """
    Renders the home page of the application.

    Returns:
        The rendered HTML template for the home page.
    """
    return render_template("index.html")

def process_existing_pdfs():
    """
    Processes existing PDF files in the specified folder and creates a vector database.

    This function is called when the application starts to ensure existing PDFs are processed.
    """
    pdf_directory = os.path.join(os.path.dirname(__file__), folder_name)
    if os.path.exists(pdf_directory) and os.path.isdir(pdf_directory):
        print("Processing PDF existing files from folder data")
        global retriever
        retriever = pdf_loader.load_pdfs_and_create_db()

# Process existing PDFs when the application starts
process_existing_pdfs()

if __name__ == "__main__":
    """
    Entry point of the application. Starts the Flask development server.
    """
    app.run(debug=True)