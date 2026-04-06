import streamlit as st
import re
from datetime import datetime
import json
import csv
import io

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Study Buddy Questionnaire",
    page_icon="📚",
    layout="centered",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Card container */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 2.5rem 2.5rem 2rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    margin-bottom: 1.5rem;
}

/* Headings */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.6rem !important;
    background: linear-gradient(90deg, #e0c3fc, #8ec5fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem !important;
}

h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #e0c3fc !important;
}

p, label, .stMarkdown {
    color: #cdd3e8 !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #8ec5fc, #e0c3fc) !important;
    border-radius: 99px;
}

/* Inputs */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #8ec5fc !important;
    box-shadow: 0 0 0 3px rgba(142,197,252,0.2) !important;
}

/* Radio buttons */
.stRadio > label {
    color: #cdd3e8 !important;
    font-size: 0.95rem;
}
.stRadio > div {
    gap: 0.4rem;
}
div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.55rem 1rem;
    transition: all 0.2s;
    cursor: pointer;
    width: 100%;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(142,197,252,0.15);
    border-color: #8ec5fc;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #8ec5fc, #e0c3fc) !important;
    color: #1a1040 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-size: 1rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(142,197,252,0.4) !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: #e0c3fc !important;
    border: 1px solid rgba(224,195,252,0.4) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    background: rgba(224,195,252,0.15) !important;
    transform: translateY(-1px) !important;
}

/* Score badge */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #8ec5fc, #e0c3fc);
    color: #1a1040;
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 700;
    border-radius: 50%;
    width: 110px;
    height: 110px;
    line-height: 110px;
    text-align: center;
    margin: 1rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 40px rgba(142,197,252,0.5);
}

/* State pill */
.state-pill {
    display: inline-block;
    padding: 0.5rem 1.4rem;
    border-radius: 99px;
    font-size: 0.95rem;
    font-weight: 500;
    margin-top: 0.6rem;
}

/* File uploader */
.stFileUploader {
    background: rgba(255,255,255,0.05) !important;
    border: 1px dashed rgba(255,255,255,0.2) !important;
    border-radius: 14px !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* Success / error messages */
.stAlert {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Validation helpers
# ─────────────────────────────────────────────
def validate_name(name):
    return bool(re.match(r"^[A-Za-z\s\-']+$", name))

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validate_student_id(sid):
    return sid.isdigit()

# ─────────────────────────────────────────────
#  Questions
# ─────────────────────────────────────────────
QUESTIONS = [
    {"text": "Study sessions are more productive when working with a buddy.",
     "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"text": "Studying with a buddy helps maintain focus during study sessions.",
     "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"text": "Tasks are completed more efficiently when studying with a buddy.",
     "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"text": "I achieve better academic results when studying with a buddy.",
     "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"text": "Positive feedback from a study buddy improves confidence.",
     "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"text": "Collaborative studying helps identify gaps in my knowledge more effectively than studying alone.",
     "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"text": "Receiving encouragement from a study buddy enhances persistence when facing difficult tasks.",
     "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"text": "Studying with a buddy facilitates deeper understanding through explanation and discussion of concepts.",
     "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"text": "Studying with a buddy increases my awareness of my own learning strategies.",
     "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"text": "The presence of a study buddy increases my sense of accountability for academic responsibilities.",
     "options": ["Not at all", "Slightly", "Moderately", "Significantly", "Extremely"]},
    {"text": "Studying with a buddy reduces tendencies toward procrastination through shared responsibility.",
     "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"text": "Interaction with a study buddy encourages me to reflect on how I learn.",
     "options": ["Not at all", "Slightly", "Moderately", "Significantly", "Extremely"]},
    {"text": "Mutual encouragement contributes significantly to my academic success.",
     "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"text": "Exposure to alternative viewpoints from a study buddy strengthens my understanding.",
     "options": ["Not at all", "Slightly", "Moderately", "Significantly", "Extremely"]},
    {"text": "Study buddy systems should be encouraged in academic settings.",
     "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
]

SCORE_MAP = {opt: i for i, opt in enumerate(["Never", "Rarely", "Sometimes", "Often", "Always"])}
SCORE_MAP.update({opt: i for i, opt in enumerate(["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"])})
SCORE_MAP.update({opt: i for i, opt in enumerate(["Not at all", "Slightly", "Moderately", "Significantly", "Extremely"])})

def option_score(option_text):
    return SCORE_MAP.get(option_text, 0)

# ─────────────────────────────────────────────
#  Psychological state
# ─────────────────────────────────────────────
def get_psychological_state(score):
    if score <= 25:
        return ("Highly stressed", "may need psychological help.", "#ff6b6b", "🔴")
    elif score <= 35:
        return ("Moderately stressed", "occasional support recommended.", "#ffa94d", "🟠")
    elif score <= 50:
        return ("Stable", "no help required.", "#74c0fc", "🔵")
    elif score <= 60:
        return ("Positive state", "good coping mechanisms.", "#69db7c", "🟢")
    else:
        return ("Very positive & resilient", "thriving!", "#da77f2", "🟣")

# ─────────────────────────────────────────────
#  Session-state initialisation
# ─────────────────────────────────────────────
defaults = {
    "page": "menu",          # menu | info | questionnaire | result | load
    "student_name": "",
    "student_dob": "",
    "student_id": "",
    "q_index": 0,
    "answers": [],           # list of (q_index, option_text, score)
    "total_score": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page):
    st.session_state.page = page

# ─────────────────────────────────────────────
#  HEADER (always shown)
# ─────────────────────────────────────────────
st.markdown("<h1 style='text-align:center'>📚 Study Buddy</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8ec5fc;margin-bottom:2rem'>Academic Wellbeing Questionnaire</p>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: MENU
# ─────────────────────────────────────────────
if st.session_state.page == "menu":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Welcome!")
    st.write("This questionnaire explores how study-buddy systems affect your academic performance and wellbeing. It takes about 5 minutes.")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️  Start New Questionnaire"):
            # reset state
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.session_state.total_score = 0
            go("info")
            st.rerun()
    with col2:
        if st.button("📂  Load Existing Results"):
            go("load")
            st.rerun()

# ─────────────────────────────────────────────
#  PAGE: STUDENT INFO
# ─────────────────────────────────────────────
elif st.session_state.page == "info":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Your Details")

    name = st.text_input("Full Name", placeholder="e.g. Jane Doe")
    dob  = st.text_input("Date of Birth", placeholder="DD/MM/YYYY")
    sid  = st.text_input("Student ID", placeholder="Digits only")

    if st.button("Continue →"):
        errors = []
        if not name:
            errors.append("Name is required.")
        elif not validate_name(name):
            errors.append("Name may only contain letters, spaces, hyphens, and apostrophes.")
        if not dob:
            errors.append("Date of birth is required.")
        elif not validate_dob(dob):
            errors.append("Date of birth must be in DD/MM/YYYY format.")
        if not sid:
            errors.append("Student ID is required.")
        elif not validate_student_id(sid):
            errors.append("Student ID must contain digits only.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.student_name = name
            st.session_state.student_dob  = dob
            st.session_state.student_id   = sid
            go("questionnaire")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("← Back"):
        go("menu")
        st.rerun()

# ─────────────────────────────────────────────
#  PAGE: QUESTIONNAIRE
# ─────────────────────────────────────────────
elif st.session_state.page == "questionnaire":
    idx   = st.session_state.q_index
    total = len(QUESTIONS)

    # Progress
    progress = idx / total
    st.progress(progress)
    st.markdown(
        f"<p style='text-align:right;color:#8ec5fc;font-size:0.85rem'>Question {idx+1} of {total}</p>",
        unsafe_allow_html=True
    )

    q = QUESTIONS[idx]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"#### {idx+1}. {q['text']}")
    choice = st.radio("Select your answer:", q["options"], key=f"q_{idx}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if idx > 0:
            if st.button("← Back"):
                # undo last answer
                if st.session_state.answers:
                    _, _, prev_score = st.session_state.answers.pop()
                    st.session_state.total_score -= prev_score
                st.session_state.q_index -= 1
                st.rerun()
    with col2:
        label = "Next →" if idx < total - 1 else "Submit ✓"
        if st.button(label, type="primary"):
            score = option_score(choice)
            st.session_state.answers.append((idx, choice, score))
            st.session_state.total_score += score
            if idx < total - 1:
                st.session_state.q_index += 1
                st.rerun()
            else:
                go("result")
                st.rerun()

# ─────────────────────────────────────────────
#  PAGE: RESULT
# ─────────────────────────────────────────────
elif st.session_state.page == "result":
    score = st.session_state.total_score
    label, detail, color, emoji = get_psychological_state(score)

    # Score display
    st.markdown(f"""
    <div class='card' style='text-align:center'>
        <h2>Results for {st.session_state.student_name}</h2>
        <div class='score-badge'>{score}</div>
        <p style='font-size:0.85rem;color:#8ec5fc'>out of 60</p>
        <div class='state-pill' style='background:{color}22;border:1px solid {color};color:{color}'>
            {emoji} {label} — {detail}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Answer summary (collapsed)
    with st.expander("📋 View all answers"):
        for q_idx, opt, sc in st.session_state.answers:
            st.markdown(
                f"**Q{q_idx+1}.** {QUESTIONS[q_idx]['text']}  \n"
                f"→ *{opt}* &nbsp; `+{sc}`"
            )

    # ── Build export data ──
    data = {
        "name": st.session_state.student_name,
        "date_of_birth": st.session_state.student_dob,
        "student_id": st.session_state.student_id,
        "answers": [
            {
                "question": QUESTIONS[qi]["text"],
                "selected_answer": opt,
                "score": sc,
            }
            for qi, opt, sc in st.session_state.answers
        ],
        "total_score": score,
        "psychological_state": f"{label} — {detail}",
    }

    # TXT
    txt_lines = [
        f"Student Name: {data['name']}",
        f"Date of Birth: {data['date_of_birth']}",
        f"Student ID: {data['student_id']}",
        "",
    ]
    for ans in data["answers"]:
        txt_lines.append(ans["question"])
        txt_lines.append(f"Answer: {ans['selected_answer']} (Score: {ans['score']})")
        txt_lines.append("")
    txt_lines += [f"Total Score: {data['total_score']}", f"Psychological State: {data['psychological_state']}"]
    txt_bytes = "\n".join(txt_lines).encode("utf-8")

    # CSV
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow(["Student Name", data["name"]])
    writer.writerow(["Date of Birth", data["date_of_birth"]])
    writer.writerow(["Student ID", data["student_id"]])
    writer.writerow([])
    writer.writerow(["Question", "Selected Answer", "Score"])
    for ans in data["answers"]:
        writer.writerow([ans["question"], ans["selected_answer"], ans["score"]])
    writer.writerow([])
    writer.writerow(["Total Score", data["total_score"]])
    writer.writerow(["Psychological State", data["psychological_state"]])
    csv_bytes = csv_buf.getvalue().encode("utf-8")

    # JSON
    json_bytes = json.dumps(data, indent=4).encode("utf-8")

    st.markdown("#### 💾 Save Results")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("Download TXT", data=txt_bytes,  file_name="results.txt",  mime="text/plain")
    with c2:
        st.download_button("Download CSV", data=csv_bytes,  file_name="results.csv",  mime="text/csv")
    with c3:
        st.download_button("Download JSON", data=json_bytes, file_name="results.json", mime="application/json")

    st.markdown("---")
    if st.button("🔄 Start Over"):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

# ─────────────────────────────────────────────
#  PAGE: LOAD EXISTING
# ─────────────────────────────────────────────
elif st.session_state.page == "load":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Load Existing Results")
    uploaded = st.file_uploader("Upload a saved results file", type=["txt", "csv", "json"])

    if uploaded:
        try:
            content = ""
            if uploaded.name.endswith(".txt"):
                content = uploaded.read().decode("utf-8")

            elif uploaded.name.endswith(".csv"):
                reader = csv.reader(io.StringIO(uploaded.read().decode("utf-8")))
                rows = list(reader)
                content = "\n".join("\t".join(r) for r in rows)

            elif uploaded.name.endswith(".json"):
                data = json.loads(uploaded.read().decode("utf-8"))
                lines = [
                    f"Student Name: {data['name']}",
                    f"Date of Birth: {data['date_of_birth']}",
                    f"Student ID: {data['student_id']}",
                    "",
                ]
                for ans in data.get("answers", []):
                    lines.append(ans["question"])
                    lines.append(f"Answer: {ans['selected_answer']} (Score: {ans['score']})")
                    lines.append("")
                lines += [
                    f"Total Score: {data['total_score']}",
                    f"Psychological State: {data['psychological_state']}",
                ]
                content = "\n".join(lines)

            st.success("File loaded successfully!")
            st.text_area("File Contents", content, height=380)

        except Exception as e:
            st.error(f"Failed to read file: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("← Back to Menu"):
        go("menu")
        st.rerun()
