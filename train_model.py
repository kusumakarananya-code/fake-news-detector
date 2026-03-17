import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample dataset (you can replace with your dataset)
data = {
    "text": [
        "This is real news",
        "Breaking: something fake happened",
        "Government announces new policy",
        "Fake news spreading online"
    ],
    "label": [1, 0, 1, 0]  # 1 = Real, 0 = Fake
}

df = pd.DataFrame(data)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2)

# Vectorization
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Model training
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model and vectorizer saved!")