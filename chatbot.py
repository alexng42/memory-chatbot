import ollama

MAX_MESSAGES = 20

conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Be concise and friendly."
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

def chat(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    
    trim_history()

    response = ollama.chat(
        model="llama3:latest",
        messages=conversation_history
    )
    
    assistant_message = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

if __name__ == "__main__":
    print("Llama3 ready. Type 'summary' to see a summary about you. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "summary":
            print(f"Bot: {summarize_user()}")
            continue
        print(f"Bot: {chat(user_input)}")