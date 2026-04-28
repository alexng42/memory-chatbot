Memory Chatbot

A locally-run AI chatbot built with Python and Ollama that maintains conversation memory across sessions.
Features

Conversational memory — remembers context within a session by maintaining full conversation history

Persistent storage — saves conversations to JSON files organized by date

Semantic search (RAG) — search across all past conversations using natural language queries powered by ChromaDB and sentence-transformers

Conversation recall — load and reference conversations from a specific date

User summarization — ask the bot to summarize everything it knows about you

Requirements

Python 3.9+

Ollama with llama3 pulled locally

Installation

Clone the repository:

bashgit clone https://github.com/yourusername/memory-chatbot.git

Install dependencies:

bashpip install ollama chromadb sentence-transformers

Make sure Ollama is running and llama3 is available:

bashollama pull llama3

Run the chatbot:

bashpython chatbot.py

Commands

summary: get a summary of what the bot knows about you

recall YYYY-MM-DD: Load conversations from a specific date

search <query>: Search across all past conversations semantically

!help: Show all available commands

quit: Exit the chatbot

How It Works

Memory — the full conversation history is sent to the model with every message, giving it context of the current session. History is trimmed to the last 20 messages to stay within the model's context window.

Persistent storage — conversations are saved to JSON files in a history/ folder organized by date. Multiple conversations on the same day are appended to the same file.

RAG (Retrieval Augmented Generation) — each message is converted to a vector embedding using all-MiniLM-L6-v2 and stored in a local ChromaDB database. When you use the search command, your query is converted to a vector and the most semantically similar past messages are retrieved and sent to the model as context.

Project Structure
```
memory-chatbot/
├── chatbot.py       # main chatbot logic and conversation loop
├── rag.py           # ChromaDB and sentence-transformers integration
├── history/         # saved conversation JSON files
└── README.md
```
