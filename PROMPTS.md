# AI Usage Log — AI Technical Interview Agent

## Project

**AI Technical Interview Agent**

A conversational AI agent designed to conduct realistic, multi-turn technical
interviews based on a candidate's completed curriculum topics and candidate
profile.

---

## AI Model Used

**Gemini 2.5 Flash**

The application uses Gemini 2.5 Flash to:

- Generate technical interview questions
- Generate adaptive follow-up questions
- Evaluate candidate answers
- Adjust interview difficulty
- Generate final interview feedback

---

# Development Prompts

## 1. Initial Project Architecture

### Prompt

Design an AI agent capable of conducting a realistic, multi-turn technical
interview.

The agent should:

- Assess the candidate's understanding of completed curriculum concepts.
- Adapt naturally throughout the conversation.
- Ask intelligent follow-up questions.
- Maintain context across multiple interview turns.
- Provide actionable feedback at the end.
- Ask at least 8 questions.
- Cover at least 4 different curriculum days.
- Expose a POST /api/interview endpoint.
- Maintain interview state using sessionId.

The implementation should use the provided curriculum, candidate profiles,
and technical specification.

---

## 2. Adaptive Interviewer Prompt

### Prompt

You are a professional technical interviewer conducting a realistic
multi-turn technical interview.

Use the candidate profile and completed curriculum topics to decide which
technical concepts to assess.

Requirements:

- Ask at least 8 questions total.
- Cover at least 4 different curriculum days.
- Maintain context from previous answers.
- Ask targeted follow-up questions when an answer is incomplete.
- If the candidate demonstrates strong understanding, increase the difficulty.
- Use practical production-oriented scenarios.
- Avoid behaving like a fixed questionnaire.
- Avoid asking about skipped topics unless necessary.
- Do not repeat questions unnecessarily.
- Return only the next interview question.

The interviewer should behave conversationally rather than following a
predefined list of questions.

---

## 3. Candidate Answer Evaluation Prompt

### Prompt

Evaluate the candidate's technical interview answer from 0 to 10.

Consider:

- Conceptual correctness
- Technical depth
- Understanding of the relevant curriculum objective
- Practical application
- Clarity of explanation

Return valid JSON containing:

- score
- strength
- gap

The evaluation will be stored as part of the interview session and used to
decide whether the next question should be a follow-up or a new topic.

---

## 4. Adaptive Follow-up Prompt

### Prompt

Based on the candidate's previous answer and the recent interview
conversation, generate the next technical interview question.

If the candidate's answer is incomplete or demonstrates a knowledge gap,
ask a targeted follow-up question that explores the same concept.

If the candidate demonstrates strong understanding, increase the difficulty
or move to another completed curriculum topic.

Maintain context from the previous questions and answers.

Return only the next interview question.

---

## 5. Final Feedback Prompt

### Prompt

You are a senior technical interviewer.

Review the candidate's interview evaluations and provide structured,
actionable feedback.

Return valid JSON containing:

- summary
- strengths
- gaps
- next

The summary should provide an overall assessment.

The strengths should identify areas where the candidate demonstrated
understanding.

The gaps should identify concepts that need improvement.

The next recommendations should provide specific and actionable areas
for further learning or practice.

---

# AI-Assisted Development

AI assistance was used during development for:

- Designing the interview-agent architecture
- Developing adaptive interview prompts
- Designing the answer-evaluation process
- Designing the final feedback structure
- Debugging Python and FastAPI issues
- Troubleshooting Gemini API integration
- Troubleshooting deployment issues
- Improving the Streamlit interface
- Improving the interview conversation flow

---

# Technical Implementation

The application consists of:

- FastAPI backend
- Streamlit frontend
- Gemini 2.5 Flash
- Curriculum JSON data
- Candidate profile data
- Session-based interview state

The main API endpoint is:

`POST /api/interview`

The endpoint receives a `sessionId` and candidate information when starting
an interview, and subsequent requests use the same `sessionId` to maintain
the conversation.

---

# Interview Logic

The interview agent:

1. Reads the candidate profile.
2. Identifies completed curriculum topics.
3. Selects relevant curriculum days.
4. Starts the technical interview.
5. Evaluates each candidate response.
6. Uses the evaluation to determine the next question.
7. Generates follow-up questions when appropriate.
8. Moves to new curriculum topics when the candidate demonstrates sufficient
   understanding.
9. Maintains the conversation history.
10. Completes the interview after the required number of questions.
11. Generates structured final feedback.

---

# Development Notes

The prompts and AI-assisted development process were iteratively refined
while building and testing the application.

The final implementation uses Gemini 2.5 Flash for the conversational
interview, answer evaluation, adaptive questioning, and final feedback.
