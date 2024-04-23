import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
messages = [
    {"role": "system", "content": "You are a friendly Spanish-speaking chatbot. Your task is to help the user learn Spanish. You should continue the conversation in Spanish, but if the user makes a mistake, correct them in English."},
]

def create_chatbot_response(prompt):
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    content = response.choices[0].message.content
    messages.append({"role": "system", "content": content})

    return content

def main():
    print("Welcome to LangBud - the Spanish teaching chatbot!")
    print("You can start typing in Spanish, and I will respond. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = create_chatbot_response(user_input)
        print("Bot: ", response)

if __name__ == "__main__":
    main()
