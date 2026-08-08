sessions = {}

def create_session(session_id, candidate):
    sessions[session_id] = {
        "candidate": candidate,
        "messages": [],
        "questions_asked": 0,
        "days_covered": [],
        "scores": [],
        "current_day": None,
        "current_topic": None,
        "done": False,
    }
    return sessions[session_id]

def get_session(session_id):
    return sessions.get(session_id)
