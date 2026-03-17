import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load datasets
fake = pd.read_csv("dataset/Fake.csv")
true = pd.read_csv("dataset/True.csv")

# Add labels
fake["label"] = 0
true["label"] = 1

# Combine datasets
data = pd.concat([fake, true])

# Use text column (important!)
X = data["text"]
y = data["label"]

# Vectorization
vectorizer = TfidfVectorizer()
X_vector = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vector, y)

# Save files
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained and saved!")