import pandas as pd

# Load dataset
df = pd.read_csv("data/Telco-Customer-Churn.csv")

print("Dataset Loaded Successfully!\n")

# Dataset Shape
print("Dataset Shape:")
print(df.shape)

# First 5 Rows
print("\nFirst 5 Rows:")
print(df.head())

# Column Names
print("\nColumn Names:")
print(df.columns)

# Dataset Information
print("\nDataset Info:")
df.info()

# Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Churn Counts
print("\nChurn Counts:")
print(df["Churn"].value_counts())

# Statistical Summary
print("\nStatistical Summary:")
print(df.describe())

print("\nTotalCharges Data Type:")
print(type(df["TotalCharges"][0]))

print("\nFirst 5 TotalCharges Values:")
print(df["TotalCharges"].head())

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\nNew Data Type:")
print(df["TotalCharges"].dtype)

print("\nMissing Values After Conversion:")
print(df["TotalCharges"].isnull().sum())

print(df[df["TotalCharges"].isnull()])

print(df[df["TotalCharges"].isnull()][["tenure", "MonthlyCharges", "TotalCharges"]])

df = df.dropna()

print("\nShape After Cleaning:")
print(df.shape)

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv("data/cleaned_churn.csv", index=False)

print("\nCleaned dataset saved successfully!")