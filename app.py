from flask import Flask, request, jsonify
from pymongo import MongoClient
import pickle
import requests
import os

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb+srv://kusumakarananya_db_user:ananya1234@cluster0.uqyqiay.mongodb.net/?retryWrites=true&w=majority")
db = client["fake_news_project"]
collection = db["history"]
users_collection = db["users"]

# Load ML Model
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# ================= PREDICT =================
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['news']
    vect = vectorizer.transform([data])

    pred = model.predict(vect)[0]
    prob = model.predict_proba(vect)[0].max() * 100

    result = "Fake" if pred == 0 else "Real"

    # Save to MongoDB
    collection.insert_one({
        "news": data,
        "result": result
    })

    return jsonify({
        "prediction": result,
        "confidence": round(prob, 2)
    })


# ================= HISTORY =================
@app.route('/history', methods=['GET'])
def history():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)


# ================= REGISTER =================
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    users_collection.insert_one({
        "username": data['username'],
        "password": data['password']
    })

    return jsonify({"msg": "User registered"})


# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = users_collection.find_one({
        "username": data['username'],
        "password": data['password']
    })

    if user:
        return jsonify({"msg": "Login success"})
    else:
        return jsonify({"msg": "Invalid credentials"})


# ================= URL CHECK =================
@app.route('/check_url', methods=['POST'])
def check_url():
    url = request.json['url']

    response = requests.get(url)
    text = response.text[:1000]

    vect = vectorizer.transform([text])
    pred = model.predict(vect)[0]

    return jsonify({
        "prediction": "Fake" if pred == 0 else "Real"
    })


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)