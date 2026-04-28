from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client=OpenAI()


print("\nWelcome to AI Interview Coach\n")

def normalize(text):
   return text.strip().lower()

 # Define available roles
roles = [
    "python",
    "ai/ml",
    "frontend",
    "backend",
    "full stack",
    "data analyst",
    "hr"
]
print("Available Roles:")
for r in roles:
    print("-", r)

role_input=input("\nEnter role: ")
role=normalize(role_input)

if role not in roles:
   print("Invalid role selected!")
   exit()
print(f"\nRole: {role.title()}")


# Define experience levels
experience_input=input("Enter your experience(Junior / Mid / Senior): ")
experience=normalize(experience_input)
valid_experience = ['junior', 'mid', 'senior']

if experience not in valid_experience:
   print("Invalid experience level!")
   exit()
print(f"\nExperience Level: {experience.title()}")


# Get number of questions
num_questions=int(input("How many questions? (max 30): "))
if num_questions >30:
   print("max limit is 30!")
   exit()

print(f"\nNumber of Questions: {num_questions}\n")


# Get difficulty level
difficulty=input("Enter difficulty level (Easy / Medium / Hard): ")
difficulty=normalize(difficulty)
valid_difficulties = ['easy', 'medium', 'hard']
if difficulty not in valid_difficulties:
   print("Invalid difficulty level!")
   exit()
print(f"\nDifficulty Level: {difficulty.title()}\n")





def generate_question(role, difficulty,experience, previous_questions):
  prompt= f"""
You are an expert interviewer.

Generate ONE {difficulty} level interview question for a {experience} {role} candidate.

STRICT RULES:
- Do NOT repeat or rephrase similar questions
- Each question must be from a completely DIFFERENT topic
- Avoid already asked questions

Previously asked questions:
{previous_questions}

Only return the question.
"""
  response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role":"user", "content":prompt}
    ]
  )

  return response.choices[0].message.content




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

print("\n--- Starting Interview Simulation ---")
print("\nType 'skip' to skip a question")
print("Type 'exit' to end interview anytime\n")

scores=[]
attempted=0
questions_asked=0

interview_data=[]

asked_questions=[]



for i in range(num_questions):
    questions_asked+=1


    print(f"\n--- Question {i+1} ---")

    while True:
       question=generate_question(role,difficulty,experience,asked_questions)

       if question not in asked_questions:
          asked_questions.append(question)
          break
    # print("\nInterview Question:\n")
    print(question)

    answer = input("\nYour Answer: ").strip().lower()

    if answer == "exit":
       print("Interview ended by user.")

       interview_data.append({
          "question":question,
          "answer":"Exited",
          "evaluation": "Not Attempted"
       })
       break
    
    if answer == "skip":
       print("Question skipped.")

       interview_data.append({
          "question":question,
          "answer":"Skipped",
          "evaluation": "Not Attempted"
       })
       continue

    result = evaluate_answer(question, answer)

    interview_data.append({
       "question": question,
       "answer": answer,
       "evaluation": result
    })
    
    import re
    match = re.search(r"Score:\s*(\d+)", result)

    if match:
     score = int(match.group(1))
     scores.append(score)
     attempted += 1



print("\n--- Detailed Feedback ---\n")

for i, data in enumerate(interview_data, start=1):
    print(f"\nQuestion {i}:")
    print(data["question"])

    print("\nYour Answer:")
    print(data["answer"])

    print("\nEvaluation:")
    print(data["evaluation"])

    print("-"*40)

print("\n--- Interview Summary ---")
print(f"Total Questions Asked: {questions_asked}")
print(f"Attempted Questions: {attempted}")

if attempted>0:
   avg_score=sum(scores)/attempted
   print(f"Average Score: {avg_score:.2f}/10")
else:
   print("No questions attempted.")




show_ideal=input("\nDo you want to see ideal answers? (yes/no): ").strip().lower()
if show_ideal=="yes: ":
   print("\n--- Ideal Answers ---\n")

for i, data in enumerate(interview_data,start=1):
   print(f"\nQuestion {i}:")
   print(data["question"])

   ideal=generate_ideal_answer(data["question"])

   print("\nIdeal Answer: ")
   print(ideal)
   print("-"*40)

