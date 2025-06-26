import joblib
import numpy as np

def load_model(model_path, scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_disease(model, scaler, features: list):
    input_data = np.array(features).reshape(1, -1)
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    return prediction
