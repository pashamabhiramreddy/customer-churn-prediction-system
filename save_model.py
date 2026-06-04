import pandas as pd
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("data/cleaned_churn.csv")

# Remove customerID
df.drop("customerID", axis=1, inplace=True)

# Encode categorical columns
encoder = LabelEncoder()

for column in df.columns:
    if df[column].dtype != "int64" and df[column].dtype != "float64":
        df[column] = encoder.fit_transform(df[column])

# Features and Target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

# Save model
with open("models/churn_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model Saved Successfully!")