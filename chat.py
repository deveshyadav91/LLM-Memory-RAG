import time

from google import genai
from config import API_KEY
from vector_store import search_memory

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"
RELEVANCE_THRESHOLD = 0.75


class ChatBot:

    def __init__(self):
        self.history = []

    def ask(self, query):

        self.history.append(f"User: {query}")

        full_history = "\n".join(self.history)

        baseline_prompt = f"""
You are a helpful conversational AI.

Here is the complete conversation history:

{full_history}

Answer the latest user question accurately using the conversation history.
"""

        retrieval_start = time.perf_counter()

        results = search_memory(query, top_k=3)

        relevant_results = [
            result
            for result in results
            if result["distance"] <= RELEVANCE_THRESHOLD
        ]

        retrieval_time = (
            time.perf_counter() - retrieval_start
        ) * 1000

        if relevant_results:

            memory_context = "\n\n".join(
                f"[{result['file']}]\n{result['content']}"
                for result in relevant_results
            )

            rag_prompt = f"""
You are a helpful conversational AI with long-term memory.

Relevant memories retrieved from the user's persistent memory:

{memory_context}

Current user question:
{query}

Use the retrieved memories when relevant.
If the answer is present in the memories, use that information.
Do not invent personal information.
"""

            memory_used = True

        else:

            rag_prompt = f"""
You are a helpful conversational AI.

Current user question:
{query}

Answer clearly and accurately.
Do not assume personal information that is not provided.
"""

            memory_used = False

        try:

            baseline_tokens = client.models.count_tokens(
                model=MODEL,
                contents=baseline_prompt
            ).total_tokens

            rag_tokens = client.models.count_tokens(
                model=MODEL,
                contents=rag_prompt
            ).total_tokens

            if baseline_tokens > 0:

                token_reduction = (
                    (baseline_tokens - rag_tokens)
                    / baseline_tokens
                ) * 100

            else:

                token_reduction = 0

        except Exception:

            token_reduction = 0

        generation_start = time.perf_counter()

        response = client.models.generate_content(
            model=MODEL,
            contents=rag_prompt
        )

        generation_time = (
            time.perf_counter() - generation_start
        ) * 1000

        total_time = retrieval_time + generation_time

        self.history.append(
            f"Assistant: {response.text}"
        )

        metrics = {
            "memory_used": memory_used,
            "token_reduction": token_reduction,
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": total_time
        }

        return response.text, metrics