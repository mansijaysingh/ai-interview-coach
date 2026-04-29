import streamlit as st
import re
from app import generate_question, evaluate_interview

st.set_page_config(page_title="AI Interview Coach", layout="centered")

if "started" not in st.session_state:
  st.session_state.started=False
if "current_q" not in st.session_state:
  st.session_state.current_q=0
if "scores" not in st.session_state:
  st.session_state.scores=[]
if "interview_data" not in st.session_state:
  st.session_state.interview_data=[]
if"asked_questions" not in st.session_state:
  st.session_state.asked_questions=[]
if "input_key" not in st.session_state:
  st.session_state.input_key=0
if "ended" not in st.session_state:
  st.session_state.ended=False




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
   st.session_state.role=role
   st.session_state.experience=experience
   st.session_state.difficulty=difficulty
   st.session_state.num_questions=num_questions

   st.rerun()

if st.session_state.started:
    st.write("Interview Started 🚀")

    if (
      st.session_state.current_q>= st.session_state.num_questions
      or st.session_state.ended
    ):
       st.success("Interview Completed 🎉")


       valid_data=[
        data for data in st.session_state.interview_data
        if data["answer"] != "Skipped"
    ]

       st.markdown("## 📊 Final Evaluation")

       if len(valid_data)==0:
        st.warning("No questions attempted")
       else:
        with st.spinner("Evaluating your overall performance..."):
         result=evaluate_interview(valid_data)

        st.write(result)

       if st.button("Restart Interview"):
         st.session_state.clear()
         st.rerun()
       st.stop()

    st.write(f"Question: {st.session_state.current_q + 1}")
       
    if "current_question" not in st.session_state:
      with st.spinner("Generating Questions..."):
        st.session_state.current_question=generate_question(
          st.session_state.role,
          st.session_state.difficulty,
          st.session_state.experience,
          st.session_state.asked_questions
        )
        st.session_state.asked_questions.append(
          st.session_state.current_question
        )
      


    st.markdown("### Question:")
    st.write(st.session_state.current_question)

    answer=st.text_area(
      "Your Answer",
      key=f"answer_{st.session_state.input_key}"
    )
    col1, col2, col3 = st.columns(3)
    submit=col1.button("Submit")
    skip=col2.button("Skip")
    end=col3.button("End Interview")


#Submit logic
    if submit and answer:
      st.session_state.interview_data.append({
      "question":st.session_state.current_question,
      "answer":answer
  })
      st.session_state.current_q+=1
      st.session_state.input_key+=1

      del st.session_state.current_question
      st.rerun()


#Skip logic
    if skip:
     st.session_state.interview_data.append({
      "question":st.session_state.current_question,
      "answer":"Skipped"
  })
     st.session_state.current_q+=1
     st.session_state.input_key+=1

     del st.session_state.current_question
    
     st.rerun()

#End interview
    if end:
     st.session_state.ended=True
     st.rerun()
     

     if "current_question" in st.session_state:
       del st.session_state.current_question
      
     if "answer" in st.session_state:
       del st.session_state["answer"]
      
     st.rerun()