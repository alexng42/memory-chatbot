import ollama
import json
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_DIR = os.path.join(BASE_DIR, "history")
os.makedirs(HISTORY_DIR, exist_ok=True)

MAX_MESSAGES = 20

conversation_history = [
    {
        "role": "system",
        "content": f"You are a helpful assistant. Be concise and friendly. Today's date is {datetime.now().strftime('%Y-%m-%d')}."
    }
]

def trim_history():
    # if the history exceeds max number of messages, remove the oldest ones
    if len(conversation_history) > MAX_MESSAGES:
         # save the system prompt
        system_prompt = conversation_history[0]
        # trim (save the last MAX_MESSAGES - 1 messages)
        conversation_history[1:] = conversation_history[-(MAX_MESSAGES - 1):]
        # restore the system prompt
        conversation_history[0] = system_prompt

def summarize_user():
    response = ollama.chat(
        model="llama3:latest",
        messages=conversation_history + [
            {
                "role": "user",
                "content": "Based on our conversation, summarize what you know about me."
            }
        ]
    )
    return response["message"]["content"]

# saving conversations
def save_conversation():
    filename = datetime.now().strftime("%Y-%m-%d") + ".json"
    with open(f"history/{filename}", "w") as f:
        json.dump(conversation_history, f)

# recall previous conversations
def search_history(date_string):
    filepath = os.path.join(HISTORY_DIR, f"{date_string}.json")
    
    if not is_valid_date(date_string):
        return "Please use the format YYYY-MM-DD, for example: recall 2026-01-06"
    
    if not os.path.exists(filepath):
        return f"No conversation found for {date_string}."
    
    with open(filepath, "r") as f:
        old_history = json.load(f)
    
    response = ollama.chat(
        model="llama3:latest",
        messages=old_history + [
            {
                "role": "user", 
                "content": f"Based only on the conversation above, summarize exactly what was discussed. Do not make anything up."
            }
        ]
    )
    return response["message"]["content"]

# validate date
def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def chat(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    
    trim_history()
    
    response = ollama.chat(
        model="llama3:latest",
        messages=conversation_history
    )
    
    assistant_message = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    save_conversation()  # save after every message
    
    return assistant_message

if __name__ == "__main__":
    print("Llama3 ready. Type 'summary' to see a summary about you. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            save_conversation()
            break
        if user_input.lower() == "summary":
            print(f"Bot: {summarize_user()}")
            continue
        if user_input.lower().startswith("recall "):
            date_string = user_input[7:]
            print(f"Bot: {search_history(date_string)}")
            continue
        print(f"Bot: {chat(user_input)}")