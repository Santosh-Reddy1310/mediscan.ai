import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import accuracy_score
import joblib
import os

# Load dataset
df = pd.read_csv("D:/10 Weeks 10 Projects/mediscan_ai/diabetes.csv")

X = df.drop(columns='Outcome', axis=1)
Y = df['Outcome']

# Standardize
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

# Split
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, stratify=Y, random_state=2)

# Train model
model = svm.SVC(kernel='linear', class_weight='balanced')
model.fit(X_train, Y_train)

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Save
joblib.dump(model, os.path.join(MODELS_DIR, "diabetes_model.pkl"))
joblib.dump(scaler, os.path.join(MODELS_DIR, "diabetes_scaler.pkl"))
