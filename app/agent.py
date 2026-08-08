import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

with open("data/curriculum.json", "r", encoding="utf-8") as f:
    curriculum = json.load(f)

def get_curriculum_day(day_number):
    return next((d for d in curriculum["days"] if d["day"] == day_number), None)

def get_candidate_topics(candidate):
    topics = []
    for mission in candidate.get("missions", []):
        if mission.get("passed") is True:
            day = get_curriculum_day(mission["day"])
            if day:
                topics.append({
                    "day": mission["day"],
                    "title": mission["title"],
                    "attempts": mission.get("attempts", 1),
                    "objectives": day.get("objectives", [])
                })
    return topics

def choose_initial_days(candidate):
    topics = get_candidate_topics(candidate)
    topics.sort(key=lambda x: x["attempts"])
    selected = []
    for topic in topics:
        if topic["day"] not in selected:
            selected.append(topic["day"])
        if len(selected) >= 5:
            break
    return selected

def build_interview_prompt(session, user_message):
    candidate = session["candidate"]
    topics = get_candidate_topics(candidate)
    prompt = f"""
You are a professional technical interviewer conducting a realistic multi-turn
technical interview.

Candidate:
Name: {candidate.get("name")}
Role: {candidate.get("jobRole")}
Experience: {candidate.get("yearsExperience")}
Education: {candidate.get("education")}

Completed curriculum topics:
{json.dumps(topics, indent=2)}

Questions asked: {session["questions_asked"]}
Days already covered: {session["days_covered"]}
Current topic: {session["current_topic"]}

Recent conversation:
{json.dumps(session["messages"][-10:], indent=2)}

Latest candidate answer:
{user_message}

Rules:
- Ask at least 8 questions total.
- Cover at least 4 different curriculum days.
- Ask a targeted follow-up when the answer is incomplete.
- If the answer is strong, increase difficulty or move to another topic.
- Keep context from previous answers.
- Do not behave like a fixed questionnaire.
- Do not ask about skipped topics unless necessary.
- Return ONLY the next interview question.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

def evaluate_answer(session, answer):
    day = get_curriculum_day(session["current_day"])
    objectives = day.get("objectives", []) if day else []
    prompt = f"""
Evaluate this technical interview answer from 0 to 10.

Topic: Day {session["current_day"]} - {day.get("title") if day else "Unknown"}
Objectives: {json.dumps(objectives)}
Answer: {answer}

Return ONLY valid JSON:
{{
  "score": 0,
  "strength": "short explanation",
  "gap": "short explanation"
}}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except Exception:
        return {"score": 5, "strength": "Answer evaluated.", "gap": "More detail could be provided."}

def generate_feedback(session):
    prompt = f"""
You are a senior technical interviewer.

Candidate: {session["candidate"].get("name")}
Role: {session["candidate"].get("jobRole")}

Evaluation:
{json.dumps(session["scores"], indent=2)}

Return ONLY valid JSON:
{{
  "summary": "overall assessment",
  "strengths": ["strength 1", "strength 2"],
  "gaps": ["gap 1", "gap 2"],
  "next": ["specific recommendation 1", "specific recommendation 2"]
}}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except Exception:
        return {"summary": "Interview completed.", "strengths": [], "gaps": [], "next": []}

def start_interview(session):
    days = choose_initial_days(session["candidate"])
    if not days:
        question = "Let's begin. What is your strongest technical area from the cohort?"
        session["current_day"] = None
        session["current_topic"] = "General technical knowledge"
    else:
        first_day = days[0]
        session["current_day"] = first_day
        day = get_curriculum_day(first_day)
        session["current_topic"] = day["title"]
        session["days_covered"].append(first_day)
        question = f"Let's begin with {day['title']}. Can you explain the core concept behind this topic and why it is useful in an AI application?"
    session["questions_asked"] += 1
    session["messages"].append({"role": "assistant", "content": question})
    return question

def continue_interview(session, user_message):
    evaluation = evaluate_answer(session, user_message)
    session["scores"].append({
        "day": session["current_day"],
        "topic": session["current_topic"],
        "score": evaluation["score"],
        "strength": evaluation["strength"],
        "gap": evaluation["gap"]
    })
    session["messages"].append({"role": "user", "content": user_message})

    if session["questions_asked"] >= 8:
        feedback = generate_feedback(session)
        session["done"] = True
        return {"reply": "Interview completed.", "done": True, "feedback": feedback}

    possible_days = choose_initial_days(session["candidate"])
    next_day = next((d for d in possible_days if d not in session["days_covered"]), None)

    if evaluation["score"] < 6 or next_day is None:
        question = build_interview_prompt(session, user_message)
    else:
        session["current_day"] = next_day
        day_data = get_curriculum_day(next_day)
        session["current_topic"] = day_data["title"]
        session["days_covered"].append(next_day)
        question = f"Let's move to {day_data['title']}. Imagine you are implementing this in a production AI system. How would you approach it, and what trade-offs would you consider?"

    session["questions_asked"] += 1
    session["messages"].append({"role": "assistant", "content": question})
    return {"reply": question, "done": False}
