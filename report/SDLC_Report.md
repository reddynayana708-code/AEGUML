# SDLC Report: Automated Essay Grading using Machine Learning

## 1. Requirement Analysis
- Objective, functional, and non-functional requirements as specified.

## 2. System Design
- Client–Server with Streamlit frontend and Flask backend. TF-IDF + BERT + Ridge.
- Sequence: Preprocess → Features → Predict → Feedback.

## 3. Implementation
- Training script with synthetic fallback dataset.
- Backend API with `/grade` and `/health`.
- Frontend Streamlit UI.

## 4. Testing
- Unit tests for preprocessing and API shape (see `tests/`).

## 5. Deployment
- Local instructions in README. Cloud options: Render/Railway/Spaces.

## 6. Maintenance
- Version control, dataset updates, model retraining.

## 7. Advanced Features
- Grammar via LanguageTool, multilingual via env model, plagiarism ready via cosine similarity extension.
