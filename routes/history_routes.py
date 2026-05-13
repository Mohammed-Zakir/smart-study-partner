from flask import Blueprint, render_template, redirect, url_for, flash
from database.db import db

history_bp = Blueprint("history_bp", __name__)


@history_bp.route("/history")
def history():
    """Show query history and uploaded documents."""
    queries   = db.get_queries()
    documents = db.get_documents()
    return render_template("history.html", queries=queries, documents=documents)


@history_bp.route("/history/delete/query/<int:query_id>", methods=["POST"])
def delete_query(query_id):
    db.delete_query(query_id)
    flash("Query deleted.", "success")
    return redirect(url_for("history_bp.history"))


@history_bp.route("/history/delete/document/<int:doc_id>", methods=["POST"])
def delete_document(doc_id):
    db.delete_document(doc_id)
    flash("Document record deleted.", "success")
    return redirect(url_for("history_bp.history"))
