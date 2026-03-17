import random

templates = [
"Breaking: {topic} situation gets worse as experts warn public.",
"Shocking development in {topic} leaves citizens surprised.",
"Government secretly planning new policy regarding {topic}.",
"Scientists reveal hidden truth about {topic}."
]

def generate_news(topic):
    article = random.choice(templates).format(topic=topic)
    return article

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Example training data
texts = ["This is real news", "Fake news example"]
labels = [1, 0]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

pickle.dump(model, open("model.pkl","wb"))
pickle.dump(vectorizer, open("vectorizer.pkl","wb"))