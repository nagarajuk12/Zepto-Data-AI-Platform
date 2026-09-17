# Zepto Support Assistant

A lightweight, robust Retrieval-Augmented Generation (RAG) customer support assistant pipeline powered by LangGraph, ChromaDB, and Sentence Transformers.

---
## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Pipeline Flowchart](#pipeline-flowchart)
- [Pipeline Stages](#pipeline-stages)
  - [1. Ingestion](#1-ingestion)
  - [2. Embedding & Vector Storage](#2-embedding--vector-storage)
  - [3. Intent Classification & Retrieval](#3-intent-classification--retrieval)
  - [4. Response Generation & Validation](#4-response-generation--validation)
- [Configuration & Execution Modes](#configuration--execution-modes)
  - [Mock Mode (`MOCK_LLM=1`)](#mock-mode-mock_llm1)
  - [Real LLM Mode (`MOCK_LLM=0`)](#real-llm-mode-mock_llm0)
- [Directory Structure](#directory-structure)
- [Execution Flow and Steps](#execution-flow-and-steps)
- [Libraries Used](#libraries-used)

---

## Overview

The **Zepto Support Assistant** provides automated customer support by coupling vector search over policy documents with conversational intent classification.

---
## System Architecture

The assistant implements a standard 4-stage RAG pipeline

$$\text{Ingestion} \longrightarrow \text{Embedding} \longrightarrow \text{Retrieval} \longrightarrow \text{Generation}$$

```
+-----------------------------------------------------------------------------+
|                               RAG PIPELINE                                  |
+-----------------------------------------------------------------------------+
   Documents (.txt)
         |
         v
   load_documents()               [Stage 1: Ingestion]
         |
         v
   create_chunks() (~300 chars)
         |
         v
   all-MiniLM-L6-v2               [Stage 2: Embedding]
         |
         v
   ChromaDB ("zepto_support")
         |
         v
   classify_intent                [Stage 3: Intent Classification]
         |
         +---------------------------------------+
         |                                       |
         v (Policy Question)                     v (General Question)
   retrieve_and_answer                     direct_answer
   - Top-3 chunks search                   - Static / Direct response
   - Context injection                     - No document retrieval
         |                                       |
         +-------------------+-------------------+
                             |
                             v
                     Final SupportResponse [Stage 4: Generation]
                     - answer
                     - sources
                     - confidence
```

---
## Pipeline Stages

### 1. Ingestion
Support policy documents are maintained in plain text format:
- **Location:** `support_assistant/docs/*.txt`
- **Document Loading:** The `load_documents()` function in `embeddings.py` reads and aggregates all `.txt` files.
- **Chunking:** `create_chunks()` partitions each document into smaller segments of approximately **300 characters**.
- **Chunk Identification:** Every chunk receives a deterministic unique identifier (e.g., `doc_03_chunk_0`).

### 2. Embedding & Vector Storage
Text chunks are embedded locally for low-latency similarity matching:
- **Embedding Model:** Local Sentence Transformers model `all-MiniLM-L6-v2`.
- **Function:** `create_embeddings()` in `embeddings.py`.
- **Vector Database:** ChromaDB.
- **Collection Name:** `zepto_support`.
- **Database Storage Path:** `support_assistant/chroma_db/`.

### 3. Intent Classification & Retrieval
User queries are routed through a LangGraph workflow triggered via `run_assistant()` in `graph.py`:

1. **`classify_intent` Node:** Evaluates the user query to determine whether it pertains to customer policies or general conversational chit-chat.
2. **Routing:**
   - **Policy Question $\rightarrow$ `retrieve_and_answer`:**
     - Query is embedded via `all-MiniLM-L6-v2`.
     - Queries the `zepto_support` ChromaDB collection.
     - Retrieves top **3** matching context chunks.
     - Extracted chunk IDs are tracked as references/sources.
   - **General Question $\rightarrow$ `direct_answer`:**
     - Bypasses vector search completely.
     - Emits a direct response without retrieving context documents.

### 4. Response Generation & Validation
Responses are structured and validated against strict Pydantic schemas:
- **Prompt Construction:** `build_prompt()` in `prompt.py` dynamically formats context and query instructions.
- **Schema Validation:** The output is validated against the `SupportResponse` Pydantic model (`schemas.py`):
  ```python
  class SupportResponse(BaseModel):
      answer: str
      sources: list[str]
      confidence: float
  ```
- For policy inquiries, `sources` contains the matching chunk IDs (e.g., `["doc_03_chunk_0", "doc_01_chunk_2"]`). For general chit-chat, `sources` remains empty.
---
## Configuration & Execution Modes

The execution behavior is governed by the `MOCK_LLM` environment variable.

### Mock Mode (`MOCK_LLM=1` - Default)
Designed for local testing, CI/CD, and environments without an active API key:
- **Intent Detection:** Keyword-based heuristic classification.
- **Retrieval:** Fully active; utilizes local `all-MiniLM-L6-v2` embeddings and ChromaDB.
- **Policy Answers:** Extracted directly from top retrieved context chunks.
- **General Answers:** Predefined fallback responses.
- **API Key:** Not required.

### Real LLM Mode (`MOCK_LLM=0`)
Utilizes a live LLM for contextual reasoning and generation:
- **Intent Detection:** LLM analyzes nuances in customer inquiries.
- **Prompting:** Context-stuffed prompts are processed by the LLM via `prompt.py`.
- **Validation:** Raw LLM outputs are parsed and verified through `SupportResponse`.
- **API Key:** Required.

---
## Directory Structure

```text
support_assistant/
├── docs/                     # Raw policy .txt files
├── chroma_db/                # Persistent ChromaDB vector store
├── embeddings.py             # Document loading, chunking, and embedding logic
├── graph.py                  # LangGraph workflow (classify, retrieve, answer)
├── prompt.py                 # System and user prompt builders
├── schemas.py                # Pydantic response models (SupportResponse)
└── api.py                    # Application entrypoint
```
---
## Execution Flow and Steps

Follow these steps to run the Zepto Support Assistant locally.

### Step 1: Clone the Repository

Clone the project from GitHub:

```bash
git clone <your-github-repository-url>
```
Move into the project folder:
```bash
cd <your-project-folder>
```
### Step 2: Check Python Version
```bash
python --version
```
### Step 3: Create a Virtual Environment
```bash
python -m venv .venv
```
Activate Virtual Environment
```bash
python -m venv .venv
```
### Step 4: Install Required Packages
Go to the support_assistant folder & Install the required packages:
```bash
cd support_assistant
pip install -r requirements.txt
```
### Step 5: Prepare the Support Documents
The support documents are stored in:

support_assistant/docs/
There are 8 .txt documents.

The documents contain information about:

* Delivery
* Returns and refunds
* Membership
* Order tracking
* Order cancellation
* Damaged or missing items
* Gift cards
* Support hours

### Step 6: Create Embeddings and ChromaDB
```bash
python embeddings.py
```
This will load the 8 support documents.
Split the documents into chunks. 
Create embeddings using all-MiniLM-L6-v2.
Store the embeddings in ChromaDB.
Create/use the zepto_support collection.

The ChromaDB data is stored in: *support_assistant/chroma_db/*

After successful execution, the output should show that the documents, chunks, embeddings, and ChromaDB records were created.

### Step 7: Check Mock LLM Mode

The project uses mock mode by default.

Set: **MOCK_LLM=1**
Mock mode does not require an LLM API key.
It uses:

* Keyword-based intent classification.
* Real ChromaDB retrieval.
* A fixed response for general questions.
* A deterministic response for retrieved policy questions.

This is the default mode used for the graded baseline.

### Step 8: Test the LangGraph Assistant
```bash
python graph.py
```
The LangGraph workflow contains three nodes:
```text
classify_intent
       |
       +----------------------+
       |                      |
       v                      v
retrieve_and_answer      direct_answer
       |                      |
       +----------+-----------+
                  |
                  v
             Final Response
```
Test a policy question such as:
```text
How long does Zepto delivery take?
```
This should be routed to:
```text
retrieve_and_answer
```
Test a general question such as:
```text
Who is the CEO of Zepto?
```
This should be routed to:
```text
direct_answer
```
### Step 9: Run the FastAPI Application
Make sure you are inside: **support_assistant/**

Run:
```blash
uvicorn api:app --reload
```
The API will start locally.
Open Swagger UI in your browser:
```text
http://localhost:8000/docs
```
### Step 10: Test the /ask Endpoint
The API uses:

POST /ask

Request format:
```text
{
  "query": "How long does Zepto delivery take?"
}
```
The response follows this structure:
```text
{
  "answer": "...",
  "sources": ["..."],
  "confidence": 1.0
}
```
### Step 11: Test the Dockerfile
Make sure Docker Desktop is running.

From the support_assistant folder, build the Docker image:
```blash
docker build -t zepto-support .
```
Run the container:
```blash
docker run --rm -p 8000:8000 zepto-support
```
The FastAPI application will run inside the container.

Open: http://localhost:8000/docs

---
## Libraries Used

The project uses the following Python libraries:

| Library | Purpose |
|---|---|
| `sentence-transformers` | Creating text embeddings using `all-MiniLM-L6-v2` |
| `chromadb` | Storing and searching document embeddings |
| `langgraph` | Building the RAG workflow and routing questions |
| `langchain-groq` | Connecting to the optional Groq LLM |
| `python-dotenv` | Loading environment variables |
| `pydantic` | Validating structured API responses |
| `fastapi` | Creating the REST API |
| `uvicorn` | Running the FastAPI application |
| `os` | File and environment variable handling |
| `pathlib` | Working with file and folder paths |
| `typing` | Type definitions such as `TypedDict` |

Overall, the system reads support documents, creates embeddings, stores them in ChromaDB, retrieves relevant information for policy questions, and then generates a structured answer.