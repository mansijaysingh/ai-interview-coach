import streamlit as st
from app import generate_question

st.set_page_config(page_title="AI Interview Coach", layout="centered")

# -------------------- Session State --------------------
if "started" not in st.session_state:
    st.session_state.started = False
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "interview_data" not in st.session_state:
    st.session_state.interview_data = []

# -------------------- UI --------------------
st.title("🤖 AI Interview Coach")
st.subheader("Practice. Evaluate. Improve.")

# -------------------- Setup Screen --------------------
if not st.session_state.started:
    roles = ["Python", "AI/ML", "Frontend", "Backend", "Full Stack", "Data Analyst", "HR"]

    role = st.selectbox("Select Role", roles)
    experience = st.selectbox("Experience Level", ["Junior", "Mid", "Senior"])
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Number of Questions", 1, 30, 5)

    if st.button("Start Interview 🚀"):
        st.session_state.started = True
        st.session_state.role = role
        st.session_state.experience = experience
        st.session_state.difficulty = difficulty
        st.session_state.num_questions = num_questions
        st.rerun()

# -------------------- Interview Screen --------------------
if st.session_state.started:

    # ✅ STOP when limit reached
    if st.session_state.current_q >= st.session_state.num_questions:
        st.success("Interview Completed 🎉")

        for i, data in enumerate(st.session_state.interview_data, start=1):
            st.markdown(f"### Q{i}: {data['question']}")
            st.write(f"**Your Answer:** {data['answer']}")
            st.markdown("---")

        if st.button("Restart"):
            st.session_state.clear()
            st.rerun()

    else:
        st.write(f"Question {st.session_state.current_q + 1}")

        # 🔥 KEY FIX: generate ONLY if not exists
        if "current_question" not in st.session_state:
            with st.spinner("Generating Question..."):
                st.session_state.current_question = generate_question(
                    st.session_state.role,
                    st.session_state.difficulty,
                    st.session_state.experience,
                    []
                )

        st.markdown("### Question:")
        st.write(st.session_state.current_question)

        # Answer input
        answer = st.text_area("Your Answer", key="answer")

        col1, col2, col3 = st.columns(3)
        submit = col1.button("Submit")
        skip = col2.button("Skip")
        end = col3.button("End Interview")

        # ---------------- Submit ----------------
        if submit and answer:
            st.session_state.interview_data.append({
                "question": st.session_state.current_question,
                "answer": answer
            })

            st.session_state.current_q += 1

            # reset answer
            st.session_state.pop("answer", None)

            # 🔥 VERY IMPORTANT
            st.session_state.pop("current_question", None)

            st.rerun()

        # ---------------- Skip ----------------
        if skip:
            st.session_state.interview_data.append({
                "question": st.session_state.current_question,
                "answer": "Skipped"
            })

            st.session_state.current_q += 1
            st.session_state.pop("answer", None)
            st.session_state.pop("current_question", None)

            st.rerun()

        # ---------------- End ----------------
        if end:
            st.session_state.clear()
            st.rerun()