# Automated Essay Grading using Machine Learning

End-to-end project with a Flask backend API and Streamlit frontend. Trains a Ridge Regression model on TF-IDF + BERT embeddings and provides grammar, readability, and sentiment feedback.

## Quick Start

1. Create a Python 3.10+ environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Add your own dataset to `data/essays.csv` with columns `essay,score`. Otherwise, a synthetic dataset will be generated during training.

4. Train the model:

```bash
python training/train_model.py
```

This will create artifacts in `models/`.

5. Run the backend API (port 8000):

```bash
python backend/app.py
```

6. Run the Streamlit frontend (port 8501):

```bash
streamlit run frontend/app.py
```

Open http://localhost:8501 and grade an essay.

## API

POST /grade

Input:
```json
{"essay": "your essay text"}
```

Response:
```json
{
  "predicted_score": 8.5,
  "feedback": "...",
  "readability": {...},
  "sentiment": {...},
  "grammar": {"issue_count": 0, "issues": []}
}
```

## Notes
- First run will download a SentenceTransformer model (~80MB).
- If LanguageTool is not available, grammar feedback will gracefully degrade.
- Set `BERT_MODEL` env var to switch to a multilingual model like `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

## Testing

Run unit tests (basic):

```bash
pytest -q
```

## SDLC Report
See `report/SDLC_Report.md` (export to PDF as needed).
