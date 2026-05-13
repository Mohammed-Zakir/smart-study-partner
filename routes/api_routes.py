from flask import Blueprint, request, jsonify

from retrieval.retriever import DocumentRetriever
from database.db import db
from config import EMBEDDINGS_FILE
import os

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/api/ask", methods=["POST"])
def ask_question():
    """REST API endpoint for question answering."""

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Field 'question' is required"}), 400

    user_query = data["question"].strip()
    if not user_query:
        return jsonify({"error": "Question cannot be empty"}), 400

    if not os.path.exists(EMBEDDINGS_FILE):
        return jsonify({"error": "No documents processed yet. Upload a PDF first."}), 404

    try:
        retriever = DocumentRetriever(EMBEDDINGS_FILE)
        result = retriever.get_answer(user_query, top_k=5)

        answer   = result.get("answer", "No answer found.")
        contexts = result.get("contexts", [])

        db.insert_query(user_query, answer)

        return jsonify({
            "question": user_query,
            "answer":   answer,
            "contexts": contexts
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/documents", methods=["GET"])
def list_documents():
    """List all uploaded documents."""
    docs = db.get_documents()
    return jsonify([
        {"id": d[0], "file_name": d[1], "file_path": d[2], "upload_date": d[3]}
        for d in docs
    ])


@api_bp.route("/api/history", methods=["GET"])
def query_history():
    """Return query history."""
    queries = db.get_queries()
    return jsonify([
        {"id": q[0], "query": q[1], "answer": q[2], "created_at": q[3]}
        for q in queries
    ])
