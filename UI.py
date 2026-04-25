import streamlit as st

st.set_page_config(page_title="AI Interview Coach", layout="centered")

st.title("🤖 AI Interview Coach")
st.subheader("Practice. Evaluate. Improve.")

st.write("Welcome! Start your AI-powered interview practice.")

st.markdown("👉Setup Your Interview")

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
