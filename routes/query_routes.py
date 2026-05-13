from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from retrieval.retriever import DocumentRetriever
from database.db import db
from config import EMBEDDINGS_FILE
import os

query_bp = Blueprint("query_bp", __name__)


# =========================
# 🔐 LOGIN CHECK
# =========================
def require_login():
    return "user" in session


# =========================
# 📊 DOCUMENT ANALYTICS
# =========================
def get_doc_analytics(documents):
    names = []
    counts = []

    for doc in documents:
        names.append(doc[1])

        # temporary usage count
        counts.append(1)

    return names, counts


# =========================
# 🏠 ASK PAGE
# =========================
@query_bp.route("/ask", methods=["GET"])
def home():

    if not require_login():
        return redirect(url_for("login"))

    documents = db.get_documents() or []

    doc_names, doc_counts = get_doc_analytics(documents)

    return render_template(
        "index.html",
        documents=documents,
        doc_names=doc_names,
        doc_counts=doc_counts,
        user=session.get("user")
    )


# =========================
# 🔍 QUERY PROCESSING
# =========================
@query_bp.route("/query", methods=["POST"])
def query_document():

    if not require_login():
        return redirect(url_for("login"))

    user_query = request.form.get("question", "").strip()

    if not user_query:
        flash("Please enter a question.", "error")
        return redirect(url_for("query_bp.home"))

    # ❗ Ensure embeddings exist
    if not os.path.exists(EMBEDDINGS_FILE):
        flash("Upload and process a PDF first.", "error")
        return redirect(url_for("upload_bp.upload_file"))

    try:

        retriever = DocumentRetriever(EMBEDDINGS_FILE)

        result = retriever.get_answer(user_query, top_k=5)

        print("Retriever Result:", result)

        answer = result.get("answer", "No answer found.")

        contexts = result.get("contexts", [])

        # 💾 Save query history
        db.insert_query(user_query, answer)

        # 📄 Reload documents
        documents = db.get_documents() or []

        doc_names, doc_counts = get_doc_analytics(documents)

        # ✅ Render on SAME PAGE
        return render_template(
            "index.html",
            question=user_query,
            answer=answer,
            contexts=contexts,
            documents=documents,
            doc_names=doc_names,
            doc_counts=doc_counts,
            user=session.get("user")
        )

    except Exception as e:

        print("Retriever Error:", e)

        flash(f"Error: {str(e)}", "error")

        return redirect(url_for("query_bp.home"))