# SmartDocQA — Flask Multi-Page App

AI-powered PDF Question Answering system built with Flask.

## Project Structure

```
smartdocqa/
├── app.py                    # Flask app entry point
├── config.py                 # Configuration (paths, models, settings)
├── requirements.txt
├── database/
│   └── db.py                 # SQLite database layer
├── models/
│   ├── embedding_model.py    # Sentence-transformer wrapper
│   ├── qa_model.py           # DistilBERT QA pipeline
│   └── model_loader.py       # Singleton model loader
├── pdf_processing/
│   ├── extract_text.py       # pdfplumber PDF → text
│   ├── clean_text.py         # Text cleaning pipeline
│   └── chunking.py           # Overlapping text chunker
├── retrieval/
│   ├── embedding_generator.py # Embed chunks + save/load .pkl
│   ├── similarity_search.py   # Cosine similarity search
│   └── retriever.py           # Full retrieve + answer pipeline
├── qa_engine/
│   ├── answer_extractor.py   # Multi-chunk answer extraction
│   └── query_processor.py    # Query orchestrator
├── routes/
│   ├── upload_routes.py      # GET/POST /upload
│   ├── query_routes.py       # GET / and POST /query
│   ├── api_routes.py         # REST API endpoints
│   └── history_routes.py     # /history page + delete actions
├── templates/
│   ├── base.html             # Shared layout + navbar
│   ├── index.html            # Home / Ask page
│   ├── upload.html           # Upload page
│   ├── results.html          # Answer results page
│   ├── history.html          # Query & document history
│   └── 404.html              # 404 error page
└── static/
    ├── css/style.css
    └── js/script.js
```

## Pages

| URL        | Description                          |
|------------|--------------------------------------|
| `/`        | Home — enter a question              |
| `/upload`  | Upload PDF, view uploaded documents  |
| `/query`   | (POST) Answer results page           |
| `/history` | Query history and document log       |

## REST API

| Method | URL               | Description              |
|--------|-------------------|--------------------------|
| POST   | `/api/ask`        | `{"question": "..."}` → answer |
| GET    | `/api/documents`  | List uploaded documents  |
| GET    | `/api/history`    | List past queries        |

## Setup & Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open http://localhost:5000 in your browser.

## Workflow

1. Go to **Upload** → upload a PDF
2. Wait for processing (text extraction → cleaning → chunking → embeddings)
3. Go to **Ask** → type a question → get an AI answer with source contexts
4. View **History** to see all past queries

## Bugs Fixed from Original Code

- `query_routes.py` and `api_routes.py` called undefined `Retriever()` — fixed to `DocumentRetriever`
- `upload_routes.py` checked `request.files["file"]` but form used `name="pdf_file"` — fixed to accept both
- `upload.html` and `script.js` had markdown backtick fences inside the files — removed
- `style.css` had a broken `button:hover` rule with no `{}` block — fixed
- `QueryProcessor` in `query_routes` was called but its result was never used for retrieval — fixed
