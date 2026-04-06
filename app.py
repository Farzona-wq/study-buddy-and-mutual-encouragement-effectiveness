import streamlit as st
import re
from datetime import datetime
import json
import csv

# ----------------- Validation -----------------
def validate_name(name):
    return bool(re.match(r"^[A-Za-z\s\-']+$", name))

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%d/%m/%Y")
        return True
    except:
        return False

def validate_student_id(student_id):
    return student_id.isdigit()

# ----------------- Questions -----------------
questions = [
    {"text": "1) Study sessions are more productive when working with a buddy.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "2) Studying with a buddy helps maintain focus during study sessions.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "3) Tasks are completed more efficiently when studying with a buddy.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]},
    {"text": "4) I achieve better academic results when studying with a buddy.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "5) Positive feedback from a study buddy improves confidence.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]},
]

# ----------------- Psychological State -----------------
def get_state(score):
    if score <= 25:
        return "Highly stressed"
    elif score <= 35:
        return "Moderately stressed"
    elif score <= 50:
        return "Stable"
    elif score <= 60:
        return "Positive"
    else:
        return "Very positive"

# ----------------- Session State -----------------
if "step" not in st.session_state:
    st.session_state.step = "menu"
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = []

# ----------------- MENU -----------------
st.title("Questionnaire System")

if st.session_state.step == "menu":
    st.subheader("Choose option")

    if st.button("Start New Questionnaire"):
        st.session_state.step = "form"

    uploaded_file = st.file_uploader("Load existing file", type=["txt", "csv", "json"])

    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("Loaded Content", content, height=300)

# ----------------- STUDENT FORM -----------------
elif st.session_state.step == "form":
    st.subheader("Enter Details")

    name = st.text_input("Full Name")
    dob = st.text_input("DOB (DD/MM/YYYY)")
    sid = st.text_input("Student ID")

    if st.button("Start"):
        if not validate_name(name):
            st.error("Invalid name")
        elif not validate_dob(dob):
            st.error("Invalid DOB")
        elif not validate_student_id(sid):
            st.error("Invalid ID")
        else:
            st.session_state.name = name
            st.session_state.dob = dob
            st.session_state.sid = sid
            st.session_state.step = "quiz"

# ----------------- QUIZ -----------------
elif st.session_state.step == "quiz":
    q = questions[st.session_state.q_index]

    st.subheader(f"Question {st.session_state.q_index + 1}")
    choice = st.radio(q["text"], q["options"], format_func=lambda x: x[0])

    if st.button("Next"):
        st.session_state.score += choice[1]
        st.session_state.answers.append((q["text"], choice))

        st.session_state.q_index += 1

        if st.session_state.q_index >= len(questions):
            st.session_state.step = "result"
        else:
            st.rerun()

# ----------------- RESULT -----------------
elif st.session_state.step == "result":
    st.subheader("Result")

    score = st.session_state.score
    state = get_state(score)

    st.write(f"Total Score: {score}")
    st.write(f"Psychological State: {state}")

    data = {
        "name": st.session_state.name,
        "dob": st.session_state.dob,
        "id": st.session_state.sid,
        "score": score,
        "state": state,
        "answers": st.session_state.answers
    }

    json_data = json.dumps(data, indent=4)

    st.download_button(
        "Download JSON",
        json_data,
        file_name="result.json"
    )

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
