import ollama
response = ollama.chat(
    model="llama3:latest",
    messages=[{"role": "user", "content": "Say hello!"}]
)
print(response["message"]["content"])