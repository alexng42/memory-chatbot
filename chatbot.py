import ollama

conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Be concise and friendly."
    }
]

def chat(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    
    response = ollama.chat(
        model="llama3:latest",
        messages=conversation_history
    )
    
    assistant_message = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

if __name__ == "__main__":
    print("Chatbot ready! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print(f"Bot: {chat(user_input)}")