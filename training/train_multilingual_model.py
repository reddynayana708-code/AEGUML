import os
import random
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sentence_transformers import SentenceTransformer
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / 'data'
MODELS_DIR = PROJECT_ROOT / 'models'

MODEL_PATH = MODELS_DIR / 'multilingual_model.pkl'
VEC_PATH = MODELS_DIR / 'multilingual_vectorizer.pkl'
SCALER_PATH = MODELS_DIR / 'multilingual_scaler.pkl'

# Using a multilingual BERT model
BERT_NAME = os.environ.get('BERT_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Ensure project root is on sys.path so that 'backend' package can be imported
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.preprocess import clean_text

def load_multilingual_dataset() -> Tuple[pd.Series, pd.Series]:
    """Load the multilingual dataset."""
    data_path = DATA_DIR / 'multilingual_essays.csv'
    
    if not data_path.exists():
        print(f"Multilingual dataset not found at {data_path}")
        print("Please ensure multilingual_essays.csv exists in the data directory")
        return pd.Series([]), pd.Series([])
    
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} essays from {df['language'].nunique()} languages")
    print(f"Language distribution:")
    print(df['language'].value_counts())
    
    return df['essay'], df['score']

def build_features(texts: pd.Series, bert: SentenceTransformer):
    """Build features from text using TF-IDF and BERT embeddings."""
    print("Building features...")
    
    # For multilingual, we'll skip English-specific preprocessing
    # Keep original text for BERT (multilingual)
    cleaned_texts = texts.astype(str)
    
    # TF-IDF features (lighter for multilingual)
    print("Extracting TF-IDF features...")
    tfidf = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), lowercase=False)
    X_tfidf = tfidf.fit_transform(cleaned_texts)
    print(f"TF-IDF features shape: {X_tfidf.shape}")
    
    # BERT embeddings (multilingual)
    print("Extracting BERT embeddings...")
    X_bert = bert.encode(
        texts.tolist(),
        convert_to_numpy=True,
        show_progress_bar=True,
        batch_size=16
    )
    print(f"BERT embeddings shape: {X_bert.shape}")
    
    # Combine features
    X = np.concatenate([X_tfidf.toarray(), X_bert], axis=1)
    print(f"Combined features shape: {X.shape}")
    
    # Scale features
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, tfidf, scaler

def main():
    """Main training function for multilingual model."""
    # Create models directory if it doesn't exist
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load multilingual data
    print("Loading multilingual dataset...")
    texts, y = load_multilingual_dataset()
    
    if len(texts) == 0:
        print("No data loaded. Exiting.")
        return
    
    # Load BERT model
    print(f"Loading multilingual BERT model: {BERT_NAME}")
    bert = SentenceTransformer(BERT_NAME)
    
    # Build features
    X, vectorizer, scaler = build_features(texts, bert)
    
    # Split data
    print("Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=None
    )
    
    # Train model
    print("Training multilingual model...")
    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating model...")
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    
    print(f"\nMultilingual Model Performance:")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    
    # Show some predictions
    print("\nSample predictions:")
    for i in range(min(5, len(preds))):
        print(f"Actual: {y_test.iloc[i]:.1f}, Predicted: {preds[i]:.1f}")
    
    # Save models
    print("\nSaving multilingual models...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VEC_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    print(f"\nMultilingual models saved to {MODELS_DIR}:")
    print(f"- Model: {MODEL_PATH}")
    print(f"- Vectorizer: {VEC_PATH}")
    print(f"- Scaler: {SCALER_PATH}")

if __name__ == '__main__':
    main()
