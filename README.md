# AI Technical Interview Agent

Python + FastAPI + Streamlit implementation for the supplied AI Cohort interview challenge.

## Run

### Terminal 1
```bash
pip install -r requirements.txt
copy .env.example .env
```

Add your Gemini API key to `.env`.

Then:
```bash
uvicorn app.main:app --reload --port 8000
```

### Terminal 2
```bash
streamlit run streamlit_app.py
```

Open the Streamlit URL and start with a candidate such as `CAND-001`.

## API

POST `/api/interview`

Initial request:
```json
{
  "sessionId": "abc-123",
  "candidate": {}
}
```

Next turns:
```json
{
  "sessionId": "abc-123",
  "message": "candidate answer"
}
```
