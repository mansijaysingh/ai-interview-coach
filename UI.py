import streamlit as st
import re
from app import generate_question, evaluate_interview,generate_ideal_answer



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
if "show_ideal" not in st.session_state:
  st.session_state.show_ideal=False
if "num_questions" not in st.session_state:
  st.session_state.num_questions=0






if not st.session_state.started:
  st.title("🤖 AI Interview Coach")
  st.subheader("Practice. Evaluate. Improve.")
  # st.write("Welcome! Start your AI-powered interview practice.")
  st.markdown("---")
  st.markdown("## 🎯 Setup Your Interview")
  

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
  # st.markdown("### 🧑‍💻 Role & Experience")
  role=st.selectbox("Select Role", roles)
  experience = st.selectbox("Experience Level", ["Junior", "Mid", "Senior"])

  # st.markdown("### ⚙️ Interview Settings")
  difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
  num_questions = st.slider("Number of Questions", 1, 30, 5)

# Start button
  col1, col2, col3 = st.columns([1,2,1])
  with col2:
    start = st.button("🚀 Start Interview", use_container_width=True)
  if start:
   st.session_state.started = True
   st.session_state.role=role
   st.session_state.experience=experience
   st.session_state.difficulty=difficulty
   st.session_state.num_questions=num_questions

   st.rerun()

if st.session_state.started :
    if not st.session_state.ended:
     st.markdown("## 🎯Interview in Progress")

    if (
      st.session_state.current_q>= st.session_state.num_questions
      or st.session_state.ended
    ):
       


       valid_data=[
        data for data in st.session_state.interview_data
        if data["answer"] != "Skipped"
    ]

       attempted=len(valid_data)

       if not st.session_state.show_ideal:
        if attempted>0:
         st.markdown("## 🎉 Interview Completed")
        else:
          st.markdown("## ⚠️ Interview Ended")
        st.markdown("---")
        st.markdown("## 📊 Final Evaluation")

       if attempted==0:
        st.info("You skipped all questions. Try attempting at least one 😊")
       else:
        with st.spinner("Evaluating your overall performance..."):
         result=evaluate_interview(valid_data)

        if not st.session_state.show_ideal:

          st.write(result)
          st.markdown("---")

          col1,col2,col3=st.columns([1,2,1])
          with col2:
           
           if st.button("💡 Show Ideal Answers", use_container_width=True):
             
             st.session_state.show_ideal=True
             st.rerun()
       
       
        else:
          st.markdown("## 💡 Ideal Answers")

          for i in range(len(st.session_state.interview_data)):
            data=st.session_state.interview_data[i]

            st.markdown(f"### Question {i+1}")
            st.write(data["question"])

            with st.spinner("Generating ideal answer..."):
              ideal=generate_ideal_answer(data["question"])

            st.write("**Ideal Answer:**")
            st.write(ideal)

            st.markdown("---")

       col1,col2,col3=st.columns([1,2,1])
       with col2:
        if st.button("🔄 Restart Interview", use_container_width=True):
          st.session_state.clear()
          st.rerun()
       st.stop()

    
       
    if "current_question" not in st.session_state:
      with st.spinner("🧠Generating your question..."):
        st.session_state.current_question=generate_question(
          st.session_state.role,
          st.session_state.difficulty,
          st.session_state.experience,
          st.session_state.asked_questions
        )
        st.session_state.asked_questions.append(
          st.session_state.current_question
        )
      

    st.markdown(f"### 📝 Question {st.session_state.current_q + 1} of {st.session_state.num_questions}")
    st.markdown("## 💬 Interview Question")
    st.info(st.session_state.current_question)

    answer = st.text_area(
    "",
    key=f"answer_{st.session_state.input_key}",
    placeholder="Type your answer here..."
)
    
    st.markdown("---")
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
     
     

     if "current_question" in st.session_state:
       del st.session_state.current_question
     st.rerun()     


    