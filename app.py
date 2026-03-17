from flask import Flask,render_template,request,jsonify
import pickle

app = Flask(__name__, template_folder="TEMPLATE")

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

@app.route("/")
def home():
    return render_template("detect.html")

@app.route("/detect",methods=["POST"])
def detect():
    
    text = request.form["news"]
    
    vector = vectorizer.transform([text])
    
    prediction = model.predict(vector)[0]
    
    result = "Real" if prediction==1 else "Fake"
    
    return jsonify({"result":result})

app.run(debug=True)