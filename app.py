import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "quiz-secret-key-2024")

QUESTIONS = [
    {
        "question": "Who is GOAT of Footbal?",
        "options": ["Kustiyar Ronaldo", "Pele", "Hand of GOD", "Leo Messi"],
        "answer": "Leo Messi",
        "category": "Sports"
    },
    {
        "question": "Who is the father of Real Mardrid?",
        "options": ["Raphinha", "Rice", "Messi", "Lamin Yamal"],
        "answer": "Messi",
        "category": "Football"
    },
    {
        "question": "Who is the best All-Rounder in cricket history?",
        "options": ["Kapil Dev", "Shakib Al Hasan", "Imran Khan", "Jacques Kallis"],
        "answer": "Shakib Al Hasan",
        "category": "Cricket"
    }
]

@app.route("/")
def index():
    return render_template("index.html", total=len(QUESTIONS))


@app.route("/start")
def start():
    session.clear()
    session["score"] = 0
    session["current"] = 0
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "current" not in session:
        return redirect(url_for("start"))

    current = session["current"]
    total = len(QUESTIONS)

    if current >= total:
        return redirect(url_for("result"))

    question = QUESTIONS[current]

    # Shuffle options (safe copy)
    options = question["options"][:]
    random.shuffle(options)

    if request.method == "POST":
        selected = request.form.get("answer")
        correct = question["answer"]

        if selected == correct:
            session["score"] += 1

        session["current"] += 1
        return redirect(url_for("quiz"))

    return render_template(
        "quiz.html",
        question=question,
        options=options,
        qno=current,
        total=total,
        progress=int((current / total) * 100),
        correct_answer=question["answer"]
    )


@app.route("/result")
def result():
    if "score" not in session:
        return redirect(url_for("index"))

    score = session["score"]
    total = len(QUESTIONS)
    percentage = int((score / total) * 100)

    # Grade system
    if percentage >= 80:
        grade = "🔥 Genius"
    elif percentage >= 50:
        grade = "👏 Well Done"
    else:
        grade = "💡 Try Again"

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        grade=grade
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
