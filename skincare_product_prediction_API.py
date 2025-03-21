from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import os
import pickle

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the model
MODEL_PATH = "models/btl_model_20250320_2034_matched-conc_P442990_purchases.pkl"

model = None
try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model is not loaded. Check logs for issues."}), 500

    try:
        data = request.get_json()

        required_features = [
            "product_id", "total_concentration", "author_id", "product_name",
            "brand_name", "submission_time", "rating"
        ]

        missing_features = [f for f in required_features if f not in data]
        if missing_features:
            return jsonify({"error": f"Missing required inputs: {', '.join(missing_features)}"}), 400

        try:
            product_id = str(data["product_id"])
            total_concentration = str(data["total_concentration"])
            author_id = str(data["author_id"])
            product_name = str(data["product_name"])
            brand_name = str(data["brand_name"])
            submission_time = str(data["submission_time"])
            rating = int(data["rating"])

        except ValueError as ve:
            return jsonify({"error": f"Invalid data type: {str(ve)}"}), 400

        features = [product_id, total_concentration, author_id, product_name, brand_name, submission_time, rating]

        prediction = model.predict([features])
        probabilities = model.predict_proba([features])[0]

        response = {
            "target": int(prediction[0]),
            "Probabilities": {
                "Would not buy P442990": round(probabilities[0], 4),
                "Would buy P442990": round(probabilities[1], 4)
            }
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))