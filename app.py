from flask import Flask, request, jsonify
import pickle
import mysql.connector

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ananya@19",
    database="fake_news_project"
)

cursor = conn.cursor()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['news']
    vect = vectorizer.transform([data])

    pred = model.predict(vect)[0]
    prob = model.predict_proba(vect)[0].max() * 100

    result = "Fake" if pred == 0 else "Real"

    cursor.execute(
        "INSERT INTO history (news_text, result) VALUES (%s, %s)",
        (data, result)
    )
    conn.commit()

    return jsonify({"prediction": result, "confidence": round(prob,2)})


@app.route('/history', methods=['GET'])
def history():
    cursor.execute("SELECT * FROM history")
    return jsonify(cursor.fetchall())

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (data['username'], data['password'])
    )
    conn.commit()
    return jsonify({"msg": "User registered"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (data['username'], data['password'])
    )
    user = cursor.fetchone()

    if user:
        return jsonify({"msg": "Login success"})
    else:
        return jsonify({"msg": "Invalid credentials"})


if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)