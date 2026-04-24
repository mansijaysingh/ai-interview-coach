from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client=OpenAI()


print("\nWelcome to AI Interview Coach\n")
role=input("Enter your role (Python / AI / Frontend): ")
difficulty=input("Enter difficulty level (Easy / Medium / Hard): ")

# def ask_question(question):
#   response=client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#       {"role":"user", "content": question}
#     ]
#   )
#   return response.choices[0].message.content

def generate_question(role, difficulty):
  prompt=f"""
    You are an expert technical interviewer.

    Generate one {difficulty} level interview question for a {role} role.

    Only give the question, no explanation.
    """
  response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role":"user", "content":prompt}
    ]
  )

  return response.choices[0].message.content


# question=generate_question(role,difficulty)
# print(question)
# answer = input("\nYour Answer: ")

def evaluate_answer(question, answer):
  prompt= f"""
    You are an expert technical interviewer.

    Question: {question}
    Candidate Answer: {answer}

    Evaluate the answer based on:
    - Clarity
    - Technical Accuracy
    - Completeness

    Give output in this format:

    Score: X/10

    Strengths:
    - point 1
    - point 2

    Weaknesses:
    - point 1
    - point 2

    Suggestion:
    - improvement suggestion
    """
  response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role":"user", "content":prompt}
    ]
  )
  return response.choices[0].message.content

# result=evaluate_answer(question, answer)
# # print("\nEvaluation:\n")
# print(result)


def generate_ideal_answer(question):
  prompt=f"""
    You are an expert interviewer.

    Provide a perfect, concise, and well-structured answer for the following interview question:

    Question: {question}

    Keep it clear, professional, and easy to understand.
    """
  response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role":"user", "content":prompt}
    ]
  )
  return response.choices[0].message.content

# ideal=generate_ideal_answer(question)
# print("\nIdeal Answer:\n")
# print(ideal)

def generate_follow_up(question, answer):
  prompt=f"""
    You are an expert interviewer.

    Based on the following interview question and candidate's answer, generate one relevant follow-up question.

    Question: {question}
    Candidate Answer: {answer}

    The follow-up should:
    - Dig deeper into the topic
    - Be specific
    - Feel like a real interview

    Only give the question.
    """
  response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role":"user", "content":prompt}
    ]
      
        )
  return response.choices[0].message.content

# follow_up=generate_follow_up(question, answer)
# print("\nFollow-up Question:\n")
# print(follow_up)

num_questions=3

for i in range(num_questions):
    print(f"\n--- Question {i+1} ---")

    question = generate_question(role, difficulty)
    print("\nInterview Question:\n")
    print(question)

    answer = input("\nYour Answer: ")

    result = evaluate_answer(question, answer)
    print("\nEvaluation:\n")
    print(result)

    ideal = generate_ideal_answer(question)
    print("\nIdeal Answer:\n")
    print(ideal)

    followup = generate_follow_up(question, answer)
    print("\nFollow-up Question:\n")
    print(followup)