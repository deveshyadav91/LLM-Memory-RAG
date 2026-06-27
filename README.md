# LLM-Memory-RAG

# LLM Memory RAG: A Lightweight Long-Term Memory System for LLMs

## Overview

Memory-RAG Lite is a lightweight Retrieval-Augmented Generation (RAG) system designed to provide **persistent long-term memory** for Large Language Models (LLMs). Instead of repeatedly sending the entire conversation history to the model, the system extracts important user information, stores it as structured memory, and retrieves only the most relevant context during future interactions.

This approach significantly reduces prompt size, improves response efficiency, and enables personalized conversations while minimizing API token consumption.

---

## Problem Statement

Most conversational AI systems rely on the complete chat history to maintain context. As conversations grow longer, this approach introduces several challenges:

* Increasing prompt token usage
* Higher API costs
* Increased response latency
* Limited scalability due to context window constraints

Long-term user information—such as preferences, skills, projects, or goals—is repeatedly transmitted even though only a small portion is relevant to the current query.

---

## Solution

LLM Memory RAG separates **short-term conversational context** from **long-term user memory**.

The system automatically extracts important information from conversations, stores it in structured Markdown files, indexes those memories using dense vector embeddings, and retrieves only semantically relevant memories when answering future queries.

Instead of processing thousands of conversation tokens, the language model receives only a concise set of relevant memories, reducing prompt size while preserving personalization.

---

## Key Features

* Persistent long-term memory for conversational AI
* Automatic memory extraction from conversations
* Structured Markdown-based memory storage
* Semantic memory retrieval using vector embeddings
* FAISS-based vector indexing for efficient similarity search
* Prompt token optimization through selective memory retrieval
* Lightweight command-line interface
* Modular and extensible architecture
* Built entirely using open-source tools and free APIs

---

# System Architecture

```text
                    User Query
                        │
                        ▼
               Gemini Language Model
                        │
                        ▼
             Conversation Logger
                        │
                        ▼
            Memory Extraction Module
                        │
                        ▼
            Structured Markdown Memory
                        │
                        ▼
          Sentence Transformer Embeddings
                        │
                        ▼
                 FAISS Vector Index
                        │
                        ▼
            Semantic Memory Retrieval
                        │
                        ▼
              Relevant Context Only
                        │
                        ▼
                Final LLM Response
```

---

## Workflow

### 1. Conversation Logging

Every interaction between the user and the language model is stored locally as conversation history.

### 2. Memory Extraction

After a conversation ends, the system identifies important long-term information, such as:

* Personal profile
* Skills
* Ongoing projects
* Preferences
* Goals

These memories are organized into structured Markdown files.

### 3. Vector Embedding

Each memory document is converted into a dense vector representation using the **all-MiniLM-L6-v2** Sentence Transformer model.

### 4. Vector Indexing

The generated embeddings are indexed using **FAISS**, enabling efficient semantic similarity search.

### 5. Semantic Retrieval

When the user asks a new question:

1. The query is embedded.
2. Similar memories are retrieved from FAISS.
3. Only relevant memories above a similarity threshold are selected.
4. Retrieved memories are appended to the prompt.

### 6. Response Generation

Gemini generates the final response using only:

* Retrieved long-term memories
* Current user query

This avoids sending the entire conversation history.

---

# Project Structure

```text
memory-rag-lite/
│
├── app.py
├── chat.py
├── config.py
├── memory.py
├── retrieve.py
├── token_counter.py
├── vector_store.py
│
├── conversations/
│   └── history.txt
│
├── memories/
│   ├── profile.md
│   ├── projects.md
│   ├── skills.md
│   ├── preferences.md
│   └── goals.md
│
├── faiss/
│   ├── memory.index
│   └── files.pkl
│
├── models/
│   └── all-MiniLM-L6-v2/
│
└── README.md
```

---

# Technology Stack

| Component            | Technology              |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| LLM                  | Google Gemini 2.5 Flash |
| Embedding Model      | all-MiniLM-L6-v2        |
| Vector Database      | FAISS                   |
| Memory Storage       | Markdown                |
| CLI                  | Rich                    |
| Numerical Computing  | NumPy                   |

---

# Memory Retrieval Pipeline

```text
User Query
     │
     ▼
Sentence Transformer
     │
     ▼
Query Embedding
     │
     ▼
FAISS Similarity Search
     │
     ▼
Relevant Memory Documents
     │
     ▼
Prompt Construction
     │
     ▼
Gemini API
     │
     ▼
Generated Response
```

---

# Token Optimization

### Traditional Chatbot

```
Conversation History
        │
        ▼
Entire Prompt Sent to LLM
```

Prompt size grows continuously as conversations become longer.

---

### Memory-RAG Lite

```
Relevant Memory
      +
Current Query
      │
      ▼
Prompt Sent to LLM
```

Only semantically relevant information is included in the prompt, significantly reducing token usage and improving inference efficiency.

---

# Example

### Conversation

```
User:
I am building a Memory-RAG Lite project.

User:
I know Python and C++.

User:
I prefer FastAPI.
```

Generated memory:

```markdown
projects.md

- Building Memory-RAG Lite
```

Later:

```
User:
What project am I currently working on?
```

The system retrieves the relevant memory from FAISS and provides the correct response without loading the complete conversation history.

---

# Installation

Clone the repository

```bash
git clone <repository-url>
cd memory-rag-lite
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
python app.py
```

---

# Future Improvements

* Incremental memory updates
* Memory importance scoring
* Metadata-based retrieval
* Hybrid retrieval (Vector + BM25)
* ChromaDB integration
* Multi-user memory management
* Streamlit web interface
* Memory versioning
* Automatic memory summarization

---

# Learning Outcomes

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation (RAG)
* Long-term memory systems for LLMs
* Semantic search
* Vector databases
* Dense text embeddings
* Prompt optimization
* API integration
* LLM application architecture
* Information retrieval

---

# Future Scope

LLM Memory RAG serves as a foundation for building production-grade AI assistants with persistent memory. The architecture can be extended to support enterprise knowledge bases, personalized assistants, customer support systems, educational tutors, and multi-session conversational agents.

---

# Author

**Devesh Yadav**


