import streamlit as st

st.set_page_config(page_title="AI Interview Coach", layout="centered")

if "started" not in st.session_state:
  st.session_state.started=False
if "current_q" not in st.session_state:
  st.session_state.current_q=0
if "scores" not in st.session_state:
  st.session_state.scores=[]
if "interview_data" not in st.session_state:
  st.session_state.interview_data=[]



st.title("🤖 AI Interview Coach")
st.subheader("Practice. Evaluate. Improve.")

st.write("Welcome! Start your AI-powered interview practice.")

st.markdown("👉Setup Your Interview")

if not st.session_state.started:
  # Role selection
  roles = [
    "Python",
    "AI/ML",
    "Frontend",
    "Backend",
    "Full Stack",
    "Data Analyst",
    "HR"
]

  role=st.selectbox("Select Role", roles)

# Experience
  experience = st.selectbox("Experience Level", ["Junior", "Mid", "Senior"])

# Difficulty
  difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# Number of questions
  num_questions = st.slider("Number of Questions", 1, 30, 5)

# Start button
  start = st.button("Start Interview 🚀")
  if start:
   st.session_state.started = True

if st.session_state.started:
    st.write("Interview Started 🚀")
    st.write(f"Question Number: {st.session_state.current_q + 1}")
