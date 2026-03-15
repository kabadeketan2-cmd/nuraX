import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# load dataset
df = pd.read_csv("neurax_project_history_dataset.csv")

# target column
y = df["success_score"]

# features
X = df.drop("success_score", axis=1)

# convert text columns to numbers
le = LabelEncoder()
for col in X.select_dtypes(include="object").columns:
    X[col] = le.fit_transform(X[col])

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# save model
joblib.dump(model, "history_model.pkl")

print("Project history model trained successfully!")