import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

# Create a simple model
model = RandomForestRegressor(n_estimators=10)
X_dummy = np.random.rand(10, 5)  # Dummy data
y_dummy = np.random.rand(10) * 10  # Dummy scores
model.fit(X_dummy, y_dummy)

# Create a vectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(["dummy text"] * 10)  # Dummy text data

# Create a scaler
scaler = StandardScaler()
scaler.fit(X_dummy)  # Fit with dummy data

# Save all files
import os
os.makedirs('models', exist_ok=True)

joblib.dump(model, 'models/model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print("Successfully created model files in the 'models' directory:")
print("- model.pkl")
print("- vectorizer.pkl")
print("- scaler.pkl")