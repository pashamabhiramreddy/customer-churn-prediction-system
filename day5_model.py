import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv("data/cleaned_churn.csv")

# Remove customerID
df.drop("customerID", axis=1, inplace=True)

# Encode categorical columns
encoder = LabelEncoder()

for column in df.columns:
    if df[column].dtype != "int64" and df[column].dtype != "float64":
        df[column] = encoder.fit_transform(df[column])

# Split features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LogisticRegression(max_iter=5000)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:")
print(round(accuracy * 100, 2), "%")

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# Predictions
y_pred = model.predict(X_test)

print("Accuracy:")
print(round(accuracy_score(y_test, y_pred) * 100, 2), "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))