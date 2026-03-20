from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import joblib
import pandas as pd
import os

app = Flask(__name__, static_folder='landing_page')

# Load models safely
try:
    model = joblib.load("models/logistic_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    kmeans = joblib.load("models/kmeans_model.pkl")
    feature_names = joblib.load("models/feature_names.pkl")
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        raw = {
            "Age": int(data.get("age", 25)),
            "Gender": data.get("gender"),
            "Hormonal Changes": data.get("hormonal"),
            "Family History": data.get("family_history"),
            "Body Weight": data.get("body_weight"),
            "Calcium Intake": data.get("calcium"),
            "Vitamin D Intake": data.get("vitamin_d"),
            "Physical Activity": data.get("physical"),
            "Smoking": data.get("smoking"),
            "Prior Fractures": data.get("prior_fracture"),
        }
        
        input_df = pd.DataFrame([raw])
        input_encoded = pd.get_dummies(input_df)
        input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)
        
        input_scaled = scaler.transform(input_encoded)
        prediction = model.predict(input_scaled)[0]
        cluster = kmeans.predict(input_scaled)[0]
        proba = model.predict_proba(input_scaled)[0]
        risk_pct = round(proba[1] * 100, 1)
        
        return jsonify({
            "status": "success",
            "prediction": int(prediction),
            "cluster": int(cluster),
            "risk_pct": float(risk_pct),
            "probability_low": float(proba[0]),
            "probability_high": float(proba[1])
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    print("Serving from folder:", os.path.abspath(app.static_folder))
    app.run(debug=True, port=8000)
