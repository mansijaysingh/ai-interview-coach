from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client=OpenAI()

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


question=generate_question(role,difficulty)
print(question)
answer = input("\nYour Answer: ")






# if __name__ =="__main__":
#   user_input=input("Enter your interview question: ")
#   answer=ask_question(user_input)
#   print("\nAI Response:\n")
#   print(answer)
