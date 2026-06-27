import os
import time

from google import genai
from google.genai import errors

from config import API_KEY
from retrieve import retrieve
from token_counter import count_tokens

client = genai.Client(api_key=API_KEY)


class ChatBot:

    def ask(self, query: str):

        # Retrieve relevant memories
        memories = retrieve(query)

        context = "\n\n".join(memories)

        # Load full conversation history
        history = ""

        history_path = "conversations/history.txt"

        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                history = f.read()

        # Prompt WITHOUT memory optimization
        full_history_prompt = f"""
Conversation History:

{history}

Current Question:
{query}
"""

        # Prompt WITH memory optimization
        memory_prompt = f"""
You are a helpful AI assistant.

Use ONLY the relevant memory below if it helps answer the question.

Relevant Memory:
{context}

Current Question:
{query}

Answer naturally.
"""

        # Token comparison
        full_tokens = count_tokens(full_history_prompt)
        memory_tokens = count_tokens(memory_prompt)

        print("\n" + "=" * 45)
        print("        MEMORY RAG COMPARISON")
        print("=" * 45)
        print(f"Without Memory RAG : {full_tokens} tokens")
        print(f"With Memory RAG    : {memory_tokens} tokens")

        if full_tokens > 0:
            reduction = (
                (full_tokens - memory_tokens)
                / full_tokens
            ) * 100

            print(f"Reduction          : {reduction:.2f}%")

        print("=" * 45)

        # Retry if Gemini is busy
        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=memory_prompt,
                )

                return response.text

            except errors.ServerError:

                print("Gemini server busy... Retrying...")
                time.sleep(2)

            except Exception as e:

                return f"Error: {e}"

        return "Gemini server unavailable. Please try again later."