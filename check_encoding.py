import pandas as pd

df = pd.read_csv("data/Telco-Customer-Churn.csv")

for column in df.columns:
    if str(df[column].dtype) == "str":
        print("\n" + "="*40)
        print(column)
        print(df[column].unique())