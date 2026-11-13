import pickle
import pandas as pd

feature_names = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
    'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
    'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
    'MonthlyCharges', 'TotalCharges'
]

print("Loading trained churn model...")
with open("models/churn_model.pkl", "rb") as file:
    model = pickle.load(file)
print("Model loaded successfully.")

sample_row = [
    1, 0, 1, 0, 24,
    1, 1, 1, 0, 1,
    1, 0, 1, 1, 0,
    1, 2, 70.5, 1500.0
]

sample = pd.DataFrame([sample_row], columns=feature_names)
print("Sample input:")
print(sample)

prediction = model.predict(sample)
print("Prediction:", prediction)
print("Customer likely to churn" if prediction[0] == 1 else "Customer not likely to churn")