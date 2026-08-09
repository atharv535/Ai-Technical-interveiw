import json
import uuid
import requests
import streamlit as st

API_URL = st.secrets["API_URL"]

st.set_page_config(page_title="AI Technical Interview", page_icon="🤖", layout="centered")
st.title(" AI Technical Interview Agent")
st.caption("Personalized adaptive technical interview")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False
if "done" not in st.session_state:
    st.session_state.done = False

if not st.session_state.started:
    st.subheader("Candidate Information")
    candidate_id = st.text_input("Candidate ID", value="CAND-001")

    if st.button("Start Interview", type="primary"):
        with open("data/candidates.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        candidate = None
        for item in data["candidates"]:
            if item["member"]["id"] == candidate_id:
                candidate = item["member"].copy()
                candidate["missions"] = item["missions"]
                break

        if candidate is None:
            st.error("Candidate not found.")
        else:
            response = requests.post(API_URL, json={
                "sessionId": st.session_state.session_id,
                "candidate": candidate
            })
            if response.status_code != 200:
                st.error(response.text)
            else:
                result = response.json()
                st.session_state.messages.append({"role": "assistant", "content": result["reply"]})
                st.session_state.started = True
                st.rerun()

if st.session_state.started:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if st.session_state.started and not st.session_state.done:
    answer = st.chat_input("Type your technical answer...")
    if answer:
        st.session_state.messages.append({"role": "user", "content": answer})
        response = requests.post(API_URL, json={
            "sessionId": st.session_state.session_id,
            "message": answer
        })
        if response.status_code != 200:
            st.error(response.text)
        else:
            result = response.json()
            if result.get("reply"):
                st.session_state.messages.append({"role": "assistant", "content": result["reply"]})
            if result.get("done"):
                st.session_state.done = True
                st.session_state.feedback = result.get("feedback", {})
            st.rerun()

if st.session_state.done:
    st.divider()
    st.header(" Interview Feedback")
    feedback = st.session_state.feedback
    st.subheader("Overall Assessment")
    st.write(feedback.get("summary", ""))
    st.subheader(" Strengths")
    for item in feedback.get("strengths", []):
        st.write(f"• {item}")
    st.subheader(" Gaps")
    for item in feedback.get("gaps", []):
        st.write(f"• {item}")
    st.subheader(" Recommended Next Steps")
    for item in feedback.get("next", []):
        st.write(f"• {item}")
st.markdown("""
<style>

.stApp,
.stAppViewContainer,
.main,
.block-container {
    background-color: #0b0f19 !important;
    color: #f1f5f9 !important;
}


/* Your existing header/card/chat CSS here */


/* =========================================
   COMPLETE DARK BOTTOM AREA
   ========================================= */

[data-testid="stBottom"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100vw !important;

    background-color: #0b0f19 !important;
    border-top: 1px solid #1f2937 !important;

    z-index: 999999 !important;
}

[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottomBlockContainer"] {
    background-color: #0b0f19 !important;
}

[data-testid="stBottom"] div {
    background-color: transparent;
}

[data-testid="stChatInput"] {
    background-color: #111827 !important;
    border: 1px solid #475569 !important;
    border-radius: 16px !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #111827 !important;
    color: #f8fafc !important;
    border: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}

[data-testid="stChatInput"] button {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] button:hover {
    background-color: #1d4ed8 !important;
}

[data-testid="stMainBlockContainer"] {
    padding-bottom: 120px !important;
}

[data-testid="stBottom"]::before,
[data-testid="stBottom"]::after {
    background-color: #0b0f19 !important;
}

[data-testid="stChatMessage"] * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)
