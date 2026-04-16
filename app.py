import uuid
from flask import Flask, render_template, request, jsonify, session
from prolog_engine import PrologSession

app = Flask(__name__)
app.secret_key = "ba_eats_secret_key_12345" # In production, use a secure random key

# In-memory storage for active sessions
sessions = {}

def get_session():
    """Retrieves or creates a PrologSession for the current user."""
    if "session_id" not in session or session["session_id"] not in sessions:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id
        sessions[session_id] = PrologSession()
    return sessions[session["session_id"]]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start_quiz():
    """Initializes or resets the questionnaire state."""
    ps = get_session()
    ps.__init__() # Reset the session state
    next_q = ps.get_next_question()
    return jsonify({
        "done": False,
        "question": next_q,
        "progress": {"current": 1, "total": len(ps.QUESTIONS)}
    })

@app.route("/api/answer", methods=["POST"])
def submit_answer():
    """Processes an answer and returns the next question or results."""
    data = request.json
    q_id = data.get("question_id")
    answer = data.get("answer")
    
    ps = get_session()
    ps.submit_answer(q_id, answer)
    
    next_q = ps.get_next_question()
    
    if next_q:
        return jsonify({
            "done": False,
            "question": next_q,
            "progress": {"current": ps.current_question_index + 1, "total": len(ps.QUESTIONS)}
        })
    else:
        results = ps.recommend()
        return jsonify({
            "done": True,
            "results": results
        })

@app.route("/api/reset", methods=["POST"])
def reset():
    """Clears the session."""
    if "session_id" in session:
        sessions.pop(session["session_id"], None)
    return jsonify({"status": "success"})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)