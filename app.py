import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "quiz-secret-key-2024")

QUESTIONS = [
    {
        "question": "Who is GOAT of Footbal?",
        "options": ["Messi", "Lm10", "Leo", "Leo Messi" ],
        "answer": ["Messi", "Lm10", "Leo", "Leo Messi" ],
        "category": "Sports"
    },
    {
        "question": "Who is the father of Real Mardrid?",
        "options": ["Messi", "Raphinha", "Lamin Yamal" , "Rice" ],
        "answer": "Messi",
        "category": "Football"
    },
{
    "question": "Who is the best All-Rounder in cricket history?",
    "options": ["Shakib Al Hasan", "Jacques Kallis", "Kapil Dev", "Imran Khan"],
    "answer": "Shakib Al Hasan",
    "category": "Cricket"
},
{
    "question": "Which country won the ICC World Cup 2019?",
    "options": ["England", "Australia", "New Zealand", "South Africa"],
    "answer": "England",
    "category": "Cricket"
},
{
    "question": "Who has the highest runs in ODI cricket?",
    "options": ["Sachin Tendulkar", "Ricky Ponting", "Kumar Sangakkara", "Brian Lara"],
    "answer": "Sachin Tendulkar",
    "category": "Cricket"
},
{
    "question": "Who is the fastest bowler in cricket history?",
    "options": ["Shoaib Akhtar", "Brett Lee", "Mitchell Starc", "Wasim Akram"],
    "answer": "Shoaib Akhtar",
    "category": "Cricket"
},
{
    "question": "Which team has won the most ICC World Cups?",
    "options": ["Australia", "West Indies", "England", "Pakistan"],
    "answer": "Australia",
    "category": "Cricket"
},
{
    "question": "Which country won FIFA World Cup 2022?",
    "options": ["Argentina", "France", "Brazil", "Germany"],
    "answer": "Argentina",
    "category": "Football"
},
{
    "question": "Who has the most Ballon d'Or?",
    "options": ["Messi", "Zidane", "Ronaldinho", "Kaka"],
    "answer": "Messi",
    "category": "Football"
},
{
    "question": "Which club is known as Red Devils?",
    "options": ["Manchester United", "Liverpool", "Chelsea", "Arsenal"],
    "answer": "Manchester United",
    "category": "Football"
},
{
    "question": "Which club has the most Champions League titles?",
    "options": ["Real Madrid", "Barcelona", "Bayern Munich", "Liverpool"],
    "answer": "Real Madrid",
    "category": "Football"
},
{
    "question": "Who is known as Brazilian magician?",
    "options": ["Ronaldinho", "Kaka", "Neymar", "Ronaldo Nazario"],
    "answer": "Ronaldinho",
    "category": "Football"
},
{
    "question": "Which country is famous for Samba football?",
    "options": ["Brazil", "Argentina", "Spain", "Portugal"],
    "answer": "Brazil",
    "category": "Football"
},
{
    "question": "Who won Golden Boot in World Cup 2018?",
    "options": ["Mbappe", "Kane", "Griezmann", "Modric"],
    "answer": "Kane",
    "category": "Football"
},
{
    "question": "Who is the best captain in cricket history?",
    "options": ["MS Dhoni", "Ricky Ponting", "Graeme Smith", "Clive Lloyd"],
    "answer": "MS Dhoni",
    "category": "Cricket"
},
{
    "question": "Which player is called Mr. 360 in cricket?",
    "options": ["AB de Villiers", "Steve Smith", "Buttler", "Maxwell"],
    "answer": "AB de Villiers",
    "category": "Cricket"
},
{
    "question": "Which country invented cricket?",
    "options": ["England", "Australia", "South Africa", "Pakistan"],
    "answer": "England",
    "category": "Cricket"
},
{
    "question": "Who is the greatest football playmaker?",
    "options": ["Messi", "Xavi", "Iniesta", "Modric"],
    "answer": "Messi",
    "category": "Football"
},
{
    "question": "Which team is known as Blaugrana?",
    "options": ["Barcelona", "Real Madrid", "PSG", "Juventus"],
    "answer": "Barcelona",
    "category": "Football"
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
    session["answers"] = []
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "current" not in session:
        return redirect(url_for("index"))

    current = session["current"]
    total = len(QUESTIONS)

    if request.method == "POST":
        selected = request.form.get("answer")
        question = QUESTIONS[current]
        correct = question["answer"]
        is_correct = selected == correct

        if is_correct:
            session["score"] += 1

        session["answers"] = session.get("answers", []) + [{
            "question": question["question"],
            "selected": selected,
            "correct": correct,
            "is_correct": is_correct,
            "category": question["category"]
        }]

        session["current"] = current + 1

        if session["current"] >= total:
            return redirect(url_for("result"))
        return redirect(url_for("quiz"))

    if current >= total:
        return redirect(url_for("result"))

    question = QUESTIONS[current]
    return render_template(
        "quiz.html",
        question=question,
        current=current + 1,
        total=total,
        progress=int((current / total) * 100)
    )


@app.route("/result")
def result():
    if "score" not in session:
        return redirect(url_for("index"))

    score = session["score"]
    total = len(QUESTIONS)
    answers = session.get("answers", [])
    percentage = int((score / total) * 100)

    if percentage >= 90:
        grade = "Excellent!"
        grade_class = "grade-excellent"
    elif percentage >= 70:
        grade = "Great job!"
        grade_class = "grade-great"
    elif percentage >= 50:
        grade = "Good effort!"
        grade_class = "grade-good"
    else:
        grade = "Keep practicing!"
        grade_class = "grade-poor"

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        grade=grade,
        grade_class=grade_class,
        answers=answers
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
