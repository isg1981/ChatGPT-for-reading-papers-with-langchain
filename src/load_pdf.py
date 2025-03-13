import os
import glob
from flask import request
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma


import os
import glob
from flask import request
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma


class PDFLoader:
    """
    A class to handle loading PDF files, processing their content, and creating a vector database.

    Attributes:
        folder_name (str): The directory where PDF files are stored.
        db_path (str): The path where the vector database will be saved.
        embeddings: The embeddings model used for vectorizing the documents.
        retriever: The retriever object used for querying the vector database.
    """

    def __init__(self, folder_name: str, db_path: str, embeddings):
        """
        Initializes the PDFLoader with the specified folder, database path, and embeddings model.

        Args:
            folder_name (str): The directory where PDF files are stored.
            db_path (str): The path where the vector database will be saved.
            embeddings: The embeddings model used for vectorizing the documents.
        """
        self.folder_name = folder_name
        self.db_path = db_path
        self.embeddings = embeddings
        self.retriever = None

    def load_pdfs_and_create_db(self):
        """
        Loads PDF files from the specified folder, processes their content, and creates a vector database.

        Returns:
            The retriever object for querying the vector database, or an error message if the process fails.
        """
        pdf_directory = os.path.join(os.path.dirname(__file__), self.folder_name)
        print(f"Searching for PDF files in: {pdf_directory}")
        pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))
        print(f"Files found: {pdf_files}")

        if not pdf_files:
            print(f"No PDF files were found in the {self.folder_name} folder.")
            return f"No PDF files were found in the {self.folder_name} folder."

        documents = []
        for pdf_file in pdf_files:
            print(f"Processing file: {pdf_file}")
            try:
                loader = PyPDFLoader(pdf_file)
                docs = loader.load()
                print(f"Loaded documents: {len(docs)}")
                if len(docs) > 0:
                    print(f"First document: {docs[0].page_content[:100]}...")  # Print first 100 characters
                documents.extend(docs)
            except Exception as e:
                print(f"Error loading file {pdf_file}: {e}")

        if not documents:
            print("Documents could not be loaded from the PDF files.")
            return "Documents could not be loaded from the PDF files."

        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        if not docs:
            print("The documents could not be split into chunks.")
            return "The documents could not be split into chunks."

        # Check if the directory exists
        os.makedirs(self.db_path, exist_ok=True)
        print(f"Full database path: {os.path.abspath(self.db_path)}")

        try:
            print(f"Creating database at: {os.path.abspath(self.db_path)}")
            db = Chroma.from_documents(docs, embedding=self.embeddings, persist_directory=self.db_path)
            db.persist()  # Save the database to disk
            self.retriever = db.as_retriever()
            print("Database successfully created.")
            return self.retriever
        except Exception as e:
            print(f"Error creating the database: {e}")
            return f"Error creating the database: {e}"

    def upload_pdfs(self):
        """
        Handles the upload of PDF files, saves them to the specified folder, and processes them to create a vector database.

        Returns:
            A tuple containing a response message and an HTTP status code, or the retriever object if successful.
        """
        if "pdfs" not in request.files:
            return "No file part", 400

        files = request.files.getlist("pdfs")
        pdf_directory = os.path.join(os.path.dirname(__file__), self.folder_name)
        os.makedirs(pdf_directory, exist_ok=True)

        for file in files:
            if file.filename.endswith(".pdf"):
                file_path = os.path.join(pdf_directory, file.filename)
                file.save(file_path)

        global retriever
        retriever = self.load_pdfs_and_create_db()
        return retriever

    def process_existing_pdfs(self):
        """
        Processes existing PDF files in the specified folder and creates a vector database.

        Returns:
            The retriever object for querying the vector database, or None if no PDF files are found.
        """
        pdf_directory = os.path.join(os.path.dirname(__file__), self.folder_name)
        if os.path.exists(pdf_directory) and os.path.isdir(pdf_directory):
            print(f"Processing PDF existing files from folder {self.folder_name}")
            global retriever
            retriever = self.load_pdfs_and_create_db()
            return retriever
        return None