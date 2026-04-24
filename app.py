from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client=OpenAI()

def ask_question(question):
  response=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role":"user", "content": question}
    ]
  )
  return response.choices[0].message.content

if __name__ =="__main__":
  user_input=input("Enter your interview question: ")
  answer=ask_question(user_input)
  print("\nAI Response:\n")
  print(answer)
  