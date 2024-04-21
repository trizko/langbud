import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_chatbot_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a friendly Spanish-speaking chatbot."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

def main():
    print("welcome to the langbud - the spanish teach chatbot!")
    print("you can start typing in spanish, and i will respond. type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = create_chatbot_response(user_input)
        print("Bot: ", response)

if __name__ == "__main__":
    main()
