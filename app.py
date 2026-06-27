from memory import extract_memory
import os
from rich.console import Console
from rich.panel import Panel

from chat import ChatBot

console = Console()

bot = ChatBot()

history_file = "conversations/history.txt"

os.makedirs("conversations", exist_ok=True)

conversation = []

console.print(
    Panel.fit(
        "[bold green]Memory-RAG Lite[/bold green]\nType 'exit' to quit.",
        title="LLM Memory System"
    )
)

while True:

    user = input("\nYou : ")

    if user.lower() == "exit":
        break

    reply = bot.ask(user)

    console.print(f"\n[cyan]AI :[/cyan] {reply}")

    conversation.append(f"User: {user}")
    conversation.append(f"Assistant: {reply}")

    # Save history after every exchange
    with open(history_file, "w", encoding="utf-8") as f:
        f.write("\n".join(conversation))

conversation_text = "\n".join(conversation)

with open(history_file, "w", encoding="utf-8") as f:
    f.write(conversation_text)

print("\nConversation Saved.")

print("\nExtracting Memory...")

from vector_store import build_index

extract_memory(conversation_text)

build_index()

print("\nMemory indexed successfully.")
