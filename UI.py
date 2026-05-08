import streamlit as st
import re
from app import generate_question, evaluate_interview

st.set_page_config(page_title="AI Interview Coach", layout="centered")

# ---------------- SESSION STATE ----------------
if "started" not in st.session_state:
    st.session_state.started = False

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "scores" not in st.session_state:
    st.session_state.scores = []

if "interview_data" not in st.session_state:
    st.session_state.interview_data = []

if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

if "ended" not in st.session_state:
    st.session_state.ended = False

if "num_questions" not in st.session_state:
    st.session_state.num_questions = 0


# ---------------- SETUP SCREEN ----------------
if not st.session_state.started:

    st.title("🤖 AI Interview Coach")
    st.subheader("Practice. Evaluate. Improve.")

    st.markdown("---")
    st.markdown("## 🎯 Setup Your Interview")

    roles = [
        "Python",
        "AI/ML",
        "Frontend",
        "Backend",
        "Full Stack",
        "Data Analyst",
        "HR"
    ]

    role = st.selectbox("Select Role", roles)

    experience = st.selectbox(
        "Experience Level",
        ["Junior", "Mid", "Senior"]
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    num_questions = st.slider(
        "Number of Questions",
        1,
        30,
        5
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        start = st.button(
            "🚀 Start Interview",
            use_container_width=True
        )

    if start:
        st.session_state.started = True
        st.session_state.role = role
        st.session_state.experience = experience
        st.session_state.difficulty = difficulty
        st.session_state.num_questions = num_questions

        st.rerun()


# ---------------- INTERVIEW SCREEN ----------------
if st.session_state.started:

    # ---------- INTERVIEW STATUS ----------
    if (
        not st.session_state.ended
        and st.session_state.current_q < st.session_state.num_questions
    ):
        st.markdown("## 🎯Interview in Progress")

    # ---------- END CONDITION ----------
    if (
        st.session_state.current_q >= st.session_state.num_questions
        or st.session_state.ended
    ):

        valid_data = [
            data for data in st.session_state.interview_data
            if data["answer"] != "Skipped"
        ]

        attempted = len(valid_data)

        # ---------- HEADINGS ----------
        if attempted > 0:
            st.markdown("## 🎉 Interview Completed")
        else:
            st.markdown("## ⚠️ Interview Ended")

        st.markdown("---")
        st.markdown("## 📊 Final Evaluation")

        # ---------- NO ATTEMPT CASE ----------
        if attempted == 0:

            st.info(
                "You skipped all questions. Try attempting at least one 😊"
            )

        # ---------- EVALUATION ----------
        else:

            with st.spinner(
                "Evaluating your overall performance..."
            ):
                result = evaluate_interview(valid_data)

            st.write(result)

            st.markdown("---")

        # ---------- RESTART BUTTON ----------
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            if st.button(
                "🔄 Restart Interview",
                use_container_width=True
            ):

                st.session_state.started = False
                st.session_state.current_q = 0
                st.session_state.interview_data = []
                st.session_state.asked_questions = []
                st.session_state.input_key = 0
                st.session_state.ended = False

                if "current_question" in st.session_state:
                    del st.session_state.current_question

                st.rerun()

        st.stop()

    # ---------- QUESTION GENERATION ----------
    if (
        st.session_state.started
        and not st.session_state.ended
        and st.session_state.current_q < st.session_state.num_questions
        and "current_question" not in st.session_state
    ):

        with st.spinner("🧠Generating your question..."):

            st.session_state.current_question = generate_question(
                st.session_state.role,
                st.session_state.difficulty,
                st.session_state.experience,
                st.session_state.asked_questions
            )

        st.session_state.asked_questions.append(
            st.session_state.current_question
        )

    # ---------- QUESTION DISPLAY ----------
    st.markdown(
        f"### 📝 Question "
        f"{st.session_state.current_q + 1} "
        f"of "
        f"{st.session_state.num_questions}"
    )

    st.markdown("## 💬 Interview Question")

    if "current_question" in st.session_state:
        st.info(st.session_state.current_question)

    # ---------- ANSWER INPUT ----------
    answer = st.text_area(
        "",
        key=f"answer_{st.session_state.input_key}",
        placeholder="Type your answer here..."
    )

    st.markdown("---")

    # ---------- BUTTONS ----------
    col1, col2, col3 = st.columns(3)

    submit = col1.button("Submit")
    skip = col2.button("Skip")
    end = col3.button("End Interview")

    # ---------- SUBMIT ----------
    if submit and answer:

        st.session_state.interview_data.append({
            "question": st.session_state.current_question,
            "answer": answer
        })

        st.session_state.current_q += 1
        st.session_state.input_key += 1

        del st.session_state.current_question

        st.rerun()

    # ---------- SKIP ----------
    if skip:

        st.session_state.interview_data.append({
            "question": st.session_state.current_question,
            "answer": "Skipped"
        })

        st.session_state.current_q += 1
        st.session_state.input_key += 1

        del st.session_state.current_question

        st.rerun()

    # ---------- END INTERVIEW ----------
    if end:

        st.session_state.ended = True

        if "current_question" in st.session_state:
            del st.session_state.current_question

        st.rerun()