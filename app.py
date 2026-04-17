import os
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "messi-goat-2026")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

LEADERBOARD_FILE = "leaderboard.json"

# --- ৩০টি কুইজ প্রশ্ন (মেসি স্পেশাল) ---
QUESTIONS = [
    # EASY (10)
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

    # MEDIUM (10)
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

    # HARD (10)
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE): return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        if name:
            session.clear()
            session["username"] = name
            session["profile_pic"] = 'default_avatar.png'
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/")
def index():
    if "username" not in session: return redirect(url_for("login"))
    return render_template("index.html", total=len(QUESTIONS), username=session["username"])

@app.route("/start")
def start():
    if "username" not in session: return redirect(url_for("login"))
    session["score"] = 0
    session["current"] = 0
    session["lifeline_count"] = 3  # ৫০:৫০ লিমিট সেট করা হলো
    indices = list(range(len(QUESTIONS)))
    random.shuffle(indices)
    session["question_order"] = indices
    return redirect(url_for("quiz"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "question_order" not in session: return redirect(url_for("start"))
    current_step = session["current"]
    total = len(QUESTIONS)
    
    if current_step >= total: return redirect(url_for("result"))

    q_idx = session["question_order"][current_step]
    question_data = QUESTIONS[q_idx]
    
    if request.method == "POST":
        selected = request.form.get("answer")
        # লাইফলাইন ব্যবহারের রিকোয়েস্ট হ্যান্ডেল করা
        if selected == "USE_FIFTY":
            if session.get("lifeline_count", 0) > 0:
                session["lifeline_count"] -= 1
                return {"status": "ok", "remaining": session["lifeline_count"]}
            return {"status": "error", "message": "Limit reached"}
        
        # উত্তর চেক করা
        if selected == question_data["answer"]:
            session["score"] += 1
        
        session["current"] += 1
        return redirect(url_for("quiz"))

    display_options = question_data["options"].copy()
    random.shuffle(display_options)
    
    return render_template("quiz.html", 
                           question=question_data, 
                           options=display_options, 
                           total=total, 
                           step=current_step + 1,
                           lifelines=session.get("lifeline_count", 3))

@app.route("/result", methods=["GET", "POST"])
def result():
    if "score" not in session: return redirect(url_for("index"))
    score, total = session["score"], len(QUESTIONS)
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
    return render_template("leaderboard.html", data=load_leaderboard())

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
