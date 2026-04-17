import os
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "quiz-pro-key-2026")

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_leaderboard(data):
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError:
        pass

QUESTIONS = [
    {"question": "Who is GOAT of Football?", "options": ["Kustiyar Ronaldo", "Pele", "Hand of GOD", "Leo Messi"], "answer": "Leo Messi", "category": "Sports"},
    {"question": "Who is the father of Real Madrid?", "options": ["Raphinha", "Rice", "Messi", "Lamin Yamal"], "answer": "Messi", "category": "Football"},
    {"question": "Who is the best All-Rounder in cricket history?", "options": ["Kapil Dev", "Shakib Al Hasan", "Imran Khan", "Jacques Kallis"], "answer": "Shakib Al Hasan", "category": "Cricket"},
    {"question": "Which country won the ICC World Cup 2019?", "options": ["New Zealand", "South Africa", "England", "Australia"], "answer": "England", "category": "Cricket"},
    {"question": "Who has the highest runs in ODI cricket?", "options": ["Ricky Ponting", "Brian Lara", "Sachin Tendulkar", "Kumar Sangakkara"], "answer": "Sachin Tendulkar", "category": "Cricket"},
    {"question": "Who is the fastest bowler in cricket history?", "options": ["Brett Lee", "Wasim Akram", "Mitchell Starc", "Shoaib Akhtar"], "answer": "Shoaib Akhtar", "category": "Cricket"},
    {"question": "Which team has won the most ICC World Cups?", "options": ["Pakistan", "Australia", "England", "West Indies"], "answer": "Australia", "category": "Cricket"},
    {"question": "Which country won FIFA World Cup 2022?", "options": ["France", "Brazil", "Argentina", "Germany"], "answer": "Argentina", "category": "Football"},
    {"question": "Who has the most Ballon d'Or?", "options": ["Zidane", "Messi", "Kaka", "Ronaldinho"], "answer": "Messi", "category": "Football"},
    {"question": "Which club is known as Red Devils?", "options": ["Liverpool", "Chelsea", "Manchester United", "Arsenal"], "answer": "Manchester United", "category": "Football"},
    {"question": "Which club has the most Champions League titles?", "options": ["Bayern Munich", "Liverpool", "Real Madrid", "Barcelona"], "answer": "Real Madrid", "category": "Football"},
    {"question": "Who is known as Brazilian magician?", "options": ["Kaka", "Ronaldinho", "Ronaldo Nazario", "Neymar"], "answer": "Ronaldinho", "category": "Football"},
    {"question": "Which country is famous for Samba football?", "options": ["Spain", "Brazil", "Portugal", "Argentina"], "answer": "Brazil", "category": "Football"},
    {"question": "Who won Golden Boot in World Cup 2018?", "options": ["Griezmann", "Modric", "Kane", "Mbappe"], "answer": "Kane", "category": "Football"},
    {"question": "Who is the best captain in cricket history?", "options": ["Ricky Ponting", "Clive Lloyd", "MS Dhoni", "Graeme Smith"], "answer": "MS Dhoni", "category": "Cricket"},
    {"question": "Which player is called Mr. 360 in cricket?", "options": ["Steve Smith", "Maxwell", "AB de Villiers", "Buttler"], "answer": "AB de Villiers", "category": "Cricket"},
    {"question": "Which country invented cricket?", "options": ["Australia", "Pakistan", "England", "South Africa"], "answer": "England", "category": "Cricket"},
    {"question": "Who is the greatest football playmaker?", "options": ["Xavi", "Messi", "Modric", "Iniesta"], "answer": "Messi", "category": "Football"},
    {"question": "Which team is known as Blaugrana?", "options": ["PSG", "Juventus", "Barcelona", "Real Madrid"], "answer": "Barcelona", "category": "Football"},
    {"question": "Which player has scored in the most Champions League seasons?", "options": ["Karim Benzema", "Cristiano Ronaldo", "Robert Lewandowski", "Lionel Messi"], "answer": "Cristiano Ronaldo", "category": "Football"}
]

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        if name:
            session.clear()
            session["username"] = name
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", total=len(QUESTIONS), username=session["username"])

@app.route("/start")
def start():
    if "username" not in session:
        return redirect(url_for("login"))
    
    session["score"] = 0
    session["current"] = 0
    indices = list(range(len(QUESTIONS)))
    random.shuffle(indices)
    session["question_order"] = indices
    return redirect(url_for("quiz"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "question_order" not in session:
        return redirect(url_for("start"))

    current_step = session["current"]
    total = len(QUESTIONS)

    if current_step >= total:
        return redirect(url_for("result"))

    q_idx = session["question_order"][current_step]
    question_data = QUESTIONS[q_idx]
    display_options = question_data["options"].copy()
    random.shuffle(display_options)

    if request.method == "POST":
        selected_answer = request.form.get("answer")
        if selected_answer == question_data["answer"]:
            session["score"] += 1
        session["current"] += 1
        return redirect(url_for("quiz"))

    return render_template("quiz.html", question=question_data, options=display_options, total=total, step=current_step + 1)

@app.route("/result", methods=["GET", "POST"])
def result():
    if "score" not in session:
        return redirect(url_for("index"))

    score = session["score"]
    total = len(QUESTIONS)
    percentage = int((score / total) * 100)
    username = session.get("username", "Guest")

    if request.method == "POST":
        data = load_leaderboard()
        data.append({"name": username, "score": score, "percentage": percentage})
        data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
        save_leaderboard(data)
        return redirect(url_for("leaderboard"))

    return render_template("result.html", score=score, total=total, percentage=percentage, name=username)

@app.route("/leaderboard")
def leaderboard():
    data = load_leaderboard()
    return render_template("leaderboard.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
