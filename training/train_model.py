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

MODEL_PATH = MODELS_DIR / 'model.pkl'
VEC_PATH = MODELS_DIR / 'vectorizer.pkl'
SCALER_PATH = MODELS_DIR / 'scaler.pkl'

# Using a multilingual BERT model
BERT_NAME = os.environ.get('BERT_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Ensure project root is on sys.path so that 'backend' package can be imported
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.preprocess import clean_text

def maybe_create_synthetic_dataset(path: Path, n: int = 300):
    """Create a synthetic dataset if it doesn't exist."""
    if path.exists():
        return
        
    print("Creating synthetic dataset...")
    topics = [
        'The impact of technology on education',
        'Climate change and its global effects',
        'The importance of mental health awareness',
        'The benefits and risks of artificial intelligence',
        'How sports shape character and teamwork'
    ]
    
    records = []
    for _ in range(n):
        topic = random.choice(topics)
        length = random.randint(80, 400)
        quality = random.random() * 10  # Score between 0 and 10
        
        # Generate some realistic-looking text
        essay = f"This is a {' '.join([topic.lower()] * 5)}. " * (length // 30)
        essay = essay[:length].capitalize() + "."
        
        records.append({
            'essay': essay,
            'score': quality
        })
    
    df = pd.DataFrame(records)
    df.to_csv(path, index=False)
    print(f"Created synthetic dataset with {len(df)} samples at {path}")

def load_dataset() -> Tuple[pd.Series, pd.Series]:
    """Load the dataset, creating a synthetic one if needed."""
    data_path = DATA_DIR / 'essays.csv'
    maybe_create_synthetic_dataset(data_path)
    
    df = pd.read_csv(data_path)
    return df['essay'], df['score']

def build_features(texts: pd.Series, bert: SentenceTransformer):
    """Build features from text using TF-IDF and BERT embeddings."""
    print("Building features...")
    
    # Clean the text
    cleaned_texts = texts.apply(clean_text)
    
    # TF-IDF features
    print("Extracting TF-IDF features...")
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_tfidf = tfidf.fit_transform(cleaned_texts)
    print(f"TF-IDF features shape: {X_tfidf.shape}")
    
    # BERT embeddings
    print("Extracting BERT embeddings...")
    X_bert = bert.encode(
        texts.tolist(),
        convert_to_numpy=True,
        show_progress_bar=True,
        batch_size=32
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
    """Main training function."""
    # Create models directory if it doesn't exist
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("Loading dataset...")
    texts, y = load_dataset()
    
    # Load BERT model
    print(f"Loading BERT model: {BERT_NAME}")
    bert = SentenceTransformer(BERT_NAME)
    
    # Build features
    X, vectorizer, scaler = build_features(texts, bert)
    
    # Split data
    print("Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    print("Training model...")
    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating model...")
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    
    print(f"\nModel Performance:")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    
    # Save models
    print("\nSaving models...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VEC_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    print(f"\nModels saved to {MODELS_DIR}:")
    print(f"- Model: {MODEL_PATH}")
    print(f"- Vectorizer: {VEC_PATH}")
    print(f"- Scaler: {SCALER_PATH}")

if __name__ == '__main__':
    main()