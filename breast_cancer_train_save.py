# ✅ Step 1: Import Required Libraries
import pandas as pd
import joblib
import os
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report

# ✅ Step 2: Load the Breast Cancer Dataset
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# ✅ Step 3: Split into Features and Target
X = df.drop('target', axis=1)
y = df['target']

# ✅ Step 4: Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ✅ Step 5: Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ✅ Step 6: Train the Model (Using Gradient Boosting)
model = GradientBoostingClassifier()
model.fit(X_train_scaled, y_train)

# ✅ Step 7: Evaluate the Model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"📊 Breast Cancer Model Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))

# ✅ Step 8: Save Model and Scaler
if not os.path.exists("models"):
    os.makedirs("models")

joblib.dump(model, "models/breast_cancer_model.pkl")
joblib.dump(scaler, "models/breast_cancer_scaler.pkl")

print("✅ Breast cancer model and scaler saved successfully.")
