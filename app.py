from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask import session, redirect, url_for
from flask_cors import CORS
from newspaper import Article
import pickle
import requests
import os

app.secret_key = "fake_news_secret_key"
app = Flask(__name__)
CORS(app)

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
    try:
        news = request.form.get('news') or request.json.get('news')

        if not news:
            return jsonify({"error": "No news provided"}), 400

        vect = vectorizer.transform([news])

        pred = model.predict(vect)[0]
        prob = model.predict_proba(vect)[0].max() * 100

        result = "Fake" if pred == 0 else "Real"

        collection.insert_one({
            "news": news,
            "result": result
        })

        return jsonify({
            "prediction": result,
            "confidence": round(prob, 2)
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Server error"}), 500

# ================= HISTORY =================
@app.route('/history', methods=['GET'])
def history():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)


# ================= REGISTER =================
@app.route('/register', methods=['POST'])
def register():

    username = request.form.get('username') or request.json.get('username')
    password = request.form.get('password') or request.json.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing fields"}), 400

    existing_user = users_collection.find_one({"username": username})

    if existing_user:
        return jsonify({"msg": "User already exists"})

    users_collection.insert_one({
        "username": username,
        "password": password
    })

    return jsonify({"msg": "Registered successfully"})


# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({
        "username": username,
        "password": password
    })

    if user:

        session["user"] = username

        return jsonify({"msg": "Login success"})

    return jsonify({"msg": "Invalid credentials"})

# ================= URL CHECK =================
@app.route('/check_url', methods=['POST'])
def check_url():

    try:

        url = request.json.get('url')

        if not url:
            return jsonify({
                "prediction": "No URL provided",
                "confidence": 0
            })

        article = Article(url)
        article.download()
        article.parse()

        text = article.text

        if not text:
            return jsonify({
                "prediction": "Unable to extract article",
                "confidence": 0
            })

        vect = vectorizer.transform([text[:2000]])

        pred = model.predict(vect)[0]
        prob = model.predict_proba(vect)[0].max() * 100

        return jsonify({
            "prediction": "Fake" if pred == 0 else "Real",
            "confidence": round(prob, 2)
        })

    except Exception as e:

        print("URL CHECK ERROR:", str(e))

        return jsonify({
            "prediction": "Error analyzing article",
            "confidence": 0
        })

@app.route('/')
def home():

    if "user" not in session:
        return redirect(url_for("register_page"))

    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/dashboard')
def dashboard():
     if "user" not in session:
        return redirect(url_for("login_page"))

    return render_template("dashboard.html")
    

@app.route('/dataset')
def dataset():
    return render_template("dataset.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/login_page')
def login_page():
    return render_template("login.html")


@app.route('/register_page')
def register_page():
    return render_template("register.html")


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)