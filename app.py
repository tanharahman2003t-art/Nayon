import os
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "messi-goat-2026"
LEADERBOARD_FILE = "leaderboard.json"

QUESTIONS = [
    {"question": "Who is the GOAT of football?", "options": ["Ronaldo", "Messi", "Pele", "Maradona"], "answer": "Messi", "level": "Easy"},
    {"question": "In which city was Lionel Messi born?", "options": ["Rosario", "Buenos Aires", "Madrid", "Barcelona"], "answer": "Rosario", "level": "Easy"},
    {"question": "What is Messi's famous jersey number for Argentina?", "options": ["7", "9", "10", "11"], "answer": "10", "level": "Easy"},
    {"question": "Which club did Messi join as a child?", "options": ["Real Madrid", "FC Barcelona", "PSG", "Liverpool"], "answer": "FC Barcelona", "level": "Easy"},
    {"question": "What is Messi's nickname?", "options": ["The King", "La Pulga", "CR7", "The Wall"], "answer": "La Pulga", "level": "Easy"},
    {"question": "Which country does Messi play for?", "options": ["Brazil", "Spain", "Argentina", "Portugal"], "answer": "Argentina", "level": "Easy"},
    {"question": "How many Ballon d'Or does Messi have (as of 2024)?", "options": ["5", "7", "8", "9"], "answer": "8", "level": "Easy"},
    {"question": "Which position does Messi mainly play?", "options": ["Goalkeeper", "Forward", "Defender", "Coach"], "answer": "Forward", "level": "Easy"},
    {"question": "Messi's first professional goal was assisted by?", "options": ["Xavi", "Iniesta", "Ronaldinho", "Eto'o"], "answer": "Ronaldinho", "level": "Easy"},
    {"question": "Which US club does Messi play for currently?", "options": ["LA Galaxy", "Inter Miami", "NY City FC", "Orlando City"], "answer": "Inter Miami", "level": "Easy"},
    {"question": "In which year did Messi win his first FIFA World Cup?", "options": ["2014", "2018", "2022", "2010"], "answer": "2022", "level": "Medium"},
    {"question": "How many goals did Messi score in the 2012 calendar year?", "options": ["85", "91", "73", "95"], "answer": "91", "level": "Medium"},
    {"question": "Which trophy did Messi win in 2021 with Argentina?", "options": ["World Cup", "Copa America", "Finalissima", "Euro Cup"], "answer": "Copa America", "level": "Medium"},
    {"question": "Against which team did Messi score his famous solo goal in 2007?", "options": ["Getafe", "Real Madrid", "Espanyol", "Sevilla"], "answer": "Getafe", "level": "Medium"},
    {"question": "Messi's first Ballon d'Or was won in which year?", "options": ["2008", "2009", "2010", "2007"], "answer": "2009", "level": "Medium"},
    {"question": "How many Champions League titles has Messi won?", "options": ["2", "3", "4", "5"], "answer": "4", "level": "Medium"},
    {"question": "Messi's first World Cup goal was against?", "options": ["Mexico", "Serbia & Montenegro", "Nigeria", "Germany"], "answer": "Serbia & Montenegro", "level": "Medium"},
    {"question": "Who was the coach when Messi won the 'Sextuple'?", "options": ["Enrique", "Guardiola", "Vilanova", "Koeman"], "answer": "Guardiola", "level": "Medium"},
    {"question": "Messi won the Golden Ball in which two World Cups?", "options": ["2010, 2014", "2014, 2018", "2014, 2022", "2006, 2022"], "answer": "2014, 2022", "level": "Medium"},
    {"question": "How many European Golden Shoes has Messi won?", "options": ["4", "5", "6", "7"], "answer": "6", "level": "Medium"},
    {"question": "Messi's 500th career goal was scored against which team?", "options": ["Real Madrid", "Atletico Madrid", "Valencia", "PSG"], "answer": "Real Madrid", "level": "Hard"},
    {"question": "How many hat-tricks has Messi scored for Barcelona?", "options": ["35", "48", "50", "42"], "answer": "48", "level": "Hard"},
    {"question": "Who is the only player to assist Messi more than 50 times?", "options": ["Dani Alves", "Suarez", "Xavi", "Neymar"], "answer": "Dani Alves", "level": "Hard"},
    {"question": "Messi made his Barcelona debut in a friendly against which team?", "options": ["Porto", "Juventus", "Milan", "Ajax"], "answer": "Porto", "level": "Hard"},
    {"question": "What was Messi's age during his senior international debut?", "options": ["17", "18", "19", "16"], "answer": "18", "level": "Hard"},
    {"question": "Against which team did Messi score 5 goals in one UCL match?", "options": ["Arsenal", "Leverkusen", "Lyon", "Celtic"], "answer": "Leverkusen", "level": "Hard"},
    {"question": "How many goals did Messi score for PSG in all competitions?", "options": ["30", "32", "35", "28"], "answer": "32", "level": "Hard"},
    {"question": "In the 2022 WC final, which minute did Messi score his first goal?", "options": ["23rd", "10th", "35th", "108th"], "answer": "23rd", "level": "Hard"},
    {"question": "Messi's famous 'napkin contract' was signed in which year?", "options": ["1999", "2000", "2001", "2002"], "answer": "2000", "level": "Hard"},
    {"question": "How many free-kick goals has Messi scored for Argentina?", "options": ["9", "10", "11", "12"], "answer": "11", "level": "Hard"}
]

@app.route("/")
def login(): return render_template("login.html")

@app.route("/start", methods=["POST"])
def start():
    session["username"] = request.form.get("username", "Guest")
    session["score"] = 0
    session["current"] = 0
    session["lifeline_count"] = 3
    indices = list(range(len(QUESTIONS)))
    random.shuffle(indices)
    session["question_order"] = indices
    return redirect(url_for("quiz"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "question_order" not in session: return redirect(url_for("/"))
    if session["current"] >= len(QUESTIONS): return redirect(url_for("result"))
    
    q_idx = session["question_order"][session["current"]]
    question = QUESTIONS[q_idx]

    if request.method == "POST":
        ans = request.form.get("answer")
        if ans == "USE_FIFTY" and session.get("lifeline_count", 0) > 0:
            session["lifeline_count"] -= 1
            return {"status": "ok", "remaining": session["lifeline_count"]}
        
        if ans == question["answer"]: session["score"] += 1
        session["current"] += 1
        return redirect(url_for("quiz"))

    opts = question["options"].copy()
    random.shuffle(opts)
    return render_template("quiz.html", question=question, options=opts, total=len(QUESTIONS), step=session["current"]+1, lifelines=session.get("lifeline_count", 3))

@app.route("/result")
def result():
    score = session.get("score", 0)
    return render_template("result.html", score=score, total=len(QUESTIONS), percentage=int((score/len(QUESTIONS))*100))

if __name__ == "__main__": app.run(debug=True)
