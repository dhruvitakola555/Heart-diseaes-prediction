
from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib
import numpy as np


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

CORS(app)


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_FILE = "heart_model.pkl"

model = joblib.load(MODEL_FILE)


# =========================================================
# FEATURE ORDER
# =========================================================

FEATURES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "message": "Heart Disease Prediction API is running"
    })


# =========================================================
# PREDICT
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # -------------------------------------------------
        # GET JSON
        # -------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No input data received."
            }), 400


        # -------------------------------------------------
        # CHECK ALL FEATURES
        # -------------------------------------------------

        missing = [
            feature
            for feature in FEATURES
            if feature not in data
        ]

        if missing:

            return jsonify({
                "success": False,
                "error": "Missing fields: " + ", ".join(missing)
            }), 400


        # -------------------------------------------------
        # CONVERT VALUES
        # -------------------------------------------------

        features = []

        for feature in FEATURES:

            value = float(data[feature])

            if not np.isfinite(value):

                return jsonify({
                    "success": False,
                    "error": f"Invalid value for {feature}"
                }), 400

            features.append(value)


        # -------------------------------------------------
        # CREATE MODEL INPUT
        # -------------------------------------------------

        input_data = np.array(
            features,
            dtype=float
        ).reshape(1, -1)


        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = int(
            model.predict(input_data)[0]
        )


        # -------------------------------------------------
        # PROBABILITY
        # -------------------------------------------------

        probabilities = model.predict_proba(
            input_data
        )[0]


        # Find probability belonging to class 1
        class_1_index = list(
            model.classes_
        ).index(1)

        risk_probability = probabilities[
            class_1_index
        ]

        risk_percentage = round(
            float(risk_probability * 100),
            2
        )


        # -------------------------------------------------
        # RESULT TEXT
        # -------------------------------------------------

        if prediction == 0:

            result = "Low Risk"

        else:

            result = "High Risk"


        # -------------------------------------------------
        # TERMINAL LOG
        # -------------------------------------------------

        print("\n========================================")
        print("NEW PREDICTION")
        print("========================================")

        print("Input:")
        print(
            dict(
                zip(FEATURES, features)
            )
        )

        print("Prediction:", prediction)
        print("Result:", result)
        print(
            "Class 1 probability:",
            risk_percentage,
            "%"
        )

        print("========================================\n")


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "prediction": prediction,

            "result": result,

            "risk_percentage": risk_percentage

        })


    # =====================================================
    # ERRORS
    # =====================================================

    except ValueError:

        return jsonify({

            "success": False,

            "error": "Please enter valid numeric values."

        }), 400


    except Exception as error:

        print("SERVER ERROR:", error)

        return jsonify({

            "success": False,

            "error": "Prediction failed."

        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" HEART DISEASE PREDICTION SERVER")
    print("========================================")
    print("Server: http://127.0.0.1:5000")
    print("========================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
