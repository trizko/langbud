import openai
from dotenv import load_dotenv
import os

def load_openai_api_key():
    # Load environment variables
    load_dotenv()
    # Return the API key from environment variables
    return os.getenv("OPENAI_API_KEY")

def create_chatbot_response(prompt):
    openai.api_key = load_openai_api_key()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a friendly Spanish-speaking chatbot."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message['content']

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
