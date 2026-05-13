import os
from flask import Blueprint, request, redirect, url_for, render_template, flash

from database.db import db
from pdf_processing.extract_text import PDFTextExtractor
from pdf_processing.clean_text import TextCleaner
from pdf_processing.chunking import TextChunker
from retrieval.embedding_generator import EmbeddingGenerator
from config import RAW_PDF_FOLDER, EMBEDDINGS_FILE

upload_bp = Blueprint("upload_bp", __name__)


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    """Upload and process a PDF document."""

    if request.method == "POST":
        # Support both 'file' and 'pdf_file' field names
        file = request.files.get("file") or request.files.get("pdf_file")

        if not file or file.filename == "":
            flash("No file selected. Please choose a PDF.", "error")
            return redirect(request.url)

        if not file.filename.lower().endswith(".pdf"):
            flash("Only PDF files are allowed.", "error")
            return redirect(request.url)

        try:
            # Save PDF
            file_path = os.path.join(RAW_PDF_FOLDER, file.filename)
            file.save(file_path)

            # Save record to DB
            db.insert_document(file.filename, file_path)

            # --- Text Extraction ---
            extractor = PDFTextExtractor()
            text = extractor.extract_text_from_pdf(file_path)

            if not text.strip():
                flash("Could not extract text from this PDF.", "error")
                return redirect(request.url)

            # --- Text Cleaning ---
            cleaner = TextCleaner()
            clean_text = cleaner.clean_text(text)

            # --- Text Chunking ---
            chunker = TextChunker()
            chunks = chunker.split_text(clean_text)

            # --- Embedding Generation ---
            embedder = EmbeddingGenerator()
            embeddings = embedder.generate_embeddings(chunks)
            embedder.save_embeddings(embeddings, chunks, EMBEDDINGS_FILE)

            flash(f'"{file.filename}" uploaded and processed successfully!', "success")
            return redirect(url_for("upload_bp.upload_file"))

        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            return redirect(request.url)

    # GET: show list of uploaded documents
    documents = db.get_documents()
    return render_template("upload.html", documents=documents)
