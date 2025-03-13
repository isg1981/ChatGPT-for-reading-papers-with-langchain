# PDF Processing and Question-Answering System

This project is a Flask-based web application that allows users to upload PDF files, process their content, and interact with them through a conversational question-answering system. The application uses LangChain for document processing, OpenAI embeddings for vectorization, and Chroma as a vector database.

The idea of this project is to interact with scientific papers in PDF format or any other document locally. For this, the OpenAI model API was used, but by modifying the code, a different model could be used. The OpenAI model was chosen because it is the most well-known. Some Dark Matter papers in PDF format are uploaded as an example, allowing interaction with them.

## Features

- **PDF Upload and Processing**: Users can upload PDF files, which are processed and stored in a vector database.
- **Conversational Q&A**: Users can ask questions about the content of the uploaded PDFs, and the system generates answers using a conversational retrieval chain.
- **Persistent Storage**: The vector database is persisted to disk, allowing the system to retain processed documents across sessions.

## Technologies Used

- **Flask**: A lightweight web framework for Python.
- **LangChain**: A framework for building applications with large language models.
- **OpenAI Embeddings**: Used for generating vector representations of text.
- **Chroma**: A vector database for storing and querying document embeddings.
- **Flask-CORS**: Enables Cross-Origin Resource Sharing (CORS) for the Flask app.

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/isg1981/ChatGPT-for-reading-papers-with-langchain.git
   cd ChatGPT-for-reading-papers-with-langchain

2. **Set up a virtual environment**
   ```bash
   python -m .venv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set up environment variables**
   - Create a .env file in the root directory.
   - Add your OpenAI API key to the .env file:

         OPENAI_API_KEY=your-api-key-here

5. **Run the Application**
   python app.py

6. **Access the application**
   Open your browser and navigate to http://127.0.0.1:5000.


## Project Structure

project/
│
├── app.py               # Main Flask application
├── src/
│   ├── load_pdf.py      # PDF processing and database creation
│   └── question.py      # Question-answering functionality
├── templates/
│   └── index.html       # HTML template for the home page
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation