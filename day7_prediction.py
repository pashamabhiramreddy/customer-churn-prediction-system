import pickle

with open("models/churn_model.pkl", "rb") as file:
    model = pickle.load(file)

sample = [[
    1, 0, 1, 0, 24,
    1, 1, 1, 0, 1,
    1, 0, 1, 1, 0,
    1, 2, 70.5, 1500.0
]]

prediction = model.predict(sample)

print("Prediction:", prediction)