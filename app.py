from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os

app = Flask(__name__, template_folder='templets', static_folder='static')

# Load the trained model
model = None
encoders = {}

try:
    with open("models/churn_model.pkl", "rb") as file:
        model = pickle.load(file)
    print("✓ Model loaded successfully")
except FileNotFoundError:
    print("⚠️ WARNING: models/churn_model.pkl not found - app will start but predictions disabled")
    model = None

# Load the original dataset to fit encoders
try:
    df_original = pd.read_csv("data/cleaned_churn.csv")
    df_original.drop("customerID", axis=1, inplace=True)
    
    # Fit encoders for categorical variables
    for column in df_original.columns:
        if df_original[column].dtype != "int64" and df_original[column].dtype != "float64":
            encoder = LabelEncoder()
            encoder.fit(df_original[column])
            encoders[column] = encoder
    print("✓ Data and encoders loaded successfully")
except FileNotFoundError:
    print("⚠️ WARNING: data/cleaned_churn.csv not found - encoders will be empty")
    encoders = {}

# Feature order (excluding customerID and Churn)
feature_order = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
    'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
    'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
    'MonthlyCharges', 'TotalCharges'
]

# Dashboard statistics
STATS = {
    "accuracy": 96.37,
    "dataset_size": 69880,
    "features": 19,
    "algorithm": "Random Forest"
}


@app.route("/")
def home():
    return render_template("home.html", stats=STATS)


@app.route("/test")
def test():
    return "✓ Flask app is running!", 200


@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    """Handle both GET (show form) and POST (process prediction)"""

    if request.method == "GET":
        # Show the prediction form
        return render_template("predict.html")

    elif request.method == "POST":
        # Process the prediction
        print("\n" + "=" * 60)
        print("PREDICTION REQUEST RECEIVED")
        print("=" * 60)

        if not model:
            return render_template(
                "predict.html",
                error="Model not loaded. Please upload models/churn_model.pkl to Render.",
            ), 503

        try:
            # Extract and validate form data
            user_data = {}
            print("\nExtracting form data...")

            for feature in feature_order:
                if feature not in request.form:
                    raise ValueError(f"Missing required field: {feature}")

                value = request.form[feature]
                print(f"  {feature}: {value}")

                # Convert to appropriate type
                if feature in encoders:
                    # Categorical - will be encoded
                    user_data[feature] = value
                else:
                    # Numeric
                    if feature == 'SeniorCitizen':
                        user_data[feature] = int(value)
                    else:
                        user_data[feature] = float(value)

            print("\nForm data validated successfully")

            # Create feature array with encoding
            print("\nEncoding categorical features...")
            features = []
            for feature in feature_order:
                if feature in encoders:
                    # Encode categorical feature
                    encoded_value = encoders[feature].transform([user_data[feature]])[0]
                    print(f"  {feature}: '{user_data[feature]}' -> {encoded_value}")
                    features.append(encoded_value)
                else:
                    # Use numeric value as is
                    print(f"  {feature}: {user_data[feature]} (numeric)")
                    features.append(user_data[feature])

            # Reshape for prediction
            features_array = np.array(features).reshape(1, -1)
            print(f"\nFeature array shape: {features_array.shape}")
            print(f"Feature array: {features_array}")

            # Make prediction and get probability
            print("\nRunning model prediction...")
            prediction = model.predict(features_array)[0]
            confidence_scores = model.predict_proba(features_array)[0]

            print(f"Prediction: {prediction}")
            print(f"Probability scores: {confidence_scores}")

            # Get confidence percentage (higher probability)
            confidence = max(confidence_scores) * 100

            # Determine result message
            if prediction == 1:
                result_message = "Customer Likely To Churn"
                result_class = "churn"
                print("Result: CHURN DETECTED")
            else:
                result_message = "Customer Not Likely To Churn"
                result_class = "no-churn"
                print("Result: NO CHURN")

            print(f"Confidence: {confidence:.2f}%")
            print("=" * 60)

            # Pass data to result page
            return render_template(
                "result.html",
                result=result_message,
                result_class=result_class,
                confidence=round(confidence, 2),
                prediction=int(prediction),
            )

        except ValueError as e:
            print(f"\nVALIDATION ERROR: {str(e)}")
            print("=" * 60)
            return (
                render_template(
                    "predict.html",
                    error=f"Validation Error: {str(e)}",
                ),
                400,
            )

        except Exception as e:
            print(f"\nERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            print("=" * 60)
            return (
                render_template(
                    "predict.html",
                    error=f"Prediction Error: {str(e)}",
                ),
                500,
            )


@app.route("/about")
def about():
    return render_template("about.html", stats=STATS)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("STARTING CUSTOMER CHURN PREDICTION SYSTEM")
    print("=" * 60)
    print(f"Model loaded: {'✓ YES' if model else '✗ NO (missing)'}")
    print(f"Number of encoders: {len(encoders)}")
    print(f"Feature order: {len(feature_order)} features")
    print("=" * 60 + "\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)