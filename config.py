import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

RAW_PDF_FOLDER     = os.path.join(BASE_DIR, "data", "raw_pdfs")
EXTRACTED_TEXT_FOLDER = os.path.join(BASE_DIR, "data", "extracted_text")
EMBEDDINGS_FOLDER  = os.path.join(BASE_DIR, "data", "embeddings")
EMBEDDINGS_FILE    = os.path.join(EMBEDDINGS_FOLDER, "document_embeddings.pkl")

SECRET_KEY = "smartdocqa_secret_key"
DEBUG = True
HOST  = "0.0.0.0"
PORT  = 5000

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
QA_MODEL_NAME        = "distilbert-base-cased-distilled-squad"

CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 5

DATABASE_PATH = os.path.join(BASE_DIR, "database", "smartdocqa.db")

ALLOWED_EXTENSIONS = {"pdf"}


def create_directories():
    os.makedirs(RAW_PDF_FOLDER, exist_ok=True)
    os.makedirs(EXTRACTED_TEXT_FOLDER, exist_ok=True)
    os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
