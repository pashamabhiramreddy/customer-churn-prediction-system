import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/cleaned_churn.csv")

df.drop("customerID", axis=1, inplace=True)

encoder = LabelEncoder()

for column in df.columns:
    if df[column].dtype != "int64" and df[column].dtype != "float64":
        df[column] = encoder.fit_transform(df[column])

print(df.head())

print("\nData Types:")
print(df.dtypes)

# Features and Target
X = df.drop("Churn", axis=1)
y = df["Churn"]

print("\nFeatures Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Set Shape:")
print(X_train.shape)

print("\nTesting Set Shape:")
print(X_test.shape)