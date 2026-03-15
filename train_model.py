import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# load dataset
df = pd.read_csv("neurax_projects_dataset.csv")

# select useful columns
X = df[["required_skills", "deadline_days"]]
y = df["priority"]

# convert text to numbers
le_skills = LabelEncoder()
X["required_skills"] = le_skills.fit_transform(X["required_skills"])

le_priority = LabelEncoder()
y = le_priority.fit_transform(y)

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# save model
joblib.dump(model, "priority_model.pkl")

print("Model trained and saved!")