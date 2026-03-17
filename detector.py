import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

fake = pd.read_csv(r"C:\Users\anany\DATASET\Fake.csv")
true = pd.read_csv(r"C:\Users\anany\DATASET\True.csv")

fake["label"] = 0
true["label"] = 1

data = pd.concat([fake, true])

X = data["text"]
y = data["label"]

vectorizer = TfidfVectorizer(stop_words="english")

X_vector = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vector, y, test_size=0.2)

model = LogisticRegression()

model.fit(X_train, y_train)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained successfully")