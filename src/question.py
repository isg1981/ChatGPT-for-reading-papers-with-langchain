from flask import request, jsonify
from flask_cors import CORS
from langchain.chains import ConversationalRetrievalChain


def ask_question(retriever, chat, memory):
    """
    Handles user questions by querying the vector database using a conversational retrieval chain.

    Args:
        retriever: The retriever object used to query the vector database.
        chat: The language model used for generating responses.
        memory: The memory object used to store conversation history.

    Returns:
        A JSON response containing the generated answer or an error message if the request is invalid.
    """
    if retriever is None:
        print("Error: No documents available. Please upload PDFs first.")
        return jsonify({"error": "No documents available. Please upload PDFs first."}), 400
    
    data = request.get_json()
    if not data or "question" not in data:
        print("Error: Invalid request payload. 'question' field is missing.")
        return jsonify({"error": "Invalid request payload. 'question' field is missing."}), 400
    
    question = data.get("question", "")
    print(f"Received question: {question}")
    
    # Configure the conversation chain without 'input_key' and 'output_key'.
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=retriever,
        memory=memory
    )
    
    # Run the chain with the question.
    result = chain({"question": question})
    answer = result.get("answer", "Could not generate a response.")
    
    return jsonify({"answer": answer})